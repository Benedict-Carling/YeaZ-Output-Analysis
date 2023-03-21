import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle("feb22data.pkl")

df = df[df["size"] > 40]
df = df[df["size"] < 300]


plt.hist(df["size"], density=True, bins=250)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell red value")
plt.show()
