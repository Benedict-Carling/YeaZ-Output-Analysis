import pandas as pd
import matplotlib.pyplot as plt


CELLFOLDER = "april6-4"
CELLPATH = "data/" + CELLFOLDER + "/cells-ssim-win7.pkl"

df = pd.read_pickle(CELLPATH)

df = df[df["size"] > 60]
df = df[df["size"] < 600]
df = df[df["meanRedValue"] < 290]
df = df[df["meanRedValue"] > 50]

# APRIL SIZE BETWEEN 60 and 600
df["maxLocalisation"] = df[
    ["greenBlueCorrelation1", "greenBlueCorrelation2", "greenBlueCorrelation0"]
].max(axis=1)

groupeddf = df.groupby("image-index").mean()

plt.hist(
    groupeddf["maxLocalisation"], density=True, bins=192
)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell size")
plt.show()

print(groupeddf)
