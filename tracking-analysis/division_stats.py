import math
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from clean_cells import getCleanCells

DIVISION_DEFINITION = 45

newdf = getCleanCells(True,False)

newdf["Growth"] = newdf.groupby("Cell")["Area"].diff()

totalcounts = newdf.groupby("Site").count()
totalcounts["Number of 5 min events"] = totalcounts[["Time"]]
totalcounts = totalcounts[["Number of 5 min events"]]

totalcounts["division Number"] = newdf.groupby("Site")["Growth"].apply(lambda x: (x+1 < -DIVISION_DEFINITION).sum())

totalcounts["divions per 90 mins"] = (totalcounts["division Number"] / totalcounts["Number of 5 min events"]) * 18

totalcounts = totalcounts.rename(index=dict(zip(["CTRL","GLN","PRO"],["CTRL-new","GLN-new","PRO-new"])))

olddf = getCleanCells(False,True)

olddf["Growth"] = olddf.groupby("Cell")["Area"].diff()

totalcounts_old = olddf.groupby("Site").count()
totalcounts_old["Number of 5 min events"] = totalcounts_old[["Time"]]
totalcounts_old = totalcounts_old[["Number of 5 min events"]]

totalcounts_old["division Number"] = olddf.groupby("Site")["Growth"].apply(lambda x: (x < -DIVISION_DEFINITION).sum())

totalcounts_old["divions per 90 mins"] = (totalcounts_old["division Number"] / totalcounts_old["Number of 5 min events"]) * 18

totalcounts_old = totalcounts_old.rename(index=dict(zip(["CTRL","GLN","PRO"],["CTRL-old","GLN-old","PRO-old"])))

totalcounts = pd.concat([totalcounts,totalcounts_old])

print(totalcounts)
