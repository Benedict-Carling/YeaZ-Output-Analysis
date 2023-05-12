import math

import numpy as np
import scipy
from cell_scatter_analysis import getSubPopulationsMerged

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
    .mean()
)
pivoted = df.pivot_table(index="field-of-view", columns="population", values="score")
pivoted = pivoted.dropna(subset=['high', 'low'])
coeffs = np.polyfit(pivoted['high'], pivoted['low'], 1)
line = np.poly1d(coeffs)

# calculate distance to line for each point
distances = []
for index, row in pivoted.iterrows():
    x = row['high']
    y = row['low']
    distance = line(x) - y 
    distances.append(distance)

# add distances as a new column to the dataframe
pivoted["distance to line of best fit"] = distances


tfdf = getTfDf()
pivoted = pivoted.join(tfdf)

# pivoted["high/low ratio"] = pivoted["high"] / pivoted["low"]
# print(grouped.head())
# print(pivoted.head())

# tfdf = getTfDf()
# pivoted = pivoted.join(tfdf)

# # with_z_scores = calculate_z_scores(pivoted)
# # with_z_scores["p_scores"] = scipy.stats.norm.sf(abs(with_z_scores["z_scores"])) * 2

# idx = np.isfinite(pivoted["high"]) & np.isfinite(pivoted["low"])
# print(idx)
# coeffs = np.polyfit(pivoted["high"][idx],pivoted["low"][idx],1)

# line = np.poly1d(coeffs)

# # calculate distance to line for each point
# distances = []
# for index, row in pivoted.iterrows():
#     x = row['high']
#     y = row['low']
#     distance = line(x) - y / np.sqrt(1 + coeffs[0]**2)
#     distances.append(distance)

# # add distances as a new column to the dataframe
# pivoted['distance_to_line_of_best_fit'] = distances

# # check if the point is above or below the line and assign the sign accordingly
# for index, row in pivoted.iterrows():
#     high = row['high']
#     low = row['low']
#     predicted_low = line(high)
#     if low > predicted_low:
#         pivoted.at[index, 'distance_to_line_of_best_fit'] = abs(pivoted.at[index, 'distance_to_line_of_best_fit'])
#     else:
#         pivoted.at[index, 'distance_to_line_of_best_fit'] = -abs(pivoted.at[index, 'distance_to_line_of_best_fit'])

# with_z_scores = calculate_z_scores(pivoted)
# with_z_scores["p_scores"] = scipy.stats.norm.sf(abs(with_z_scores["z_scores"])) * 2

# print(with_z_scores.sort_values("p_scores"))

pivoted.sort_values("distance to line of best fit").to_csv("{}/{} Candidates v3.csv".format(
        CELLDIRECTORY, FILENAME
    ),)
