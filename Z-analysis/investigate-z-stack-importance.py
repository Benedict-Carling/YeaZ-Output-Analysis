import pandas as pd
import matplotlib.pyplot as plt
import diptest

df = pd.read_pickle("data/mar15/cells.pkl")

df = df[df["size"] > 10]
df = df[df["size"] < 1000]


df["maxLocalisation"] = df[
    ["greenBlueCorrelation1", "greenBlueCorrelation2", "greenBlueCorrelation0"]
].max(axis=1)

dip = diptest.dipstat(df["maxLocalisation"])
print(dip)

dip1 = diptest.dipstat(df["greenBlueCorrelation1"])
print(dip1)

dip2 = diptest.dipstat(df["greenBlueCorrelation2"])
print(dip2)

dip0 = diptest.dipstat(df["greenBlueCorrelation0"])
print(dip0)


# plt.hist(
#     df["maxLocalisation"], density=True, bins=300
# )  # density=False would make counts
# plt.ylabel("Probability")
# plt.xlabel("Data")
# plt.title("Max Localistation per cell")

# plt.hist(
#     df["greenBlueCorrelation0"], density=True, bins=300
# )  # density=False would make counts
# plt.ylabel("Probability")
# plt.xlabel("Data")
# plt.title("Localistaion z=-1")

# plt.hist(
#     df["greenBlueCorrelation1"], density=True, bins=300
# )  # density=False would make counts
# plt.ylabel("Probability")
# plt.xlabel("Data")
# plt.title("Localistaion z=0")

# plt.hist(
#     df["greenBlueCorrelation2"], density=True, bins=300
# )  # density=False would make counts
# plt.ylabel("Probability")
# plt.xlabel("Data")
# plt.title("Localistaion z=1")


# plt.show()
