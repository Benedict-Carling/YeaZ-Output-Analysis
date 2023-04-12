import pandas as pd
import matplotlib.pyplot as plt


CELLFOLDER = "april6-6"
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

plt.bar(
    list(range(1, 193)),
    groupeddf["maxLocalisation"],
    tick_label=[str(numeric_string) for numeric_string in list(range(1, 193))],
    width=0.4,
)  # density=False would make counts
plt.ylabel("Localisation Score")
plt.xlabel("Data")
plt.xticks(rotation=90)
plt.title("Average localisation per well")

plt.show()

print(groupeddf)
