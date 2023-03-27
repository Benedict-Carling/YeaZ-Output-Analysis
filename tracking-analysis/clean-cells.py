import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

files = [
    {"site": "1&2", "name": 1, "path": "tracking-analysis/fov1-0-30 copy.csv"},
    {"site": "1&2", "name": 2, "path": "tracking-analysis/fov2-0-30 copy.csv"},
    {"site": "3&4", "name": 3, "path": "tracking-analysis/fov3-0-30 copy.csv"},
    {"site": "3&4", "name": 4, "path": "tracking-analysis/fov4-0-30 copy.csv"},
    {"site": "5&6", "name": 5, "path": "tracking-analysis/fov5-0-30 copy.csv"},
    {"site": "5&6", "name": 6, "path": "tracking-analysis/fov6-0-30 copy.csv"},
    {"site": "7&8", "name": 7, "path": "tracking-analysis/fov7-0-30 copy.csv"},
    {"site": "7&8", "name": 8, "path": "tracking-analysis/fov8-0-30 copy.csv"},
]


def getCleanCells():
    allcells = pd.DataFrame()

    for file in files:
        df = pd.read_csv(file["path"])
        # Cut in time
        df = df[df["Time"] <= 24]
        # Remove cells whose trajectory includes size over 154
        large_cells_ids = df[df["Area"] >= 155]["Cell"].unique()
        df = df[~df["Cell"].isin(large_cells_ids)]
        # Remove cells whose growth includes a jump over 24 pixels
        df["Growth"] = df.groupby("Cell")["Area"].diff()
        large_growth_ids = df[df["Growth"] >= 25]["Cell"].unique()
        df = df[~df["Cell"].isin(large_growth_ids)]
        # Remove new cells whose first appearance is greater the 40
        initial_present_cell_ids = df[df["Time"] == 0]["Cell"].unique()
        new_cells = df[~df["Cell"].isin(initial_present_cell_ids)]
        new_cells_first = new_cells.groupby(
            "Cell",
            as_index=False,
        ).first()
        non_valid_new_cells = new_cells_first[new_cells_first["Area"] >= 40]["Cell"]
        df = df[~df["Cell"].isin(non_valid_new_cells)]
        df["Name"] = file["name"]
        df["Site"] = file["site"]
        # I have realised that it works if i dont try to change it into a string, it needs to be the same type
        df = df.assign(Cell=lambda x: x.Name * 10_000 + x.Cell)
        # Comment to remove initally present cells
        initial_present_cell_ids = df[df["Time"] == 0]["Cell"].unique()
        df = df[~df["Cell"].isin(initial_present_cell_ids)]

        allcells = pd.concat([allcells, df])

    return allcells


allcells = getCleanCells()
print(allcells)

# Max Trajectories Including all trajectories
# Site - Mean
# 1&2    10.136634
# 3&4    10.292072
# 5&6    10.086124
# 7&8    10.987124
# Site - Standard Error
# 1&2    0.222511
# 3&4    0.176679
# 5&6    0.242886
# 7&8    0.240313
# max = allcells.groupby("Cell", as_index=False).max()
# bysite = max.groupby("Site").mean()
# print(bysite["Growth"])

# Max Trajectories Additional min requirement of 4 hour existance
# Site - mean
# 1&2    13.402299
# 3&4    13.097561
# 5&6    12.434783
# 7&8    14.184211
# Site - standard error
# 1&2    0.429922
# 3&4    0.419347
# 5&6    0.530196
# 7&8    0.474142
count = allcells.groupby("Cell", as_index=False).count()
too_short_ids = count[count["Time"] <= 12]["Cell"].unique()
allcells = allcells[~allcells["Cell"].isin(too_short_ids)]
max = allcells.groupby("Cell", as_index=False).max()
# bysite = max.groupby("Site").mean()
# print(bysite["Growth"])
# print(bysite.loc["1&2"]["Growth"])
print(max[max["Site"] == "1&2"]["Growth"])

fds = ttest_ind(
    max[max["Site"] == "1&2"]["Growth"],
    max[max["Site"] == "3&4"]["Growth"],
    equal_var=False,
)

print(fds)
