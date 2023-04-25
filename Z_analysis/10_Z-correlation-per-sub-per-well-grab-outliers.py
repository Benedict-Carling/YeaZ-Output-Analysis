import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

EXPERIMENTNAME = "april5"
CELLPATH = "data/" + EXPERIMENTNAME + "/cells-v2.0.pkl"

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

# lowPopulationGrouped = lowPopulationGrouped[lowPopulationGrouped["maxLocalisation"] > 0.16]
# lowPopulationGrouped = lowPopulationGrouped[lowPopulationGrouped["maxLocalisation"] < 0.175]
# print(lowPopulationGrouped)

# highPopulationGrouped = highPopulationGrouped[highPopulationGrouped["maxLocalisation"] > 0.285]
# highPopulationGrouped = highPopulationGrouped[highPopulationGrouped["maxLocalisation"] < 0.295]
# print(highPopulationGrouped)

print(highPopulationGrouped.sort_values("maxLocalisation"))
