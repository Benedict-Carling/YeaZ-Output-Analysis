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
        columns=["image-index", "channel", "z-index", "image"]
    )
    for imageIndex, item in enumerate(f):
        for zIndex, z in enumerate(item):
            for channelIndex, channel in enumerate(item[1]):
                df = pd.concat(
                    [
                        df,
                        pd.DataFrame(
                            [
                                {
                                    "image-index": imageIndex + 1,
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
    # We use the 4th Channel for the masks
    df = pd.DataFrame(columns=["channel", "image"])
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

            # Blue 0
            blueChannel0 = df.loc[
                (df["channel"] == "Blue") & (df["image-index"] == item["image-index"])
            ].iloc[0]
            blueWindow0 = blueChannel0["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            blueCell0 = np.multiply(blueWindow0, BinaryCellMask)

            # Blue 1
            blueChannel1 = df.loc[
                (df["channel"] == "Blue") & (df["image-index"] == item["image-index"])
            ].iloc[1]
            blueWindow1 = blueChannel1["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            blueCell1 = np.multiply(blueWindow1, BinaryCellMask)

            # Blue 2
            blueChannel2 = df.loc[
                (df["channel"] == "Blue") & (df["image-index"] == item["image-index"])
            ].iloc[2]
            blueWindow2 = blueChannel2["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            blueCell2 = np.multiply(blueWindow2, BinaryCellMask)

            # Green 0
            greenChannel0 = df.loc[
                (df["channel"] == "Green") & (df["image-index"] == item["image-index"])
            ].iloc[0]
            greenWindow0 = greenChannel0["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            greenCell0 = np.multiply(greenWindow0, BinaryCellMask)

            # Green 1
            greenChannel1 = df.loc[
                (df["channel"] == "Green") & (df["image-index"] == item["image-index"])
            ].iloc[1]
            greenWindow1 = greenChannel1["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            greenCell1 = np.multiply(greenWindow1, BinaryCellMask)

            # Green 2
            greenChannel2 = df.loc[
                (df["channel"] == "Green") & (df["image-index"] == item["image-index"])
            ].iloc[2]
            greenWindow2 = greenChannel2["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            greenCell2 = np.multiply(greenWindow2, BinaryCellMask)

            # Correlation 0
            roundBlue0 = blueCell0[blueCell0 != 0.0]
            roundGreen0 = greenCell0[greenCell0 != 0.0]
            roundBlueflat0 = (roundBlue0.flatten(),)
            roundGreenflat0 = roundGreen0.flatten()

            # Correlation 1
            roundBlue1 = blueCell1[blueCell1 != 0.0]
            roundGreen1 = greenCell1[greenCell1 != 0.0]
            roundBlueflat1 = (roundBlue1.flatten(),)
            roundGreenflat1 = roundGreen1.flatten()

            # Correlation 2
            roundBlue2 = blueCell2[blueCell2 != 0.0]
            roundGreen2 = greenCell2[greenCell2 != 0.0]
            roundBlueflat2 = (roundBlue2.flatten(),)
            roundGreenflat2 = roundGreen2.flatten()

            celldf = pd.concat(
                [
                    celldf,
                    pd.DataFrame(
                        [
                            {
                                "image-index": item["image-index"],
                                "cellId": cellId,
                                "size": BinaryCellMask.sum(),
                                "meanRedValue": redCell.mean(),
                                "meanBlueValue": blueCell0.mean(),
                                "meanGreenValue": greenCell0.mean(),
                                "greenBlueCorrelation0": np.corrcoef(
                                    roundBlueflat0, roundGreenflat0
                                )[0][1],
                                "greenBlueCorrelation1": np.corrcoef(
                                    roundBlueflat1, roundGreenflat1
                                )[0][1],
                                "greenBlueCorrelation2": np.corrcoef(
                                    roundBlueflat2, roundGreenflat2
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
