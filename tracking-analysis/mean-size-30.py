import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

celldf = pd.DataFrame(
    columns=["field-of-view", "initally-present-mean", "new-cells-mean", "ratio"]
)

# Fov 1

fov1 = pd.read_csv("tracking-analysis/fov1-0-30 copy.csv")

fov1 = fov1[fov1["Time"] <= 24]

initalPresent = fov1[fov1["Time"] == 0]["Cell"]

initalCells24 = fov1[fov1["Cell"].isin(initalPresent)]
otherCells24 = fov1[~fov1["Cell"].isin(initalPresent)]

celldf = pd.concat(
    [
        celldf,
        pd.DataFrame(
            [
                {
                    "field-of-view": 1,
                    "initally-present-mean": initalCells24["Area"].mean(),
                    "new-cells-mean": otherCells24["Area"].mean(),
                    "ratio": otherCells24["Area"].mean() / initalCells24["Area"].mean(),
                }
            ]
        ),
    ],
    ignore_index=True,
)

# Fov 2

fov2 = pd.read_csv("tracking-analysis/fov2-0-30 copy.csv")

fov2 = fov2[fov2["Time"] <= 24]

initalPresent = fov2[fov2["Time"] == 0]["Cell"]

initalCells24 = fov2[fov2["Cell"].isin(initalPresent)]
otherCells24 = fov2[~fov2["Cell"].isin(initalPresent)]

celldf = pd.concat(
    [
        celldf,
        pd.DataFrame(
            [
                {
                    "field-of-view": 2,
                    "initally-present-mean": initalCells24["Area"].mean(),
                    "new-cells-mean": otherCells24["Area"].mean(),
                    "ratio": otherCells24["Area"].mean() / initalCells24["Area"].mean(),
                }
            ]
        ),
    ],
    ignore_index=True,
)

# Fov 3

fov3 = pd.read_csv("tracking-analysis/fov3-0-30 copy.csv")

fov3 = fov3[fov3["Time"] <= 24]

initalPresent = fov3[fov3["Time"] == 0]["Cell"]

initalCells24 = fov3[fov3["Cell"].isin(initalPresent)]
otherCells24 = fov3[~fov3["Cell"].isin(initalPresent)]

celldf = pd.concat(
    [
        celldf,
        pd.DataFrame(
            [
                {
                    "field-of-view": 3,
                    "initally-present-mean": initalCells24["Area"].mean(),
                    "new-cells-mean": otherCells24["Area"].mean(),
                    "ratio": otherCells24["Area"].mean() / initalCells24["Area"].mean(),
                }
            ]
        ),
    ],
    ignore_index=True,
)

# Fov 4

fov4 = pd.read_csv("tracking-analysis/fov4-0-30 copy.csv")

fov4 = fov4[fov4["Time"] <= 24]

initalPresent = fov4[fov4["Time"] == 0]["Cell"]

initalCells24 = fov4[fov4["Cell"].isin(initalPresent)]
otherCells24 = fov4[~fov4["Cell"].isin(initalPresent)]

celldf = pd.concat(
    [
        celldf,
        pd.DataFrame(
            [
                {
                    "field-of-view": 4,
                    "initally-present-mean": initalCells24["Area"].mean(),
                    "new-cells-mean": otherCells24["Area"].mean(),
                    "ratio": otherCells24["Area"].mean() / initalCells24["Area"].mean(),
                }
            ]
        ),
    ],
    ignore_index=True,
)

# Fov 5

fov5 = pd.read_csv("tracking-analysis/fov5-0-30 copy.csv")

fov5 = fov5[fov5["Time"] <= 24]

initalPresent = fov5[fov5["Time"] == 0]["Cell"]


initalCells24 = fov5[fov5["Cell"].isin(initalPresent)]
otherCells24 = fov5[~fov5["Cell"].isin(initalPresent)]

celldf = pd.concat(
    [
        celldf,
        pd.DataFrame(
            [
                {
                    "field-of-view": 5,
                    "initally-present-mean": initalCells24["Area"].mean(),
                    "new-cells-mean": otherCells24["Area"].mean(),
                    "ratio": otherCells24["Area"].mean() / initalCells24["Area"].mean(),
                }
            ]
        ),
    ],
    ignore_index=True,
)

# Fov 6

fov6 = pd.read_csv("tracking-analysis/fov6-0-30 copy.csv")

fov6 = fov6[fov6["Time"] <= 24]

initalPresent = fov6[fov6["Time"] == 0]["Cell"]


initalCells24 = fov6[fov6["Cell"].isin(initalPresent)]
otherCells24 = fov6[~fov6["Cell"].isin(initalPresent)]

celldf = pd.concat(
    [
        celldf,
        pd.DataFrame(
            [
                {
                    "field-of-view": 6,
                    "initally-present-mean": initalCells24["Area"].mean(),
                    "new-cells-mean": otherCells24["Area"].mean(),
                    "ratio": otherCells24["Area"].mean() / initalCells24["Area"].mean(),
                }
            ]
        ),
    ],
    ignore_index=True,
)

# Fov 7

fov7 = pd.read_csv("tracking-analysis/fov7-0-30 copy.csv")

fov7 = fov7[fov7["Time"] <= 24]

initalPresent = fov7[fov7["Time"] == 0]["Cell"]

initalCells24 = fov7[fov7["Cell"].isin(initalPresent)]
otherCells24 = fov7[~fov7["Cell"].isin(initalPresent)]

celldf = pd.concat(
    [
        celldf,
        pd.DataFrame(
            [
                {
                    "field-of-view": 7,
                    "initally-present-mean": initalCells24["Area"].mean(),
                    "new-cells-mean": otherCells24["Area"].mean(),
                    "ratio": otherCells24["Area"].mean() / initalCells24["Area"].mean(),
                }
            ]
        ),
    ],
    ignore_index=True,
)

# Fov 8

fov8 = pd.read_csv("tracking-analysis/fov8-0-30 copy.csv")

fov8 = fov8[fov8["Time"] <= 24]

initalPresent = fov8[fov8["Time"] == 0]["Cell"]

initalCells24 = fov8[fov8["Cell"].isin(initalPresent)]
otherCells24 = fov8[~fov8["Cell"].isin(initalPresent)]

celldf = pd.concat(
    [
        celldf,
        pd.DataFrame(
            [
                {
                    "field-of-view": 8,
                    "initally-present-mean": initalCells24["Area"].mean(),
                    "new-cells-mean": otherCells24["Area"].mean(),
                    "ratio": otherCells24["Area"].mean() / initalCells24["Area"].mean(),
                }
            ]
        ),
    ],
    ignore_index=True,
)

print(celldf)
