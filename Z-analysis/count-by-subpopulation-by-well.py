# data from https://allisonhorst.github.io/palmerpenguins/

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

species = [str(numeric_string) for numeric_string in list(range(1, 97))]

df = pd.read_pickle("data/mar15/cells.pkl")

df = df[df["size"] > 65]
df = df[df["size"] < 600]

df["maxLocalisation"] = df[
    ["greenBlueCorrelation1", "greenBlueCorrelation2", "greenBlueCorrelation0"]
].max(axis=1)

# lowPopulation = df[df["meanRedValue"] > 78]
# lowPopulation = lowPopulation[lowPopulation["meanRedValue"] < 93]

highPopulation = df[df["meanRedValue"] > 95]
highPopulation = highPopulation[highPopulation["meanRedValue"] < 140]


highPopulationGrouped = highPopulation.groupby("field-of-view", as_index=False).mean()

print(len(highPopulationGrouped["maxLocalisation"]))

print(highPopulationGrouped["field-of-view"].unique())
