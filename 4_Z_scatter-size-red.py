import pandas as pd
import matplotlib.pyplot as plt

from Analysis_Directory import CELLPATH

df = pd.read_pickle(CELLPATH)

# df = df[df["size"] > 60]
# df = df[df["size"] < 800]

# df = df[df["meanRedValue"] > 110]
# df = df[df["meanRedValue"] < 500]

# April5
# Low 100-310 size
# High 350-560 size

print(df)


plt.scatter(
    df["size"], df["meanRedValue"], alpha=0.003
)  # density=False would make counts
plt.ylabel("Mean Red")
plt.xlabel("Size")
plt.title("All cells size vs mean red Value")
plt.show()
