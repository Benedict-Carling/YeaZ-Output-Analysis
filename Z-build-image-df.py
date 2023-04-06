from ast import List
import nd2
import numpy as np
import pandas as pd
import h5py

FOLDER = "data/april5/"

ND2FILE = FOLDER + "ChannelMono,Red,Green,Blue_Seq0000.nd2"
MASKFILE = FOLDER + "newmaskfile.h5"
ND2TOTALDFOUTOUT = FOLDER + "nd2_1.h5"
MASKTOTALDFOUTOUT = FOLDER + "mask.pkl"
TOTALDFOUTOUT = FOLDER + "all-images.pkl"
CELLOUT = FOLDER + "cells.pkl"

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


def Nd2toDataFrame(path):
    f = nd2.imread(path)
    df = pd.DataFrame(
        columns=["image-index", "field-of-view", "channel", "z-index", "image"]
    )
    for imageIndex, item in enumerate(f):
        # for zIndex, z in enumerate(item):
        for channelIndex, channel in enumerate(item[1]):
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        [
                            {
                                "image-index": imageIndex + 1,
                                "field-of-view": ((imageIndex) // 9) + 1,
                                "channel": channelIndexToName(channelIndex),
                                "z-index": 1,
                                "image": channel,
                            }
                        ]
                    ),
                ]
            )
    return df


def readh5mask(path):
    # We use the 4th Channel for the masks
    df = pd.DataFrame(columns=["field-of-view", "channel", "image"])
    with h5py.File(path, "r") as f:
        for key in f.keys():
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
    return df


nd2df = Nd2toDataFrame(ND2FILE)
h5df = readh5mask(MASKFILE)


def getMaskBoxForInt(cellId: int, image):
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
    celldf = pd.DataFrame(
        columns=[
            "image-index",
            "field-of-view",
            "cellId",
            "size",
            "meanRedValue",
            "meanBlueValue",
            "meanGreenValue",
            "greenBlueCorrelation",
        ]
    )
    masks = df[df["channel"] == "Mask"]
    masks = masks.reset_index()
    for _index, item in masks.iterrows():
        processMask = np.copy(item["image"])
        cellIds = np.delete(np.unique(processMask), 0)
        for cellId in cellIds:
            [x1, y1, x2, y2] = getMaskBoxForInt(cellId, processMask)
            cellMask = processMask[x1 : (x2 + 1), y1 : (y2 + 1)]
            BinaryCellMask = cleanMaskToBinaryMask(cellId, cellMask)
            redChannel = df.loc[
                (df["channel"] == "Red") & (df["image-index"] == item["image-index"])
            ].iloc[0]
            redWindow = redChannel["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            redCell = np.multiply(redWindow, BinaryCellMask)
            blueChannel = df.loc[
                (df["channel"] == "Blue") & (df["image-index"] == item["image-index"])
            ].iloc[0]
            blueWindow = blueChannel["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            blueCell = np.multiply(blueWindow, BinaryCellMask)
            greenChannel = df.loc[
                (df["channel"] == "Green") & (df["image-index"] == item["image-index"])
            ].iloc[0]
            greenWindow = greenChannel["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            greenCell = np.multiply(greenWindow, BinaryCellMask)
            # Correlation Statistics
            roundBlue = blueCell[blueCell != 0.0]
            roundGreen = greenCell[greenCell != 0.0]
            roundBlueflat = (roundBlue.flatten(),)
            roundGreenflat = roundGreen.flatten()
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
                                "meanBlueValue": blueCell.mean(),
                                "meanGreenValue": greenCell.mean(),
                                "greenBlueCorrelation": np.corrcoef(
                                    roundBlueflat, roundGreenflat
                                )[0][1],
                            }
                        ]
                    ),
                ],
                ignore_index=True,
            )
    return celldf


totaldf = pd.concat([nd2df, h5df])
celldf = CreateCellDataFrama(totaldf)

try:
    celldf.to_pickle(CELLOUT)
except:
    print("Unable to write")
