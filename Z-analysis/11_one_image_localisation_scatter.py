from get_sub_pop import getSubPopulationsMerged
from analysis_directory import CELLPATH
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from adjustText import adjust_text
import math
import statistics
from scipy.stats import sem

from analysis_directory import CELLPATH
from analysis_directory import CELLDIRECTORY
from analysis_directory import FILENAME

rawdf = pd.read_pickle(CELLPATH)

cleandf = getSubPopulationsMerged(rawdf)

IMAGE = 151

df = cleandf[cleandf["image-index"] == IMAGE]

lowPopulation = df[df["population"]=="low"]
highPopulation = df[df["population"]=="high"]

print(lowPopulation)
print(highPopulation)


hd = highPopulation["scoreMax"].to_list()
ld = lowPopulation["scoreMax"].to_list()

chd = [x for x in hd if not math.isnan(x)]
cld = [x for x in ld if not math.isnan(x)]
print(IMAGE)
print("High Population")
print("Standard Error highPopulation",format(sem(chd),".5f"))
print("Size highPopulation",len(chd))
print("Standard Deviation highPopulation",format(statistics.stdev(chd), ".5f"))
print("Low Population")
print("Standard Error lowPopulation",format(sem(cld),".5f"))
print("Size lowPopulation",len(cld))
print("Standard Deviation lowPopulation",format(statistics.stdev(cld), ".5f"))

# highData = highPopulation[~highPopulation["scoreMax"].isna()] 
# lowData = lowPopulation[~lowPopulation["scoreMax"].isna()] 
# hd = highData.tolist()
# ld = lowData.tolist()

data = [chd, cld]

# Multiple box plots on one Axes
fig, ax = plt.subplots()
ax.boxplot(data,labels=["high","low"])
plt.title("{} Cell Localisation Scores Box plot - index {}".format(FILENAME, IMAGE))
plt.ylabel("Nuclear Cytosolic Ratio Score")


plt.savefig(
    "{}/{} Cell Localisation Boxplot {}".format(
        CELLDIRECTORY, FILENAME,IMAGE
    ),
    bbox_inches="tight",
    dpi=200,
)