import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

files = [
    {"site": "1&2", "name": "fov1", "path": "tracking-analysis/fov1-0-30 copy.csv"},
    {"site": "1&2", "name": "fov2", "path": "tracking-analysis/fov2-0-30 copy.csv"},
    {"site": "3&4", "name": "fov3", "path": "tracking-analysis/fov3-0-30 copy.csv"},
    {"site": "3&4", "name": "fov4", "path": "tracking-analysis/fov4-0-30 copy.csv"},
    {"site": "5&6", "name": "fov5", "path": "tracking-analysis/fov5-0-30 copy.csv"},
    {"site": "5&6", "name": "fov6", "path": "tracking-analysis/fov6-0-30 copy.csv"},
    {"site": "7&8", "name": "fov7", "path": "tracking-analysis/fov7-0-30 copy.csv"},
    {"site": "7&8", "name": "fov8", "path": "tracking-analysis/fov8-0-30 copy.csv"},
]

allcells = pd.DataFrame()

for file in files:
    df = pd.read_csv(file["path"])
    df = df[df["Time"] <= 24]
    allcells = pd.concat(
        [allcells, df],
        ignore_index=True,
    )

print(allcells)
print(allcells[allcells["Area"] >= 154])

plt.hist(df["Area"], density=True, bins=400)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell red value")
plt.show()

# Learning things over 154 are likely not cells there are 963 / 50683 over 154 ~2%.

plt.hist(df["Area"], density=True, bins=400)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell red value")
plt.show()
