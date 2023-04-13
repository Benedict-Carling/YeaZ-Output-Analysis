import numpy as np
import pandas as pd

CELLFOLDER = "april5"
CELLPATH = "data/" + CELLFOLDER + "/cells.pkl"


df = pd.read_pickle(CELLPATH)
# df = df[df["size"] > 40]
# df = df[df["size"] < 300]

# new df 2434
# new df 2434

print(df[df["image-index"] == 1])
