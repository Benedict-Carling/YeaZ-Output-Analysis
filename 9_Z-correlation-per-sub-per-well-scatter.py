import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text


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

# lowPopulationGrouped = lowPopulationGrouped[
#     lowPopulationGrouped["image-index"].isin(
#         highPopulationGrouped["image-index"].unique()
#     )
# ]

penguin_means = {
    "Low Subpopulation": lowPopulationGrouped["greenBlueCorrelation2"],
    "High Subpopulation": highPopulationGrouped["greenBlueCorrelation2"],
}

species = [str(item) for item in highPopulationGrouped["image-index"].unique()]

x = np.arange(len(species))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

plt.scatter(
    penguin_means["Low Subpopulation"], penguin_means["High Subpopulation"], alpha=0.3
)  # density=False would make counts

# for i, txt in enumerate(species):
#     plt.annotate(txt,(penguin_means["Low Subpopulation"][i],penguin_means["High Subpopulation"][i]),fontsize=6)

plt.gcf().set_size_inches(16, 9)
plt.ylabel("Low subpopulation localisation score")
plt.xlabel("High subpopulation localisation score")
plt.title(
    "Comparision of localisation per population - April 6 - 6 hour - greenBlueCorrelation2"
)
plt.axis([0.2, 0.37, 0.2, 0.37])

texts = [
    plt.text(
        penguin_means["Low Subpopulation"][i],
        penguin_means["High Subpopulation"][i],
        txt,
        fontsize="xx-small",
    )
    for i, txt in enumerate(species)
]
adjust_text(texts, arrowprops=dict(arrowstyle="-", color="k", lw=0.5))

plt.savefig("April5-hour4-2.png", dpi=200)
