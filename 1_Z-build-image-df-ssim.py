from typing import List
import nd2
import numpy as np
import pandas as pd
import h5py
from skimage.metrics import structural_similarity as ssim

FOLDER = "data/april5/"

ND2FILE = FOLDER + "ChannelMono,Red,Green,Blue_Seq0000.nd2"
MASKFILE = FOLDER + "newmaskfile.h5"
ND2TOTALDFOUTOUT = FOLDER + "nd2_1.h5"
MASKTOTALDFOUTOUT = FOLDER + "mask.pkl"
TOTALDFOUTOUT = FOLDER + "all-images.pkl"
CELLOUT = FOLDER + "cells-ssim-win7.pkl"

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


def maximum(a, b):
    if a >= b:
        return a
    else:
        return b


def minimum(a, b):
    if a >= b:
        return b
    else:
        return a


def Nd2toDataFrame(path):
    print("Converting ND2 File to Dataframe")
    f = nd2.imread(path)
    df = pd.DataFrame(
        columns=["image-index", "field-of-view", "channel", "z-index", "image"]
    )
    for imageIndex, item in enumerate(f):
        print("Converting ND2 at index: ", imageIndex)
        for zIndex, z in enumerate(item):
            for channelIndex, channel in enumerate(z):
                df = pd.concat(
                    [
                        df,
                        pd.DataFrame(
                            [
                                {
                                    "image-index": imageIndex + 1,
                                    "field-of-view": ((imageIndex) // 9) + 1,
                                    "channel": channelIndexToName(channelIndex),
                                    "z-index": zIndex,
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
                                "field-of-view": int((index) // 9) + 1,
                                "channel": "Mask",
                                "z-index": 3,
                                "image": df1,
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
            # "mask-box",
            # "binary-cell-mask",
            "size",
            "meanRedValue",
            "meanBlueValue",
            "meanGreenValue",
            "greenBlueCorrelation0",
            "greenBlueCorrelation1",
            "greenBlueCorrelation2",
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
            if BinaryCellMask.sum() <= 5:
                continue
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
                (df["channel"] == "Blue")
                & (df["image-index"] == item["image-index"])
                & (df["z-index"] == 0)
            ].iloc[0]
            blueWindow0 = blueChannel0["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            blueCell0 = np.multiply(blueWindow0, BinaryCellMask)

            # blue 1
            blueChannel1 = df.loc[
                (df["channel"] == "Blue")
                & (df["image-index"] == item["image-index"])
                & (df["z-index"] == 1)
            ].iloc[0]
            blueWindow1 = blueChannel1["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            blueCell1 = np.multiply(blueWindow1, BinaryCellMask)

            # blue 2
            blueChannel2 = df.loc[
                (df["channel"] == "Blue")
                & (df["image-index"] == item["image-index"])
                & (df["z-index"] == 2)
            ].iloc[0]
            blueWindow2 = blueChannel2["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            blueCell2 = np.multiply(blueWindow2, BinaryCellMask)

            # Green 0
            greenChannel0 = df.loc[
                (df["channel"] == "Green")
                & (df["image-index"] == item["image-index"])
                & (df["z-index"] == 0)
            ].iloc[0]
            greenWindow0 = greenChannel0["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            greenCell0 = np.multiply(greenWindow0, BinaryCellMask)
            # Green 1
            greenChannel1 = df.loc[
                (df["channel"] == "Green")
                & (df["image-index"] == item["image-index"])
                & (df["z-index"] == 1)
            ].iloc[0]
            greenWindow1 = greenChannel1["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            greenCell1 = np.multiply(greenWindow1, BinaryCellMask)
            # Green 2
            greenChannel2 = df.loc[
                (df["channel"] == "Green")
                & (df["image-index"] == item["image-index"])
                & (df["z-index"] == 2)
            ].iloc[0]
            greenWindow2 = greenChannel2["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            greenCell2 = np.multiply(greenWindow2, BinaryCellMask)

            # Append
            celldf = pd.concat(
                [
                    celldf,
                    pd.DataFrame(
                        [
                            {
                                "image-index": item["image-index"],
                                "field-of-view": item["field-of-view"],
                                "cellId": cellId,
                                "shape0": BinaryCellMask.shape[0],
                                "shape1": BinaryCellMask.shape[1],
                                # "mask-box": [x1, y1, x2, y2],
                                # "binary-cell-mask": BinaryCellMask,
                                "size": BinaryCellMask.sum(),
                                "meanRedValue": redCell.mean(),
                                "meanBlueValue": blueCell1.mean(),
                                "meanGreenValue": greenCell2.mean(),
                                "greenBlueCorrelation0": ssim(
                                    blueCell0,
                                    greenCell0,
                                    win_size=7,
                                    gaussian_weights=True,
                                    data_range=maximum(
                                        blueCell0.max(), greenCell0.max()
                                    )
                                    - minimum(blueCell0.min(), greenCell0.min()),
                                ),
                                "greenBlueCorrelation1": ssim(
                                    blueCell1,
                                    greenCell1,
                                    win_size=7,
                                    gaussian_weights=True,
                                    data_range=maximum(
                                        blueCell1.max(), greenCell1.max()
                                    )
                                    - minimum(blueCell1.min(), greenCell1.min()),
                                ),
                                "greenBlueCorrelation2": ssim(
                                    blueCell2,
                                    greenCell2,
                                    win_size=7,
                                    gaussian_weights=True,
                                    data_range=maximum(
                                        blueCell2.max(), greenCell2.max()
                                    )
                                    - minimum(blueCell2.min(), greenCell2.min()),
                                ),
                            }
                        ]
                    ),
                ]
            )
    return celldf


nd2df = Nd2toDataFrame(ND2FILE)
print(nd2df)
h5df = readh5mask(MASKFILE)
print(h5df)
totaldf = pd.concat([nd2df, h5df])
# Suppress/hide the warning
np.seterr(invalid="ignore")
celldf = CreateCellDataFrama(totaldf)
print(totaldf)
print(celldf)

try:
    celldf.to_pickle(CELLOUT)
except:
    print("Unable to print")
