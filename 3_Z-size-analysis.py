import pandas as pd
import matplotlib.pyplot as plt


CELLFOLDER = "april5"
CELLPATH = "data/" + CELLFOLDER + "/cells-v2.0.pkl"

df = pd.read_pickle(CELLPATH)

df = df[df["size"] > 60]
df = df[df["size"] < 600]

# APRIL SIZE BETWEEN 60 and 600


plt.hist(df["size"], density=True, bins=50)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell size")
plt.show()

print(df)
