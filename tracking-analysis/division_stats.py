import math
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from clean_cells import getCleanCells

DIVISION_DEFINITION_TOP = -10
DIVISION_DEFINITION_BOTTOM = -70

newdf = getCleanCells(newOnly = True,oldOnly = False)

newdf["Growth"] = newdf.groupby("Cell")["Area"].diff()



totalcounts = newdf.groupby("Site").count()
totalcounts["Number of 5 min events"] = totalcounts[["Time"]]
totalcounts = totalcounts[["Number of 5 min events"]]


totalcounts["mean growth (pixels/5 mins)"] = newdf.groupby("Site")["Growth"].mean()
totalcounts["SEM mean growth (pixels/5 mins)"] = newdf.groupby("Site")["Growth"].sem()

totalcounts["mean max growth (/trajectory)"] = newdf.groupby("Cell").max().groupby("Site").mean()["Growth"]

totalcounts = totalcounts.rename(index=dict(zip(["CTRL","GLN","PRO"],["CTRL-new","GLN-new","PRO-new"])))

olddf = getCleanCells(newOnly = False,oldOnly = True)

olddf["Growth"] = olddf.groupby("Cell")["Area"].diff()

totalcounts_old = olddf.groupby("Site").count()
totalcounts_old["Number of 5 min events"] = totalcounts_old[["Time"]]
totalcounts_old = totalcounts_old[["Number of 5 min events"]]

totalcounts_old["mean growth (pixels/5 mins)"] = olddf.groupby("Site")["Growth"].mean()
totalcounts_old["SEM mean growth (pixels/5 mins)"] = olddf.groupby("Site")["Growth"].sem()


totalcounts_old["mean max growth (/trajectory)"] = olddf.groupby("Cell").max().groupby("Site").mean()["Growth"]

totalcounts_old = totalcounts_old.rename(index=dict(zip(["CTRL","GLN","PRO"],["CTRL-old","GLN-old","PRO-old"])))

totalcounts = pd.concat([totalcounts,totalcounts_old])
print(" ")
print(totalcounts)
totalcounts.to_csv("Timelapse Population Stats.csv")

newdf["Initially Present"] = False
olddf["Initially Present"] = True

cells = pd.concat([newdf,olddf])
cells = cells.drop(["Variance","Total Intensity","Center of Mass X","Center of Mass Y","Angle of Major Axis","Length Major Axis","Length Minor Axis","Disappeared in video"],axis=1)
cells.to_csv("timelapse all cells.csv")

