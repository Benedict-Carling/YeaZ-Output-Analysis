import math

from tf_library_mapping import getTfDf
from get_sub_pop import getSubPopulationsMerged
import scipy.stats as stats
import pandas as pd

from analysis_directory import CELLPATH

rawdf = pd.read_pickle(CELLPATH)

df = getSubPopulationsMerged(rawdf)

metrics = df.groupby(["image-index","population"]).agg({"scoreMax":["mean","sem","count"]})

def group_cells_by_image_and_color(df):
    """
    Given a pandas dataframe, group the cellIds by image-index and color.
    Returns a dictionary where each key is an image-index and the value is another
    dictionary with keys 'blue' and 'red' containing the corresponding cellIds.
    """
    # Create an empty dictionary to store the results
    results = {}

    # Group the dataframe by image-index and color
    grouped = df.groupby(["image-index", "population"])

    # Iterate over each group
    for name, group in grouped:
        # Extract the image-index and color from the group name
        image_index, population = name

        # Get the cellIds for this group
        cell_ids = group["scoreMax"].values

        # Sort the cellIds into a dictionary by color
        if image_index not in results:
            results[image_index] = {"low": [], "high": []}

        results[image_index][population].extend(cell_ids)
    return results

def calc_new_stat(row):
   hd = row["high"]
   ld = row["low"]
   chd = [x for x in hd if not math.isnan(x)]
   cld = [x for x in ld if not math.isnan(x)]
   score = stats.ttest_ind(a=chd, b=cld, equal_var=True)
   return score.statistic

def calc_new_pvalue(row):
   hd = row["high"]
   ld = row["low"]
   chd = [x for x in hd if not math.isnan(x)]
   cld = [x for x in ld if not math.isnan(x)]
   score = stats.ttest_ind(a=chd, b=cld, equal_var=True)
   return score.pvalue
    

# print(df)
# print(metrics)
result_dict = group_cells_by_image_and_color(df)
raw_pandas_dict = pd.DataFrame(result_dict)
pandas_dict = raw_pandas_dict.transpose()
pandas_dict["ttest"] = pandas_dict.apply(calc_new_stat, axis=1)
pandas_dict["ttest_p"] = pandas_dict.apply(calc_new_pvalue, axis=1)

dataonly = pandas_dict[["ttest","ttest_p"]]

tfdf = getTfDf()

fdas = dataonly.join(tfdf)

# filtered = dataonly[dataonly["ttest_p"] <= 0.002]

print(fdas)
