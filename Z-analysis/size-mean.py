import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle("data/mar15/cells.pkl")

df = df[df["size"] > 65]
df = df[df["size"] < 600]

print(df)


plt.hist(df["size"], density=True, bins=100)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell red value")
plt.show()
