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


def Limitdf(
    df,
    type: Literal[
        "april5",
        "april6-4",
        "april24-2",
        "april24-3",
        "20230503_205612_083",
        "20230503_203021_220",
    ],
):
    limits = getAxisLimit(type)
    df = df[df["size"] > limits[0]]
    df = df[df["size"] < limits[1]]
    df = df[df["meanRedValue"] > limits[2]]
    df = df[df["meanRedValue"] < limits[3]]
    return df


def getAxisLimit(
    type: Literal[
        "april5",
        "april6-4",
        "april24-2",
        "april24-3",
        "april6-2",
        "20230503_205612_083",
        "20230503_203021_220",
        "20230503_195034_753",
        "20230503_192438_458",
        "20230503_184638_666",
        "20230503_181027_601",
        "20230503_174429_594",
        "20230503_171604_196",
    ]
):
    if type == "april24-2":
        return [100, 600, 180, 450]
    if type == "april24-3":
        return [100, 600, 180, 450]
    if type == "april5":
        return [60, 700, 110, 350]
    if type == "april6-4":
        return [130, 700, 110, 450]
    if type == "april6-2":
        return [130, 700, 110, 350]
    if type == "20230503_205612_083":
        return [100, 630, 140, 260]
    if type == "20230503_203021_220":
        return [100, 560, 140, 260]
    if type == "20230503_195034_753":
        return [100, 620, 140, 290]
    if type == "20230503_192438_458":
        return [150, 580, 170, 280]
    if type == "20230503_184638_666":
        return [130, 580, 170, 370]
    if type == "20230503_181027_601":
        return [130, 580, 170, 370]
    if type == "20230503_174429_594":
        return [130, 580, 170, 370]
    if type == "20230503_171604_196":
        return [130, 580, 170, 370]


# print(df)
