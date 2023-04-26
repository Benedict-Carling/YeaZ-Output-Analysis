from typing import List
import nd2
import cv2
import numpy as np
import pandas as pd
import h5py
from skimage import measure
from skimage.metrics import structural_similarity as ssim
import json

FOLDER = "data/april24-2/"

ND2FILE = FOLDER + "ChannelMono,Red,Green,Blue_Seq0000.nd2"
MASKFILE = FOLDER + "newmaskfile.h5"
CELLOUT = FOLDER + "raw_images"
SUBPOP_MASKS = FOLDER + "subpop_masks"
from PIL import Image

import warnings

warnings.simplefilter("ignore")

FOV = 14


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
        imageFOV = imageIndex + 1
        print("Converting ND2 at index: ", imageIndex)
        for channelIndex, channel in enumerate(item):
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        [
                            {
                                "image-index": imageFOV,
                                "field-of-view": imageFOV,
                                "channel": channelIndexToName(channelIndex),
                                "image": channel,
                            }
                        ]
                    ),
                ]
            )
            arr2img(
                "{}/{}_{}.png".format(
                    CELLOUT, imageFOV, channelIndexToName(channelIndex)
                ),
                channel,
            )
    return df


def readh5mask(path, labels):
    print("Converting H5 Mask to Dataframe")
    # We use the 4th Channel for the masks
    df = pd.DataFrame(columns=["field-of-view", "channel", "image"])
    with h5py.File(path, "r") as f:
        for key in f.keys():
            data = f[key]
            b_group_key = list(data.keys())[0]
            df1 = np.array(f[key][b_group_key][()])
            index = int(key.removeprefix("FOV"))
            print("Converting H5 file at index: ", key)
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
            try:
                mask2img(
                    "{}/{}_{}_{}.png".format(
                        SUBPOP_MASKS, int(index + 1), "blue", "mask"
                    ),
                    df1,
                    labels[str(float(index + 1))]["blue"],
                    (255, 0, 0),
                )
                mask2img(
                    "{}/{}_{}_{}.png".format(
                        SUBPOP_MASKS, int(index + 1), "red", "mask"
                    ),
                    df1,
                    labels[str(float(index + 1))]["red"],
                    (0, 0, 255),
                )
            except:
                print("i")
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


def arr2img(filename, arr):
    # Map the lowest pixel value to 0 and the highest to 355
    arr = ((arr - np.min(arr)) / (np.max(arr) - np.min(arr))) * 255
    # Round the pixel values to the nearest integer
    arr = np.round(arr).astype("uint8")
    # Create an image object from the array
    im = Image.fromarray(arr)
    # Save the image
    im.save(filename)


def set_allowed_pixels(arr, allowed_pixels):
    # Create a Boolean mask of the allowed pixels
    allowed_mask = np.isin(arr, allowed_pixels)

    # Set all pixels outside the mask to zero
    arr[~allowed_mask] = 0

    return arr


def mask2img(filename, array, ids, color):
    arr = array.copy()
    allowed_pixels = np.array(ids)
    arr = set_allowed_pixels(arr, allowed_pixels)
    arr = np.where(arr >= 1, 1, arr)
    outlines = get_mask_outline(arr)
    # Create an image object from the array
    # Map the lowest pixel value to 0 and the highest to 355
    outlines = (
        (outlines - np.min(outlines)) / (np.max(outlines) - np.min(outlines))
    ) * 255
    # Round the pixel values to the nearest integer
    outlines = np.round(outlines).astype("uint8")
    # Create an RGB version of the grayscale array for colorization
    gray_rgb = cv2.cvtColor(outlines, cv2.COLOR_GRAY2RGB)

    # Define the neon green color for the image

    # Threshold the grayscale array to create a binary mask of non-black pixels
    _, mask = cv2.threshold(outlines, 1, 255, cv2.THRESH_BINARY)

    # Apply the mask to the RGB array to change only the non-black pixels to neon green
    gray_rgb[mask != 0] = color
    cv2.imwrite(filename, gray_rgb)


def get_mask_outline(mask):
    """
    Returns an array of the outline of a binary segmentation mask.
    """
    contours, _ = cv2.findContours(
        mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    outline_mask = np.zeros_like(mask)
    cv2.drawContours(outline_mask, contours, -1, 1, thickness=1)
    return outline_mask


def load_dict_from_json(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    return data


cellLabels = load_dict_from_json("{}labelled_cells.json".format(FOLDER))
print(cellLabels)
# nd2df = Nd2toDataFrame(ND2FILE)
# print(nd2df)
h5df = readh5mask(MASKFILE, cellLabels)
print(h5df)