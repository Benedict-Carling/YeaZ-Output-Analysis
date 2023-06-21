import numpy as np
import pandas as pd

from analysis_directory import CELLPATH
from analysis_directory import CELLDIRECTORY
from analysis_directory import FILENAME
from get_cellIds_per_well import getSubPopulationsMerged


def calculate_se(*arr):
    """
    Calculates the standard error between an array of three numbers.
    """
    arr = arr[~np.isnan(arr)]

    # Calculate the standard deviation of the array
    sd = np.std(arr, ddof=1)

    # Calculate the standard error of the array
    se = sd / np.sqrt(len(arr))

    return se


rawdf = pd.read_pickle(CELLPATH)

df1 = rawdf.assign(
    Discount_Percent=lambda x: calculate_se(x["score0"], x["score1"], x["score2"])
)

print(rawdf[["score0", "score1", "score2"]])

df = getSubPopulationsMerged(rawdf)

# low = df[df["population"] == "low"]
# high = df[df["population"] == "high"]

# group_low = low.groupby(["image-index"], as_index=False).agg(
#     {"scoreMax": ["mean","sem"],"score0": ["mean","sem"],"score1": ["mean","sem"],"score2": ["mean","sem"], "cellId": "count"}
# )
# group_high = high.groupby(["image-index"], as_index=False).agg(
#     {"scoreMax": ["mean","sem"],"score0": ["mean","sem"],"score1": ["mean","sem"],"score2": ["mean","sem"], "cellId": "count"}
# )

# print(group_low)
# print(group_high)
# print("ScoreMax mean Sem: ",np.mean(group_high["scoreMax"]["sem"]))
# print("ScoreMax mean Sem: ",np.mean(group_low["scoreMax"]["sem"]))
