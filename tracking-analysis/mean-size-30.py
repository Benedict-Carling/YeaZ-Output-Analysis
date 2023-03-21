import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

celldf = pd.DataFrame(
    columns=[
        "field-of-view",
        "initally-present-mean",
        "new-cells-mean",
    ]
)

fov1 = pd.read_csv("tracking-analysis/fov8-0-30 copy.csv")

fov1 = fov1[fov1["Time"] <= 30]

initalPresent = fov1[fov1["Time"] == 0]["Cell"]

allCells30 = fov1[fov1["Time"] == 30]

initalCells30 = allCells30[allCells30["Cell"].isin(initalPresent)]
otherCells30 = allCells30[~allCells30["Cell"].isin(initalPresent)]

celldf

celldf = pd.concat(
    [
        celldf,
        pd.DataFrame(
            [
                {
                    "field-of-view": 1,
                    "initally-present-mean": initalCells30["Area"].mean(),
                    "new-cells-mean": otherCells30["Area"].mean(),
                }
            ]
        ),
    ],
    ignore_index=True,
)
