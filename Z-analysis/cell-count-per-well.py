import pandas as pd
import matplotlib.pyplot as plt
import diptest

df = pd.read_pickle("data/mar15/cells.pkl")

df = df[df["size"] > 10]
df = df[df["size"] < 1000]


df["maxLocalisation"] = df[
    ["greenBlueCorrelation1", "greenBlueCorrelation2", "greenBlueCorrelation0"]
].max(axis=1)

# This command counts all items in the group
groupeddf = df.groupby("field-of-view").count()
print(groupeddf)

plt.hist(groupeddf["maxLocalisation"], density=True)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Number of Cells per well")

plt.show()
