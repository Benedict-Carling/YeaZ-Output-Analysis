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

df = getSubPopulationsMerged(rawdf, EXPERIMENTNAME)
dfclean = getDensityFiltered(rawdf, EXPERIMENTNAME)

print(df)


def calculate_z_scores(df):
    """Converts the given data array into an array of corresponding Z scores.

    Args:
    data_array: A 1D numpy array of the data samples.

    Returns:
    A 1D numpy array of the Z scores of the data samples.
    """
    # Calculate the mean and standard deviation of the given data
    data_array = df["distance_to_line_of_best_fit"]
    mean = np.mean(data_array)
    std_dev = np.std(
        data_array, ddof=1
    )  # using sample standard deviation with Bessel's correction

    # Calculate the Z scores of the data samples
    df["z_scores"] = (df["distance_to_line_of_best_fit"] - mean) / std_dev

    return df


grouped = (
    df[["field-of-view", "population", "score"]]
    .groupby(["field-of-view", "population"])
    .aggregate(["mean","count"])
)

pivoted = grouped.pivot_table(index="field-of-view", columns=["population"], values=("score"))
print(pivoted)


pivoted = pivoted.dropna()
coeffs = np.polyfit(pivoted["mean"]['high'], pivoted["mean"]['low'], 1)
line = np.poly1d(coeffs)

# calculate distance to line for each point
distances = []
for index, row in pivoted.iterrows():
    x = row["mean"]['high']
    y = row["mean"]['low']
    distance = line(x) - y 
    distances.append(distance)

# add distances as a new column to the dataframe
pivoted["distance to line of best fit"] = distances


pivoted["high/low ratio"] = pivoted["mean"]["high"] / pivoted["mean"]["low"]
tfdf = getTfDf()
pivoted = pivoted.join(tfdf)
print(pivoted)

total_cells = grouped = (
    df[["field-of-view", "score"]]
    .groupby(["field-of-view"])
    .count()
)
total_cells["total_cell_number"] = total_cells["score"]

pivoted = pivoted.join(total_cells["total_cell_number"])

pivoted.to_csv("{}/{} Candidates v4.csv".format(
        CELLDIRECTORY, FILENAME
    ),)
