import pandas as pd
from cell_scatter_analysis import getSubPopulationsMerged
import json

from helper_analysis_path import CELLPATH, EXPERIMENTNAME, CELLDIRECTORY


def group_cells_by_image_and_color(df):
    """
    Given a pandas dataframe, group the cellIds by image-index and color.
    Returns a dictionary where each key is an image-index and the value is another
    dictionary with keys 'blue' and 'red' containing the corresponding cellIds.
    """
    # Create an empty dictionary to store the results
    results = {}

    # Group the dataframe by image-index and color
    grouped = df.groupby(["image-index", "color"])

    # Iterate over each group
    for name, group in grouped:
        # Extract the image-index and color from the group name
        image_index, color = name

        # Get the cellIds for this group
        cell_ids = group["cellId"].values

        # Sort the cellIds into a dictionary by color
        if image_index not in results:
            results[image_index] = {"blue": [], "red": []}

        results[image_index][color].extend(cell_ids)

    return results

def save_dict_to_json_file(dict_data, file_path):
    """
    Save a dictionary to a JSON file

    :param dict_data: The dictionary to save
    :param file_path: The file path to save the dictionary to
    """
    with open(file_path, "w") as f:
        json.dump(dict_data, f)

rawdf = pd.read_pickle(CELLPATH)
df = getSubPopulationsMerged(rawdf, EXPERIMENTNAME, False)
data = group_cells_by_image_and_color(df)
save_dict_to_json_file(data,"{}labelled_cells.json".format(CELLDIRECTORY))