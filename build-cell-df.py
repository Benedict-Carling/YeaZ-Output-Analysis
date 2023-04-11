from typing import List
import pandas as pd
import tifffile
import numpy as np
from nd2reader import ND2Reader
import matplotlib.pyplot as plt
from math import isclose
import matplotlib.pyplot as plt
import h5py

FOLDER = "data/feb22/"

TOTALDFOUTOUT = FOLDER + "all-images.pkl"
CELLDF = FOLDER + "all-cells.pkl"


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
    celldf = pd.DataFrame(
        columns=["field-of-view", "cellId", "mask-box", "binary-cell-mask", "size"]
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
                (df["channel"] == "Red")
                & (df["field-of-view"] == item["field-of-view"])
            ].iloc[0]
            redWindow = redChannel["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            redCell = np.multiply(redWindow, BinaryCellMask)
            blueChannel = df.loc[
                (df["channel"] == "Blue")
                & (df["field-of-view"] == item["field-of-view"])
            ].iloc[0]
            blueWindow = blueChannel["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            blueCell = np.multiply(blueWindow, BinaryCellMask)
            greenChannel = df.loc[
                (df["channel"] == "Green")
                & (df["field-of-view"] == item["field-of-view"])
            ].iloc[0]
            greenWindow = greenChannel["image"][x1 : (x2 + 1), y1 : (y2 + 1)]
            greenCell = np.multiply(greenWindow, BinaryCellMask)
            # Correlation Statistics
            roundBlue = blueCell[blueCell != 0.0]
            roundGreen = greenCell[greenCell != 0.0]
            roundBlueflat = (roundBlue.flatten(),)
            roundGreenflat = roundGreen.flatten()
            celldf = celldf.append(
                {
                    "field-of-view": item["field-of-view"],
                    "cellId": cellId,
                    "mask-box": [x1, y1, x2, y2],
                    "binary-cell-mask": BinaryCellMask,
                    "size": BinaryCellMask.sum(),
                    "meanRedValue": redCell.mean(),
                    "meanBlueValue": blueCell.mean(),
                    "meanGreenValue": greenCell.mean(),
                    "greenBlueCorrelation": np.corrcoef(roundBlueflat, roundGreenflat)[
                        0
                    ][1],
                    "roundBlue": roundBlue,
                    "roundBlueflat": roundBlueflat,
                },
                ignore_index=True,
            )
    return celldf


totaldf = pd.read_pickle(TOTALDFOUTOUT)
celldf = CreateCellDataFrama(totaldf)
celldf.to_pickle(CELLDF)
print(celldf)
