from get_sub_pop import getSubPopulationsMerged
from low_high_selection import addPopulationCharacterisation
from analysis_directory import CELLPATH
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text

from analysis_directory import CELLPATH
from analysis_directory import CELLDIRECTORY
from analysis_directory import FILENAME

rawdf = pd.read_pickle(CELLPATH)

df = getSubPopulationsMerged(rawdf)

lowPopulation = df[df["population"]=="low"]
highPopulation = df[df["population"]=="high"]

group_low = lowPopulation.groupby(["image-index"], as_index=False).agg(
    {"scoreMax": "mean", "cellId": "count"}
)
group_high = highPopulation.groupby(["image-index"], as_index=False).agg(
    {"scoreMax": "mean", "cellId": "count"}
)

dataframe = pd.merge(
    group_low, group_high, on="image-index", how="inner", suffixes=["_low", "_high"]
)
dataframe = dataframe[dataframe["cellId_low"] >= 10]
dataframe = dataframe[dataframe["cellId_high"] >= 10]

print(dataframe)

species = [str(item) for item in dataframe["image-index"].unique()]

print(species)

x = dataframe["scoreMax_low"]
y = dataframe["scoreMax_high"]

plt.gcf().set_size_inches(16, 9)
plt.scatter(x, y, color="steelblue", alpha=0.3)  # density=False would make counts
plt.ylabel("Low subpopulation localisation score")
plt.xlabel("High subpopulation localisation score")
plt.title("{} Cell Localisation Scores Graph: Max Localisation Ratio".format(FILENAME))

# plt.axis([1, 2.1, 1, 2.1])


# texts = [plt.text(y, z, x) for x, y, z in zip(dataframe["image-index"], x, y)]
# adjust_text(texts, arrowprops=dict(arrowstyle="-", color="k", lw=0.1))

a, b = np.polyfit(x, y, 1)
plt.plot(x, a * x + b, color="grey", linestyle="solid", linewidth=1)

plt.savefig(
    "{}/{} Cell Localisation Scores Max Localisation - Ratio Metric Labels.png".format(
        CELLDIRECTORY, FILENAME
    ),
    bbox_inches="tight",
    dpi=200,
)

# plt.savefig("April5-hour4-2.png", dpi=200)
