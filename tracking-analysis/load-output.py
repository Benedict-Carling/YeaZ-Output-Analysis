import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df = pd.read_csv('tracking-analysis/fov2-0-30.csv')

print(df)

# Channel name "BF_KS" or "GFP_KS"
# df = df[df["Channel"] == "BF_KS"]
df = df[df["Time"] <= 30]
# df = df[df["Area"] <= 250]
print(df.columns.values.tolist())

# minCells = df.groupby("Cell",as_index=False).agg(','.join)

# Value names are "Area" or "Mean"
table = pd.pivot_table(df,values=["Area"],columns=["Time"],index="Cell")
nptable = np.array(table)
print(nptable)

for row in nptable:
    if (math.isnan(row[0])):
        plt.plot(row, linewidth = '0.5', c = 'hotpink')
    else:
        plt.plot(row, linewidth = '0.5', c = "grey")

plt.ylabel('Mean Cell size')
plt.xlabel('Time');
plt.title("Mean cell size over time FOV 2")

plt.show()