import math
from cell_scatter_analysis import getSubPopulationsMerged

from tf_library_mapping import getTfDf
import scipy.stats as stats
import pandas as pd
import statistics

from helper_analysis_path import CELLPATH
from helper_analysis_path import EXPERIMENTNAME

rawdf = pd.read_pickle(CELLPATH)

df = getSubPopulationsMerged(rawdf, EXPERIMENTNAME)

print(df)



grouped = df[["field-of-view","population","score"]].groupby(["field-of-view","population"]).mean()
pivoted = df.pivot_table(index='field-of-view', columns='population', values='score')
pivoted["high/low ratio"] = pivoted['high'] / pivoted['low']
print(grouped.head())
print(pivoted.head())

tfdf = getTfDf()
pivoted = pivoted.join(tfdf)


pivoted.sort_values("high/low ratio").to_csv("candidates_{}.csv".format(EXPERIMENTNAME))