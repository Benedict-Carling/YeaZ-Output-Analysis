import pandas as pd
import matplotlib.pyplot as plt

from Analysis_Directory import CELLPATH


df = pd.read_pickle(CELLPATH)

df = df[df["size"] > 60]
df = df[df["size"] < 600]
df = df[df["meanRedValue"] < 290]
df = df[df["meanRedValue"] > 50]

# APRIL SIZE BETWEEN 60 and 600


plt.hist(
    df["greenBlueCorrelation0"], density=True, bins=250
)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell size")
plt.show()

print(df)
