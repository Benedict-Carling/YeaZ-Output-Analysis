import pandas as pd
import matplotlib.pyplot as plt


CELLFOLDER = "april5"
CELLPATH = "data/"+ CELLFOLDER + "/cells.pkl"

df = pd.read_pickle(CELLPATH)

# df = df[df["size"] > 60]
# df = df[df["size"] < 600]

# df = df[df["meanRedValue"] < 290]
# df = df[df["meanRedValue"] > 50]

# APRIL SIZE BETWEEN 60 and 600
# APRIL meanRedValue BETWEEN 60 and 290

print(df)


# plt.hist(df["meanRedValue"], density=True, bins=250)  # density=False would make counts
# plt.ylabel("Probability")
# plt.xlabel("Data")
# plt.title("Mean cell red value")
# plt.show()
