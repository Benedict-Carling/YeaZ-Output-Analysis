# data from https://allisonhorst.github.io/palmerpenguins/

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_pickle("data/mar15/cells.pkl")

df = df[df["size"] > 65]
df = df[df["size"] < 600]

df["maxLocalisation"] = df[
    ["greenBlueCorrelation1", "greenBlueCorrelation2", "greenBlueCorrelation0"]
].max(axis=1)

lowPopulation = df[df["meanRedValue"] > 76]
lowPopulation = lowPopulation[lowPopulation["meanRedValue"] < 94]

highPopulation = df[df["meanRedValue"] > 94]
highPopulation = highPopulation[highPopulation["meanRedValue"] < 125]


lowPopulationGrouped = lowPopulation.groupby("field-of-view", as_index=False).mean()
highPopulationGrouped = highPopulation.groupby("field-of-view", as_index=False).mean()

lowPopulationGrouped = lowPopulationGrouped[
    lowPopulationGrouped["field-of-view"].isin(
        highPopulationGrouped["field-of-view"].unique()
    )
]

penguin_means = {
    "Low Subpopulation": lowPopulationGrouped["maxLocalisation"],
    "High Subpopulation": highPopulationGrouped["maxLocalisation"],
}

print(len(lowPopulationGrouped["maxLocalisation"]))
print(len(highPopulationGrouped["maxLocalisation"]))

species = [str(item) for item in highPopulationGrouped["field-of-view"].unique()]

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
