import math

import numpy as np
import scipy
from cell_scatter_analysis import getSubPopulationsMerged, getDensityFiltered

from tf_library_mapping import getTfDf
import scipy.stats as stats
import pandas as pd
from sklearn.linear_model import LinearRegression

from helper_analysis_path import CELLPATH
from helper_analysis_path import EXPERIMENTNAME
from helper_analysis_path import CELLDIRECTORY
from helper_analysis_path import FILENAME

rawdf = pd.read_pickle(CELLPATH)

print(rawdf[["size", "meanRedValue"]])
rawdf[["size", "meanRedValue"]].to_csv(FILENAME + " microscopy data.csv")


# df = getSubPopulationsMerged(rawdf, EXPERIMENTNAME)
# # dfclean = getDensityFiltered(rawdf, EXPERIMENTNAME)

# print(df["image-index"].unique())
