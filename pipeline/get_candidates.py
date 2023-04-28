import math

import numpy as np
import scipy
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


def calculate_z_scores(df):
    """Converts the given data array into an array of corresponding Z scores.

    Args:
    data_array: A 1D numpy array of the data samples.

    Returns:
    A 1D numpy array of the Z scores of the data samples.
    """
    # Calculate the mean and standard deviation of the given data
    data_array = df["high/low ratio"]
    mean = np.mean(data_array)
    std_dev = np.std(
        data_array, ddof=1
    )  # using sample standard deviation with Bessel's correction

    # Calculate the Z scores of the data samples
    df["z_scores"] = (df["high/low ratio"] - mean) / std_dev

    return df


df["score"] = df["scoreMax"]
grouped = (
    df[["field-of-view", "population", "score"]]
    .groupby(["field-of-view", "population"])
    .mean()
)
pivoted = df.pivot_table(index="field-of-view", columns="population", values="score")
pivoted["high/low ratio"] = pivoted["high"] / pivoted["low"]
print(grouped.head())
print(pivoted.head())

tfdf = getTfDf()
pivoted = pivoted.join(tfdf)

with_z_scores = calculate_z_scores(pivoted)
with_z_scores["p_scores"] = scipy.stats.norm.sf(abs(with_z_scores["z_scores"])) * 2

print(with_z_scores.sort_values("p_scores"))

with_z_scores.sort_values("p_scores").to_csv("candidates_{}.csv".format(EXPERIMENTNAME))
