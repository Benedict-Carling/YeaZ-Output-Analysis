from typing import Literal
import pandas as pd
import matplotlib.pyplot as plt

from helper_analysis_path import CELLPATH
from helper_analysis_path import CELLDIRECTORY
from helper_analysis_path import FILENAME
from scipy.spatial.distance import cdist


df = pd.read_pickle(CELLPATH)

# April5 4 hours NLIM
# Low 100-310 size
# High 350-560 size

# April 6 4 hour GLN
# Size 120 - 700
# Red 110 - 450


def Limitdf(df, type: Literal["april5", "april6-4","april24-2","april24-3"]):
    if type=="april24-2":
        df = df[df["size"] > 100]
        df = df[df["size"] < 600]
        df = df[df["meanRedValue"] > 180]
        df = df[df["meanRedValue"] < 450]
    if type=="april24-3":
        df = df[df["size"] > 100]
        df = df[df["size"] < 600]
        df = df[df["meanRedValue"] > 180]
        df = df[df["meanRedValue"] < 450]
    if type == "april6-4":
        df = df[df["size"] > 130]
        df = df[df["size"] < 700]
        df = df[df["meanRedValue"] > 110]
        df = df[df["meanRedValue"] < 450]
    return df


def getAxisLimit(type: Literal["april5", "april6-4","april24-2","april24-3"]):
    if type == "april24-2":
        return [100, 600, 180, 450]
    if type == "april24-3":
        return [100, 600, 180, 450]
    if type == "april5":
        return [60, 700, 110, 350]
    if type == "april6-4":
        return [130, 700, 110, 450]


# print(df)
