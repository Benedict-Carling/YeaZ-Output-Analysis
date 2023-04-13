import pandas as pd
import matplotlib.pyplot as plt

from analysis_directory import CELLPATH
from analysis_directory import CELLDIRECTORY
from analysis_directory import FILENAME

df = pd.read_pickle(CELLPATH)

# df = df[df["size"] > 25]
df = df[df["size"] < 900]

# APRIL SIZE BETWEEN 60 and 600


plt.hist(df["size"], density=True, bins=300)  # density=False would make counts

plt.gcf().set_size_inches(16, 9)
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("{} Cell Size Histogram - No cells {}".format(FILENAME,len(df)))
plt.savefig("{}/{} Cell Size Histogram.png".format(CELLDIRECTORY,FILENAME),dpi=200)

