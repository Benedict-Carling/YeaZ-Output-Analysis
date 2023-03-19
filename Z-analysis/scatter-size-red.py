import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle("data/mar15/cells.pkl")

df = df[df["size"] > 65]
df = df[df["size"] < 800]

df = df[df["meanRedValue"] > 50]
df = df[df["meanRedValue"] < 150]

print(df)


plt.scatter(
    df["size"], df["meanRedValue"], alpha=0.003
)  # density=False would make counts
plt.ylabel("Mean Red")
plt.xlabel("Size")
plt.title("All cells size vs mean red Value")
plt.show()
