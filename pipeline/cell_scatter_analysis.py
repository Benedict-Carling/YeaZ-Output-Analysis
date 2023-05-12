from typing import Literal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import KernelDensity
import json
from helper_spatial_limit import Limitdf, getAxisLimit
from helper_analysis_path import CELLPATH
from helper_analysis_path import CELLDIRECTORY
from helper_analysis_path import FILENAME
from helper_analysis_path import EXPERIMENTNAME

pd.options.mode.chained_assignment = None


def em_clustering(df, x_axis, y_axis, num_clusters=2, confidence=0.85):
    # Get the values of the two axes
    x_values = df[x_axis].values.reshape(-1, 1)
    y_values = df[y_axis].values.reshape(-1, 1)

    # Combine the two axes into a single array
    data = np.hstack((x_values, y_values))

    # Create a Gaussian mixture model with the specified number of clusters
    gmm = GaussianMixture(n_components=num_clusters)

    # Fit the model to the data
    gmm.fit(data)

    # Get the predicted labels for each data point
    labels = gmm.predict(data)

    # Get the probabilities for each label
    probs = gmm.predict_proba(data)

    # Create a new column in the dataframe for the predicted labels
    df["label"] = labels

    # Create a new column in the dataframe for the maximum probability for each label
    df["max_prob"] = np.max(probs, axis=1)

    # Filter the dataframe to include only the rows with high enough confidence
    filtered_df = df[df["max_prob"] >= confidence]
    removed_cells = df[df["max_prob"] < confidence]

    # Split the filtered dataframe into two subgroups based on the predicted labels
    subgroup1 = filtered_df[filtered_df["label"] == 0]
    subgroup2 = filtered_df[filtered_df["label"] == 1]

    # Get the center of each cluster
    print(gmm.means_)
    if gmm.means_[0][0] <= gmm.means_[1][0]:
        print("First group is the subgroup")
        return subgroup1, subgroup2, removed_cells
    else:
        print("Second group is the subgroup, swapping order")
        return subgroup2, subgroup1, removed_cells


def combine_dataframes(*dfs):
    """
    Combines a variable number of dataframes into a single dataframe.
    """
    return pd.concat(dfs, ignore_index=True)


def filter_by_density(df, x_col, y_col):
    # Extract the data from the DataFrame
    x = df[x_col].values
    y = df[y_col].values

    # Estimate the density of the points using a Gaussian kernel density estimator
    xy = np.vstack([x, y]).T
    kde = KernelDensity(
        algorithm="ball_tree", bandwidth=1, metric="euclidean", kernel="linear"
    )
    kde.fit(xy)
    densities = np.exp(kde.score_samples(xy))

    # Select the points where the density exceeds the minimum value
    min_density = np.percentile(densities, 70)
    mask = densities >= min_density
    filtered_df = df.loc[mask]
    return filtered_df


def graph(df, name, axis=False):
    plt.clf()
    plt.cla()
    plt.scatter(df["size"], df["meanRedValue"], color=df["color"], s=5, alpha=0.03)
    # plt.scatter(centroids[:, 0], centroids[:, 1], c="green", s=50)
    plt.gcf().set_size_inches(16, 9)
    if axis:
        plt.axis(axis)
    plt.ylabel("Mean Red")
    plt.xlabel("Size")
    plt.title("{} {} - No cells {}".format(FILENAME, name, len(df)))
    plt.savefig(
        "{}/{} Cell Scatter {}.png".format(CELLDIRECTORY, FILENAME, name),
        bbox_inches="tight",
        dpi=200,
    )


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


def getSubPopulationsMerged(df, type: Literal["april5", "april6-4"], with_graph=False):
    df = Limitdf(df, type)
    dfclean = filter_by_density(df, "size", "meanRedValue")
    # Graph Density scatter
    if with_graph:
        axis = getAxisLimit(type)
        densityCopy = dfclean.copy()
        densityCopy["color"] = "green"
        graph(densityCopy, "Filter by density", axis)

    sub1, sub2, removed_cells = em_clustering(dfclean, "size", "meanRedValue")

    sub1["color"] = "blue"
    sub1["population"] = "low"
    sub2["color"] = "red"
    sub2["population"] = "high"
    removed_cells["color"] = "grey"
    removed_cells["population"] = "none"

    totaldf = combine_dataframes(sub1, sub2, removed_cells)

    if with_graph:
        axis = getAxisLimit(type)
        subpopCopy = totaldf.copy()
        graph(subpopCopy, "Expectation Maximisation", axis)
    return totaldf


def getDensityFiltered(df, type: Literal["april5", "april6-4"], with_graph=False):
    df = Limitdf(df, type)
    dfclean = filter_by_density(df, "size", "meanRedValue")
    return dfclean


df = pd.read_pickle(CELLPATH)
getSubPopulationsMerged(df, EXPERIMENTNAME, True)
