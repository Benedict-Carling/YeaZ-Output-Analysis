import numpy as np
import pandas as pd


df= pd.read_pickle("feb22data.pkl")
df= df[df["size"] > 40]
df= df[df["size"] < 300]

print(df["size"])
    