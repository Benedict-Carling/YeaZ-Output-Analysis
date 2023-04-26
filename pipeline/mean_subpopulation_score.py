import pandas as pd

from cell_scatter_analysis import getSubPopulationsMerged
from analysis_path import CELLPATH, EXPERIMENTNAME


rawdf = pd.read_pickle(CELLPATH)
df = getSubPopulationsMerged(rawdf, EXPERIMENTNAME, False)

df["normalScore"] = df["nuc_scoreMax"] / df["meanRedValue"]

scores = df.groupby("population").mean()

print(scores)