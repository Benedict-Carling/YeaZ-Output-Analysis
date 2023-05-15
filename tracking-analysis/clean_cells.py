import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from timelapse_path import CELLDIRECTORY

files = [
    {"site": "PRO", "name": 1, "path": "1.csv"},
    {"site": "PRO", "name": 2, "path": "2.csv"},
    {"site": "PRO", "name": 3, "path": "3.csv"},
    {"site": "PRO", "name": 4, "path": "4.csv"},
    {"site": "PRO", "name": 5, "path": "5.csv"},
    {"site": "PRO", "name": 6, "path": "6.csv"},
    {"site": "PRO", "name": 7, "path": "7.csv"},
    {"site": "PRO", "name": 8, "path": "8.csv"},
    {"site": "GLN", "name": 9, "path": "9.csv"},
    {"site": "GLN", "name": 10, "path": "10.csv"},
    {"site": "GLN", "name": 11, "path": "11.csv"},
    {"site": "GLN", "name": 12, "path": "12.csv"},
    {"site": "GLN", "name": 13, "path": "13.csv"},
    {"site": "GLN", "name": 14, "path": "14.csv"},
    {"site": "GLN", "name": 15, "path": "15.csv"},
    {"site": "GLN", "name": 16, "path": "16.csv"},
    {"site": "CTRL", "name": 17, "path": "17.csv"},
    {"site": "CTRL", "name": 18, "path": "18.csv"},
    {"site": "CTRL", "name": 19, "path": "19.csv"},
    {"site": "CTRL", "name": 20, "path": "20.csv"},
    {"site": "CTRL", "name": 21, "path": "21.csv"},
    {"site": "CTRL", "name": 22, "path": "22.csv"},
]


def getCleanCells(newOnly: bool = False, oldOnly: bool = False):
    allcells = pd.DataFrame()

    for file in files:
        df = pd.read_csv(CELLDIRECTORY + file["path"])
        df["Name"] = file["name"]
        df["Site"] = file["site"]
        # Cut in time
        df = df[df["Time"] <= 72]
        # Remove cells whose trajectory includes size over 154
        large_cells_ids = df[df["Area"] >= 1050]["Cell"].unique()
        df = df[~df["Cell"].isin(large_cells_ids)]
        # Remove cells whose growth includes a jump over 24 pixels
        df["Growth"] = df.groupby("Cell")["Area"].diff()
        large_growth_ids = df[df["Growth"] >= 220]["Cell"].unique()
        df = df[~df["Cell"].isin(large_growth_ids)]
        # # Remove new cells whose first appearance is greater the 40 (150)
        initial_present_cell_ids = df[df["Time"] == 0]["Cell"].unique()
        new_cells = df[~df["Cell"].isin(initial_present_cell_ids)]
        new_cells_first = new_cells.groupby(
            "Cell",
            as_index=False,
        ).first()
        non_valid_new_cells = new_cells_first[new_cells_first["Area"] >= 200]["Cell"]
        df = df[~df["Cell"].isin(non_valid_new_cells)]
        # I have realised that it works if i dont try to change it into a string, it needs to be the same type
        df = df.assign(Cell=lambda x: x.Name * 10_000 + x.Cell)
        # Remove cells if they have dissapered within 2 hours of appearing
        # disappearedWithTimeCount = df.groupby(["Cell"], as_index=False).agg(
        #     {"Time": "count", "Disappeared in video": "any"}
        # )
        # disappeared = disappearedWithTimeCount[
        #     disappearedWithTimeCount["Disappeared in video"] == True
        # ]
        # disappearIds = disappeared["Cell"]
        # df = df[~df["Cell"].isin(disappearIds)]
        # Comment to remove initally present cells
        if newOnly:
            initial_present_cell_ids = df[df["Time"] == 0]["Cell"].unique()
            df = df[~df["Cell"].isin(initial_present_cell_ids)]
        
        if oldOnly:
            initial_present_cell_ids = df[df["Time"] == 0]["Cell"].unique()
            df = df[df["Cell"].isin(initial_present_cell_ids)]

        allcells = pd.concat([allcells, df])

    return allcells


# Divisions Estimate
# table = pd.pivot_table(allcells, values=["Area"], columns=["Time"], index="Cell")
# print(table["0"])

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
# bysite = max.groupby("Site").agg({"Growth":["mean","sem","count"]})
# print(bysite)

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
# count = allcells.groupby("Cell", as_index=False).count()
# too_short_ids = count[count["Time"] <= 12]["Cell"].unique()
# allcells = allcells[~allcells["Cell"].isin(too_short_ids)]
# max = allcells.groupby("Cell", as_index=False).max()
# bysite = max.groupby("Site").agg({"Growth":["mean","sem","count"]})
# print(bysite)
# print(bysite.loc["1&2"]["Growth"])
# print(max[max["Site"] == "1&2"]["Growth"])

# fds = ttest_ind(
#     max[max["Site"] == "1&2"]["Growth"],
#     max[max["Site"] == "3&4"]["Growth"],
#     equal_var=False,
# )

# Total Growth Graph
# data = pd.DataFrame()
# cells12 = allcells[allcells["Site"] == "1&2"]
# table = pd.pivot_table(cells12, values=["Area"], columns=["Time"], index="Cell")
# table = table.apply(lambda x: sorted(x, key=pd.isnull), 1)
# fdsa = np.array(table)
# dataframe12 = pd.DataFrame(list(map(np.ravel, fdsa)))
# cells34 = allcells[allcells["Site"] == "3&4"]
# table = pd.pivot_table(cells34, values=["Area"], columns=["Time"], index="Cell")
# table = table.apply(lambda x: sorted(x, key=pd.isnull), 1)
# fdsa = np.array(table)
# dataframe34 = pd.DataFrame(list(map(np.ravel, fdsa)))
# cells56 = allcells[allcells["Site"] == "5&6"]
# table = pd.pivot_table(cells56, values=["Area"], columns=["Time"], index="Cell")
# table = table.apply(lambda x: sorted(x, key=pd.isnull), 1)
# fdsa = np.array(table)
# dataframe56 = pd.DataFrame(list(map(np.ravel, fdsa)))
# cells78 = allcells[allcells["Site"] == "7&8"]
# table = pd.pivot_table(cells78, values=["Area"], columns=["Time"], index="Cell")
# print(table)
# table = table.apply(lambda x: sorted(x, key=pd.isnull), 1)
# fdsa = np.array(table)
# print(fdsa)
# dataframe78 = pd.DataFrame(list(map(np.ravel, fdsa)))
# # print(pd.concat([dataframe78.mean(),dataframe78.count()]))
# print(dataframe78.groupby(axis=0,level=-1).mean())
# plt.plot(dataframe12.count(), linewidth="0.5", label ='1&2')
# plt.plot(dataframe34.count(), linewidth="0.5", label ='3&4')
# plt.plot(dataframe56.count(), linewidth="0.5", label ='5&6')
# plt.plot(dataframe78.count(), linewidth="0.5", label ='7&8')
# plt.ylabel("Mean Cell size")
# plt.xlabel("Time (20 mins intervals) after first appearance")
# plt.legend()
# plt.title("Mean cell size at each age of cell")
# plt.show()
