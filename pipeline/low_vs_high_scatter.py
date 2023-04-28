from typing import Literal
from cell_scatter_analysis import getSubPopulationsMerged
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text

from helper_analysis_path import EXPERIMENTNAME
from helper_analysis_path import CELLPATH
from helper_analysis_path import CELLDIRECTORY
from helper_analysis_path import FILENAME

rawdf = pd.read_pickle(CELLPATH)
df = getSubPopulationsMerged(rawdf, EXPERIMENTNAME)

lowPopulation = df[df["population"] == "low"]
highPopulation = df[df["population"] == "high"]

group_low = lowPopulation.groupby(["field-of-view"], as_index=False).agg(
    {"score": "mean", "cellId": "count"}
)
group_high = highPopulation.groupby(["field-of-view"], as_index=False).agg(
    {"score": "mean", "cellId": "count"}
)

dataframe = pd.merge(
    group_low, group_high, on="field-of-view", how="inner", suffixes=["_low", "_high"]
)
dataframe = dataframe[dataframe["cellId_low"] >= 3]
dataframe = dataframe[dataframe["cellId_high"] >= 3]

species = [str(item) for item in dataframe["field-of-view"].unique()]

y = dataframe["score_low"]
x = dataframe["score_high"]

plt.cla()
plt.clf()
plt.gcf().set_size_inches(16, 9)
plt.scatter(x, y, color="steelblue", alpha=0.3)  # density=False would make counts
plt.ylabel("Low subpopulation localisation score")
plt.xlabel("High subpopulation localisation score")
plt.title("{} Cell Localisation Scores Graph: Max Localisation Ratio".format(FILENAME))


def getScoreAxis(type: Literal["april5", "april6-4", "april23-2", "april23-3"]):
    if type == "april5":
        return [1, 2.1, 1, 2.1]
    if type == "april6-4":
        return [1, 1.8, 1, 1.8]
    if type == "april23-2":
        return [1, 1.8, 1, 1.8]
    if type == "april23-3":
        return [1, 1.8, 1, 1.8]


plt.axis(getScoreAxis(EXPERIMENTNAME))
# texts = [plt.text(y, z, x) for x, y, z in zip(dataframe["field-of-view"], x, y)]
# adjust_text(texts, arrowprops=dict(arrowstyle="-", color="k", lw=0.1))

a, b = np.polyfit(x, y, 1)
plt.plot(x, a * x + b, color="grey", linestyle="solid", linewidth=1)

plt.savefig(
    "{}/{} Cell Localisation Scores Ratio Localisation.png".format(
        CELLDIRECTORY, FILENAME
    ),
    bbox_inches="tight",
    dpi=200,
)

# plt.savefig("April5-hour4-2.png", dpi=200)
