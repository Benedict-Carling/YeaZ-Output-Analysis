import pandas as pd
import matplotlib.pyplot as plt

from cell_scatter_analysis import getSubPopulationsMerged
from helper_analysis_path import CELLPATH, EXPERIMENTNAME
from helper_analysis_path import CELLDIRECTORY, FILENAME


rawdf = pd.read_pickle(CELLPATH)
df = getSubPopulationsMerged(rawdf, EXPERIMENTNAME, False)

def plotHistogram(df,axis,name,limit=False):
    plt.cla()
    plt.clf()
    if limit:
        df = df[df[axis] >= limit[0]]
        df = df[df[axis] <= limit[1]]
    plt.hist(
        df[axis], density=True, bins=250
    )  # density=False would make counts
    plt.ylabel("Probability")
    plt.xlabel(axis)
    plt.title("{} {} - No cells {}".format(FILENAME, name, len(df)))
    plt.savefig(
        "{}/{} {}.png".format(CELLDIRECTORY, FILENAME, name),
        bbox_inches="tight",
        dpi=200,
    )

# name = "whole population localisation score"
# plotHistogram(df,"score",name,[0.5,1.5])

name = "Localisation score per cell"
plotHistogram(df,"score",name,[0.5,1.5])

grouped = df.groupby("field-of-view").mean()
name = "Mean Localisation per well"
plotHistogram(grouped,"score",name)