import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CELLFOLDER = "april5"
CELLPATH = "data/" + CELLFOLDER + "/cells-v2.0.pkl"

df = pd.read_pickle(CELLPATH)

df = df[df["size"] > 60]
df = df[df["size"] < 600]
df = df[df["meanRedValue"] < 290]
df = df[df["meanRedValue"] > 50]

df["maxLocalisation"] = df[
    ["greenBlueCorrelation1", "greenBlueCorrelation2", "greenBlueCorrelation0"]
].max(axis=1)

lowPopulation = df[df["size"] > 100]
lowPopulation = lowPopulation[lowPopulation["size"] < 310]

highPopulation = df[df["size"] > 350]
highPopulation = highPopulation[highPopulation["size"] < 560]


lowPopulationGrouped = lowPopulation.groupby("image-index", as_index=False).mean()
highPopulationGrouped = highPopulation.groupby("image-index", as_index=False).mean()

lowPopulationGrouped = lowPopulationGrouped[
    lowPopulationGrouped["image-index"].isin(
        highPopulationGrouped["image-index"].unique()
    )
]

penguin_means = {
    "Low Subpopulation": lowPopulationGrouped["maxLocalisation"],
    "High Subpopulation": highPopulationGrouped["maxLocalisation"],
}

species = [str(item) for item in highPopulationGrouped["image-index"].unique()]

x = np.arange(len(species))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

plt.scatter(
    penguin_means["High Subpopulation"], penguin_means["Low Subpopulation"], alpha=0.3
)  # density=False would make counts
plt.ylabel("Low subpopulation localisation score")
plt.xlabel("High subpopulation localisation score")
plt.title("Comparision of localisation per population")
plt.show()

