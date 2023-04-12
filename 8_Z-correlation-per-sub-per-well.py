import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Analysis_Directory import CELLPATH


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

print(len(lowPopulationGrouped["maxLocalisation"]))
print(len(highPopulationGrouped["maxLocalisation"]))

species = [str(item) for item in highPopulationGrouped["image-index"].unique()]

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
