import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle("data/mar15/cells.pkl")

df = df[df["size"] > 65]
df = df[df["size"] < 600]

df = df[df["meanRedValue"] > 50]
df = df[df["meanRedValue"] < 150]

df = df[df["field-of-view"] == 7]

print(df)

plt.hist(df["meanRedValue"], density=True, bins=50)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell red value")
plt.show()
