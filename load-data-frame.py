import numpy as np
import pandas as pd

CELLFOLDER = "april5"
CELLPATH = "data/" + CELLFOLDER + "/cells.pkl"


df = pd.read_pickle(CELLPATH)
df = df[df["size"] > 40]
df = df[df["size"] < 300]

print(df["size"])
