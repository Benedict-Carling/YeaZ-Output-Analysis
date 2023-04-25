import math

from tf_library_mapping import getTfDf
from get_sub_pop import getSubPopulationsMerged
import scipy.stats as stats
import pandas as pd
import statistics

from analysis_directory import CELLPATH
from analysis_directory import EXPERIMENTNAME

rawdf = pd.read_pickle(CELLPATH)

df = getSubPopulationsMerged(rawdf, EXPERIMENTNAME)


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


def calc_new_high_value(row):
    try:
        hd = row["high"]
        chd = [x for x in hd if not math.isnan(x)]
        return statistics.mean(chd)
    except:
        return 0


def calc_new_low_value(row):
    try:
        hd = row["low"]
        chd = [x for x in hd if not math.isnan(x)]
        return statistics.mean(chd)
    except:
        return 0


def calc_more_localised_direction(row):
    try:
        hd = row["high"]
        ld = row["low"]
        chd = [x for x in hd if not math.isnan(x)]
        cld = [x for x in ld if not math.isnan(x)]
        highmean = statistics.mean(chd)
        lowmean = statistics.mean(cld)
        if lowmean >= highmean:
            return "low"
        else:
            return "high"
    except:
        return "n/a"


result_dict = group_cells_by_image_and_color(df)
raw_pandas_dict = pd.DataFrame(result_dict)
pandas_dict = raw_pandas_dict.transpose()
pandas_dict["ttest"] = pandas_dict.apply(calc_new_stat, axis=1)
pandas_dict["ttest_p"] = pandas_dict.apply(calc_new_pvalue, axis=1)
pandas_dict["high_mean"] = pandas_dict.apply(calc_new_high_value, axis=1)
pandas_dict["low_mean"] = pandas_dict.apply(calc_new_low_value, axis=1)
pandas_dict["Population most localised"] = pandas_dict.apply(calc_more_localised_direction, axis=1)

print(pandas_dict)

dataonly = pandas_dict[["ttest", "ttest_p", "high_mean","low_mean","Population most localised"]]

tfdf = getTfDf()

candidates = dataonly.join(tfdf)

candidates.sort_values("ttest_p").to_csv("candidates_April6th_GLN_4hours.csv")
