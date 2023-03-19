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

lowPopulation = df[df["meanRedValue"] > 78]
lowPopulation = lowPopulation[lowPopulation["meanRedValue"] < 93]

highPopulation = df[df["meanRedValue"] > 95]
highPopulation = highPopulation[highPopulation["meanRedValue"] < 122]


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

fig, ax = plt.subplots(layout="constrained")

for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    # ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel("Localisation Score")
ax.set_title("Localisation score by sub population")
ax.set_xticks(x + width, species)
plt.xticks(rotation=90)
ax.legend(loc="upper left", ncols=3)
# ax.set_ylim(0, 250)

plt.show()
