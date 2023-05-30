import math
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from clean_cells import getCleanCells


newdf = getCleanCells(newOnly = False,oldOnly = False)
newdf["Growth"] = newdf.groupby("Cell")["Area"].diff()

prodf = newdf[newdf["Site"] == "PRO"]
protable = pd.pivot_table(prodf, values=["Growth"], columns=["Time"], index="Cell")
protable.to_csv("GROWTH-pro-data-april-12.csv")
print(protable)

glndf = newdf[newdf["Site"] == "GLN"]
glntable = pd.pivot_table(glndf, values=["Growth"], columns=["Time"], index="Cell")
glntable.to_csv("GROWTH-gln-data-april-12.csv")
print(glntable)

CTRLdf = newdf[newdf["Site"] == "CTRL"]
CTRLtable = pd.pivot_table(CTRLdf, values=["Growth"], columns=["Time"], index="Cell")
CTRLtable.to_csv("GROWTH-control-data-april-12.csv")
print(CTRLtable)

nptable = np.array(glntable)


for row in nptable:
    if math.isnan(row[0]):
        plt.plot(row, linewidth="0.5", c="hotpink")
    else:
        plt.plot(row, linewidth="0.5", c="grey")

plt.ylabel("Mean Cell size")
plt.xlabel("Time")
plt.title("Mean cell size over time FOV 1")

plt.show()


