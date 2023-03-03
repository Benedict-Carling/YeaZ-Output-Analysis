from typing import List
import pandas as pd
import tifffile
import numpy as np
from nd2reader import ND2Reader
import matplotlib.pyplot as plt
from math import isclose
import matplotlib.pyplot as plt
import h5py

ND2FILE = "data/feb22-mask/ChannelMono,Red,Green,Blue_Seq0000.nd2"
MASKFILE = "data/feb22-mask/newmaskfile.h5"


def readh5mask(path):
    # We use the 4th Channel for the masks
    df = pd.DataFrame(columns=["field-of-view", "channel", "image"])
    with h5py.File(path, "r") as f:
        for key in f.keys():
            data = f[key]
            b_group_key = list(data.keys())[0]
            df1 = np.array(f[key][b_group_key][()])
            df = df.append(
                {
                    "field-of-view": key.removeprefix("FOV"),
                    "channel": "Mask",
                    "image": df1,
                },
                ignore_index=True,
            )
    return df


def Nd2toDataFrame(path):
    df = pd.DataFrame(columns=["field-of-view", "channel", "image"])
    with ND2Reader(path) as images:
        images.iter_axes = "v"
        images.bundle_axes = "cyx"
        for FieldOfViewIndex, fov in enumerate(images):
            for ChannelIndex, channel in enumerate(fov):
                channel = ""
                if ChannelIndex == 0:
                    channel = "Mono"
                if ChannelIndex == 1:
                    channel = "Red"
                if ChannelIndex == 2:
                    channel = "Green"
                if ChannelIndex == 3:
                    channel = "Blue"

                df = df.append(
                    {
                        "field-of-view": FieldOfViewIndex,
                        "channel": ChannelIndex,
                        "image": channel,
                    },
                    ignore_index=True,
                )
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
    celldf = pd.DataFrame(
        columns=["field-of-view", "cellId", "mask-box", "binary-cell-mask", "size"]
    )
    data = df[df["channel"] == "Mask"]
    data = data.reset_index()
    for _index, item in data.iterrows():
        processMask = np.copy(item["image"])
        cellIds = np.delete(np.unique(processMask), 0)
        for cellId in cellIds:
            [x1, y1, x2, y2] = getMaskBoxForInt(cellId, processMask)
            cellMask = processMask[x1 : (x2 + 1), y1 : (y2 + 1)]
            BinaryCellMask = cleanMaskToBinaryMask(cellId, cellMask)
            celldf = celldf.append(
                {
                    "field-of-view": item["field-of-view"],
                    "cellId": cellId,
                    "mask-box": [x1, y1, x2, y2],
                    "binary-cell-mask": BinaryCellMask,
                    "size": BinaryCellMask.sum(),
                },
                ignore_index=True,
            )
    return celldf


nd2df = Nd2toDataFrame(ND2FILE)
h5df = readh5mask(MASKFILE)
totaldf = pd.concat([nd2df, h5df])

celldf = CreateCellDataFrama(totaldf)
celldf.to_pickle("feb22data.pkl")
print(celldf)
