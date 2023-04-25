from typing import Literal
import pandas as pd
import matplotlib.pyplot as plt

from analysis_directory import CELLPATH
from analysis_directory import CELLDIRECTORY
from analysis_directory import FILENAME
from scipy.spatial.distance import cdist


df = pd.read_pickle(CELLPATH)

# df = df[df["size"] > 120]
# df = df[df["size"] < 700]

# df = df[df["meanRedValue"] > 110]
# df = df[df["meanRedValue"] < 450]

# April5 4 hours NLIM
# Low 100-310 size
# High 350-560 size

# April 6 4 hour GLN
# Size 120 - 700
# Red 110 - 450

def Limitdf(df,type: Literal["april5","april6-4"]):
    if type=="april6-4":
        df = df[df["size"] > 120]
        df = df[df["size"] < 700]
        df = df[df["meanRedValue"] > 110]
        df = df[df["meanRedValue"] < 450]
    return df

# print(df)

# plt.scatter(
#     df["size"], df["meanRedValue"], alpha=0.003
# )  # density=False would make counts
# plt.axis([120, 700, 110, 450])
# plt.gcf().set_size_inches(16, 9)
# plt.ylabel("Mean Red")
# plt.xlabel("Size")
# plt.title("{} Cell Scatter Graph - No cells {}".format(FILENAME, len(df)))
# plt.savefig(
#     "{}/{} Cell Scatter Graph.png".format(CELLDIRECTORY, FILENAME),
#     bbox_inches="tight",
#     dpi=200,
# )
