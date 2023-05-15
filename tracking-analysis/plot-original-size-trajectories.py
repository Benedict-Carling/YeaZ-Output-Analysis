import math
from matplotlib import pyplot as plt
import numpy as np
from clean_cells import getCleanCells


df = getCleanCells(False)

print(df)

timedf = df.pivot("Cell", "Time", "Area")
print(timedf)

nptable = np.array(timedf)


for row in nptable:
    if math.isnan(row[0]):
        plt.plot(row, linewidth="0.5", c="hotpink")
    else:
        plt.plot(row, linewidth="0.5", c="grey")

plt.ylabel("Mean Cell size")
plt.xlabel("Time")
plt.title("All Trajectories")

plt.show()
