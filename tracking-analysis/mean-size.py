import pandas as pd
import numpy as np

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
    ]
)

for file in files:
    df = pd.read_csv(file["path"])
    df = df[df["Time"] <= 24]
    initial_present_cell_ids = df[df["Time"] == 0]["Cell"]
    initial_cells = df[df["Cell"].isin(initial_present_cell_ids)]
    # Getting cells who were not initially present and whose fist appearance is smaller than 25
    new_cells_no_size = df[~df["Cell"].isin(initial_present_cell_ids)]
    new_cells_first = new_cells_no_size.groupby("Cell", as_index=False).first()
    valid_new_cell_ids = new_cells_first[new_cells_first["Area"] <= 10]["Cell"]
    new_cells = df[df["Cell"].isin(valid_new_cell_ids)]

    celldf = pd.concat(
        [
            celldf,
            pd.DataFrame(
                [
                    {
                        "site": file["site"],
                        "field-of-view": file["name"],
                        "initally-present-mean": initial_cells["Area"].mean(),
                        "new-cells-mean": new_cells["Area"].mean(),
                        "ratio": new_cells["Area"].mean()
                        / initial_cells["Area"].mean(),
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

print(celldf)
