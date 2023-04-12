import pandas as pd
import matplotlib.pyplot as plt

from Analysis_Directory import CELLPATH


df = pd.read_pickle(CELLPATH)

# df = df[df["size"] > 25]
df = df[df["size"] < 600]

# APRIL SIZE BETWEEN 60 and 600


plt.hist(df["size"], density=True, bins=200)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell size")
plt.show()

print(df)
