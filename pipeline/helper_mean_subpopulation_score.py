import pandas as pd

from cell_scatter_analysis import getSubPopulationsMerged
from helper_analysis_path import CELLPATH, EXPERIMENTNAME


rawdf = pd.read_pickle(CELLPATH)
df = getSubPopulationsMerged(rawdf, EXPERIMENTNAME, False)

df["normalScore"] = df["score"] / df["meanGreenValue"]

scores = df.groupby("population").mean()

print(scores)
