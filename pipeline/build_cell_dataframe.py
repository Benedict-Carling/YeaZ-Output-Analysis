from analysis_path import CELLDIRECTORY

from typing import List
import nd2
import numpy as np
import pandas as pd
import h5py
from scipy.ndimage import gaussian_filter, binary_erosion, binary_dilation


ND2FILE = CELLDIRECTORY + "ChannelMono,Red,Green,Blue_Seq0000.nd2"
MASKFILE = CELLDIRECTORY + "newmaskfile.h5"
CELLOUT = CELLDIRECTORY + "cells-ratio-with-nuc.pkl"

import warnings

warnings.simplefilter("ignore")

# Default order
# –––––––––––––
# Field of view
# Z stack
# Channels
# Y
# X


def channelIndexToName(index: int):
    if index == 0:
        return "Mono"
    if index == 1:
        return "Red"
    if index == 2:
        return "Green"
    if index == 3:
        return "Blue"


def flatten(lst):
    """
    Flattens a nested list into a single list.
    """
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def grayscale_to_binary(image, threshold):
    """
    Converts a grayscale image to a binary image based on a threshold value.
    """
    binary = np.where(image > threshold, 1, 0)
    return binary


def apply_gaussian_blur(image, sigma):
    """
    Applies a Gaussian blur to a grayscale image.
    """
    blurred_image = gaussian_filter(image, sigma=sigma)
    return blurred_image


def erode_then_dilate(image, kernel_size):
    """
    Applies erosion and dilation to a grayscale image using a given kernel size.
    """
    kernel = np.ones((kernel_size, kernel_size), dtype=bool)
    eroded = binary_erosion(image, structure=kernel)
    dilated = binary_dilation(eroded, structure=kernel)
    return dilated


def get_cell_nucleus(bfp_channel):
    blurred_image = apply_gaussian_blur(bfp_channel, sigma=1)
    withoutzeros = blurred_image[blurred_image != 0]
    p = np.percentile(withoutzeros, 90)
    binary_image = grayscale_to_binary(blurred_image, p)
    result_image = erode_then_dilate(binary_image, kernel_size=3)
    return result_image


def mean_pixel_value(image, mask):
    """
    Finds the mean pixel value of a grayscale image within a binary mask.
    """
    # Apply the mask to the image
    # Find the mean pixel value of the masked image
    multiplied_mask = np.multiply(image, mask)
    mean = multiplied_mask[multiplied_mask != 0]
    return np.mean(mean)


def invert_binary_image(image):
    """
    Inverts a binary segmentation image.
    """
    inverted_image = np.logical_not(image)
    return inverted_image


def nuclear_cytosolic_ratio(gfp_channel, bfp_channel):
    nucleus_mask = get_cell_nucleus(bfp_channel)
    nuclear_score = mean_pixel_value(gfp_channel, nucleus_mask)
    cytosolic_score = mean_pixel_value(gfp_channel, invert_binary_image(nucleus_mask))
    loc_score = nuclear_score / cytosolic_score
    return loc_score, nuclear_score


def Nd2toDataFrame(path):
    print("Converting ND2 File to Dataframe")
    f = nd2.imread(path)
    df = pd.DataFrame(columns=["image-index", "field-of-view", "channel", "image"])
    for imageIndex, item in enumerate(f):
        print("Converting ND2 at index: ", imageIndex)
        for channelIndex, channel in enumerate(item):
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        [
                            {
                                "image-index": imageIndex + 1,
                                "field-of-view": ((imageIndex) // 2) + 1,
                                "channel": channelIndexToName(channelIndex),
                                "image": channel,
                            }
                        ]
                    ),
                ]
            )
    return df


def readh5mask(path):
    print("Converting H5 Mask to Dataframe")
    # We use the 4th Channel for the masks
    df = pd.DataFrame(columns=["field-of-view", "channel", "image"])
    with h5py.File(path, "r") as f:
        for key in f.keys():
            print("Converting H5 file at index: ", key)
            data = f[key]
            b_group_key = list(data.keys())[0]
            df1 = np.array(f[key][b_group_key][()])
            index = int(key.removeprefix("FOV"))
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        [
                            {
                                "image-index": int(index + 1),
                                "field-of-view": int((index) // 2) + 1,
                                "channel": "Mask",
                                "image": df1,
                                "max": df1.max(),
                            }
                        ]
                    ),
                ],
                ignore_index=True,
            )
    f.close()
    return df


def getMaskBoxForInt(cellId: int, image) -> List[int]:
    mask = np.copy(image)
    where = np.array(np.where(mask == cellId))
    x1, y1 = np.amin(where, axis=1)
    x2, y2 = np.amax(where, axis=1)
    return [x1, y1, x2, y2]


def cleanMaskToBinaryMask(int: int, image):
    mask = np.copy(image)
    mask[mask != int] = 0
    mask[mask == int] = 1
    return mask


def CreateCellDataFrama(df):
    print("Merging Mask and Image dataframe to cell dataframe")
    celldf = pd.DataFrame(
        columns=[
            "field-of-view",
            "image-index",
            "cellId",
            "size",
            "meanRedValue",
            "score",
        ]
    )
    masks = df[df["channel"] == "Mask"]
    masks = masks.reset_index()
    for _index, item in masks.iterrows():
        processMask = np.copy(item["image"])
        cellIds = np.delete(np.unique(processMask), 0)
        print("Evaluting Cells statistics in mask: ", _index)
        for cellId in cellIds:
            [x1, y1, x2, y2] = getMaskBoxForInt(cellId, processMask)
            cellMask = processMask[x1 : (x2 + 1), y1 : (y2 + 1)]
            BinaryCellMask = cleanMaskToBinaryMask(cellId, cellMask)
            if BinaryCellMask.shape[0] <= 7:
                continue
            if BinaryCellMask.shape[1] <= 7:
                continue
            redChannel = df.loc[
                (df["channel"] == "Red") & (df["image-index"] == item["image-index"])
            ].iloc[0]
            redWindow = redChannel["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            redCell = np.multiply(redWindow, BinaryCellMask)

            # blue 0
            blueChannel0 = df.loc[
                (df["channel"] == "Blue") & (df["image-index"] == item["image-index"])
            ].iloc[0]
            blueWindow0 = blueChannel0["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            blueCell0 = np.multiply(blueWindow0, BinaryCellMask)

            # Green 0
            greenChannel0 = df.loc[
                (df["channel"] == "Green") & (df["image-index"] == item["image-index"])
            ].iloc[0]
            greenWindow0 = greenChannel0["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            greenCell0 = np.multiply(greenWindow0, BinaryCellMask)

            score0, nuc_score0 = nuclear_cytosolic_ratio(greenCell0, blueCell0)

            if score0:
                celldf = pd.concat(
                    [
                        celldf,
                        pd.DataFrame(
                            [
                                {
                                    "image-index": item["image-index"],
                                    "field-of-view": item["field-of-view"],
                                    "cellId": cellId,
                                    "size": BinaryCellMask.sum(),
                                    "meanRedValue": redCell.mean(),
                                    "score": score0,
                                }
                            ]
                        ),
                    ]
                )
    return celldf


# nd2df = Nd2toDataFrame(ND2FILE)
h5df = readh5mask(MASKFILE)
print(h5df)
# totaldf = pd.concat([nd2df, h5df])
# # Suppress/hide the warning
# np.seterr(invalid="ignore")
# celldf = CreateCellDataFrama(totaldf)
# print(totaldf)
# print(celldf)

# try:
#     celldf.to_pickle(CELLOUT)
# except:
#     print("Unable to print")
