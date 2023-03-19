import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle("data/mar15/cells.pkl")

df = df[df["size"] > 10]
df = df[df["size"] < 1000]


df["maxLocalisation"] = df[
    ["greenBlueCorrelation1", "greenBlueCorrelation2", "greenBlueCorrelation0"]
].max(axis=1)

plt.hist(
    df["maxLocalisation"], density=True, bins=1000
)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell red value")
plt.show()
