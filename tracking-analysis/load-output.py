import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df = pd.read_csv("tracking-analysis/fov1-0-30 copy.csv")

print(df)

# 1: 277 367
# 2: 185
# 2: 401 514
# 7: 344
# 8: 170 146 222

# Channel name "BF_KS" or "GFP_KS"
# df = df[df["Channel"] == "BF_KS"]
df = df[df["Time"] <= 30]
df = df[df["Cell"] != 277]
df = df[df["Cell"] != 367]

df = df[df["Area"] <= 200]

INITIAL_SIZE_LIMIT = 30

initial_present_cell_ids = df[df["Time"] == 0]["Cell"]
initial_cells = df[df["Cell"].isin(initial_present_cell_ids)]
# Getting cells who were not initially present and whose fist appearance is smaller than 20
new_cells_no_size = df[~df["Cell"].isin(initial_present_cell_ids)]
new_cells_first = new_cells_no_size.groupby(
    "Cell",
    as_index=False,
).first()
valid_new_cell_ids = new_cells_first[new_cells_first["Area"] <= INITIAL_SIZE_LIMIT][
    "Cell"
]


merged_array = []

for element in valid_new_cell_ids:
    merged_array.append(element)

# iterate through array2 and append each element to the new array
for element in initial_present_cell_ids:
    merged_array.append(element)

new_cells = df[df["Cell"].isin(merged_array)]

print(df.columns.values.tolist())

# minCells = df.groupby("Cell",as_index=False).agg(','.join)

# Value names are "Area" or "Mean"
table = pd.pivot_table(new_cells, values=["Area"], columns=["Time"], index="Cell")
nptable = np.array(table)


for row in nptable:
    if math.isnan(row[0]):
        plt.plot(row, linewidth="0.5", c="hotpink")
    else:
        plt.plot(row, linewidth="0.5", c="grey")

plt.ylabel("Mean Cell size")
plt.xlabel("Time")
plt.title("Mean cell size over time FOV 1")

plt.show()

print(df.sort_values("Area"))
