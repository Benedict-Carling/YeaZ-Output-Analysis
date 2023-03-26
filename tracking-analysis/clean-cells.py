import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        initial_present_cell_ids = df[df["Time"] == 0]["Cell"]
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
max = allcells.groupby("Cell", as_index=False).max()
bysite = max.groupby("Site").mean()
print(bysite["Growth"])

# Max Trajectories Additional min requirement of 4 hour existance
# Site - mean
# 1&2     9.937500
# 3&4    10.053097
# 5&6    10.254601
# 7&8    11.109589
# Site - standard error
# 1&2    0.214957
# 3&4    0.177859
# 5&6    0.245927
# 7&8    0.232883
count = allcells.groupby("Cell", as_index=False).count()
too_short_ids = count[count["Time"] <= 12]["Cell"].unique()
allcells = allcells[~allcells["Cell"].isin(too_short_ids)]
max = allcells.groupby("Cell", as_index=False).nth(5)
print(max)
