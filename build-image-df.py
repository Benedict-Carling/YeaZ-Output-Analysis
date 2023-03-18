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

ND2FILE = FOLDER+"ChannelMono,Red,Green,Blue_Seq0000.nd2"
MASKFILE = FOLDER+"newmaskfile.h5"
TOTALDFOUTOUT = FOLDER+"all-images.pkl"


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
                    "field-of-view": int(key.removeprefix("FOV")),
                    "channel": "Mask",
                    "image": df1,
                    "imageShape": df1.shape,

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
                channelName = ""
                if ChannelIndex == 0:
                    channelName = "Mono"
                if ChannelIndex == 1:
                    channelName = "Red"
                if ChannelIndex == 2:
                    channelName = "Green"
                if ChannelIndex == 3:
                    channelName = "Blue"

                df = df.append(
                    {
                        "field-of-view": FieldOfViewIndex,
                        "channel": channelName,
                        "image": np.array(channel),
                        "imageShape": np.array(channel).shape,
                    },
                    ignore_index=True,
                )
    return df


nd2df = Nd2toDataFrame(ND2FILE)
h5df = readh5mask(MASKFILE)
totaldf = pd.concat([nd2df, h5df])
totaldf.to_pickle(TOTALDFOUTOUT)
