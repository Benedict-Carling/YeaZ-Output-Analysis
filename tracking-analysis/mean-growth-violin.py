import pandas as pd
import numpy as np
import seaborn as sns
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

celldf = pd.DataFrame(
    columns=[
        "site",
        "field-of-view",
        "initally-present-mean",
        "new-cells-mean",
        "ratio",
        "growth",
    ]
)

GROWTH_LIMIT = 40

for file in files:
    df = pd.read_csv(file["path"])
    df = df[df["Time"] <= 24]
    initial_present_cell_ids = df[df["Time"] == 0]["Cell"]
    initial_cells = df[df["Cell"].isin(initial_present_cell_ids)]
    # Getting cells who were not initially present and whose fist appearance is smaller than 20
    new_cells_no_size = df[~df["Cell"].isin(initial_present_cell_ids)]
    new_cells_first = new_cells_no_size.groupby(
        "Cell",
        as_index=False,
    ).first()
    valid_new_cell_ids = new_cells_first[new_cells_first["Area"] <= GROWTH_LIMIT][
        "Cell"
    ]
    new_cells = df[df["Cell"].isin(valid_new_cell_ids)]

    growth = new_cells.groupby("Cell")["Area"].diff()

    celldf = pd.concat(
        [
            celldf,
            pd.DataFrame(
                [
                    {
                        "site": file["site"],
                        "field-of-view": file["name"],
                        "initally-present-mean": initial_cells["Area"],
                        "new-cells-mean": new_cells["Area"],
                        "growth": growth,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )




print(celldf.iloc[0]["growth"])
print(celldf.iloc[1]["growth"])

growth12 = np.array(pd.concat([celldf.iloc[0]["growth"], celldf.iloc[1]["growth"]]))
growth1_2 = growth12[~np.isnan(growth12)]
growth34 = np.array(pd.concat([celldf.iloc[2]["growth"], celldf.iloc[3]["growth"]]))
growth3_4 = growth34[~np.isnan(growth34)]

growth56 = np.array(pd.concat([celldf.iloc[4]["growth"], celldf.iloc[5]["growth"]]))
growth5_6 = growth56[~np.isnan(growth56)]

growth78 = np.array(pd.concat([celldf.iloc[6]["growth"], celldf.iloc[7]["growth"]]))
growth7_8 = growth78[~np.isnan(growth78)]


growthArray = [growth1_2, growth3_4, growth5_6, growth7_8]


metricdf = pd.concat(
    [
        pd.DataFrame([{"field-of-view": 1, "growth": growth12}]),
        pd.DataFrame([{"field-of-view": 2, "growth": growth34}]),
        pd.DataFrame([{"field-of-view": 3, "growth": growth56}]),
        pd.DataFrame([{"field-of-view": 4, "growth": growth78}]),
    ]
)

print(len(growthArray))
print(len([1, 2, 3, 4]))

print("Including new cell that appear with size less than", GROWTH_LIMIT)
print("mean new cell growth fov1&2: ", growth12.mean())
print("mean new cell growth fov3&4: ", growth34.mean())
print("mean new cell growth fov5&6: ", growth56.mean())
print("mean new cell growth fov7&8: ", growth78.mean())

# fig, ax = plt.subplots()

# vp = ax.violinplot(
#     growthArray,
#     [1, 2, 3, 4],
#     points=500,
#     widths=0.7,
#     showmeans=True,
#     showmedians=False,
#     showextrema=False,
#     bw_method=0.05,
# )
# # styling:
# for body in vp["bodies"]:
#     body.set_alpha(0.9)
# ax.set(ylim=(0, 14), yticks=np.arange(0, 15))
# plt.ylabel("Mean cell growth rate")
# plt.xlabel("Location")
# plt.title("Mean cell growth rate per location")

# plt.show()
