import pandas as pd
import matplotlib.pyplot as plt


CELLFOLDER = "april5"
CELLPATH = "data/" + CELLFOLDER + "/cells-v2.0.pkl"

df = pd.read_pickle(CELLPATH)

df = df[df["meanRedValue"] < 290]
df = df[df["meanRedValue"] > 70]

# APRIL meanRedValue BETWEEN 70 and 290

plt.hist(df["meanRedValue"], density=True, bins=250)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell red value - April 5th NLIM Proline 4hours")
plt.show()

print(df)
