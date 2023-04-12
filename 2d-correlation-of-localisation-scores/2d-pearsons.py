import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text
from scipy import signal

CELLFOLDER = "april5"
CELLPATH = "data/" + CELLFOLDER + "/cells-ssim-win7.pkl"

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


cor01 = np.corrcoef(highPopulationGrouped["greenBlueCorrelation0"], highPopulationGrouped["greenBlueCorrelation1"])[0][1]
cor02 = np.corrcoef(highPopulationGrouped["greenBlueCorrelation0"], highPopulationGrouped["greenBlueCorrelation2"])[0][1]
cor12 = np.corrcoef(highPopulationGrouped["greenBlueCorrelation1"], highPopulationGrouped["greenBlueCorrelation2"])[0][1]
cor0max = np.corrcoef(highPopulationGrouped["greenBlueCorrelation0"], highPopulationGrouped["maxLocalisation"])[0][1]
cor1max = np.corrcoef(highPopulationGrouped["greenBlueCorrelation1"], highPopulationGrouped["maxLocalisation"])[0][1]
cor2max = np.corrcoef(highPopulationGrouped["greenBlueCorrelation2"], highPopulationGrouped["maxLocalisation"])[0][1]

print("01",cor01)
print("02",cor02)
print("12",cor12)
print("0max",cor0max)
print("1max",cor1max)
print("2max",cor2max)

cor01 = np.corrcoef(df["greenBlueCorrelation0"], df["greenBlueCorrelation1"])[0][1]
cor02 = np.corrcoef(df["greenBlueCorrelation0"], df["greenBlueCorrelation2"])[0][1]
cor12 = np.corrcoef(df["greenBlueCorrelation1"], df["greenBlueCorrelation2"])[0][1]
cor0max = np.corrcoef(df["greenBlueCorrelation0"], df["maxLocalisation"])[0][1]
cor1max = np.corrcoef(df["greenBlueCorrelation1"], df["maxLocalisation"])[0][1]
cor2max = np.corrcoef(df["greenBlueCorrelation2"], df["maxLocalisation"])[0][1]

print("01",cor01)
print("02",cor02)
print("12",cor12)
print("0max",cor0max)
print("1max",cor1max)
print("2max",cor2max)

# April 6

# Grouped

# 01 0.9781701486664647
# 02 0.9480376441408361
# 12 0.9833829127866682
# 0max 0.9954390402881967
# 1max 0.9908163533641455
# 2max 0.9685748086375073

# Individual

# 01 0.8220933909983832
# 02 0.8012736787691512
# 12 0.8189534045321194
# 0max 0.9382053325002091
# 1max 0.9070860002640966
# 2max 0.8813224362264248

# High subpopulation
#       0                       1                   2       
#   0
#   1   0.9816416016371652
#   2   0.9503032287999555      0.98566524962276
#   max 0.9905227292518008      0.9923281414213694  0.9781103667209265