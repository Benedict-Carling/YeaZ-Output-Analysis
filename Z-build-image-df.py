import nd2
import numpy as np
import pandas as pd
import h5py

FOLDER = "data/mar15/"

ND2FILE = FOLDER + "ChannelMono,Red,Green,Blue_Seq0000.nd2"
MASKFILE = FOLDER + "newmaskfile.h5"
ND2TOTALDFOUTOUT = FOLDER + "nd2_1.h5"
MASKTOTALDFOUTOUT = FOLDER + "mask.pkl"
TOTALDFOUTOUT = FOLDER + "all-images.pkl"

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
# h5df = readh5mask(MASKFILE)
nd2df.to_hdf(ND2TOTALDFOUTOUT, "df")
# h5df.to_pickle(MASKTOTALDFOUTOUT)
# totaldf = pd.concat([nd2df, h5df])
# totaldf.to_pickle(TOTALDFOUTOUT)
