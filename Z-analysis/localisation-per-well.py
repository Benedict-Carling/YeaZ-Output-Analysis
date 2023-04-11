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
groupeddf = df.groupby("field-of-view").mean()
print(groupeddf)

plt.bar(
    list(range(1, 97)),
    groupeddf["maxLocalisation"],
    tick_label=[str(numeric_string) for numeric_string in list(range(1, 97))],
    width=0.4,
)  # density=False would make counts
plt.ylabel("Localisation Score")
plt.xlabel("Data")
plt.xticks(rotation=90)
plt.title("Average localisation per well")

plt.show()
