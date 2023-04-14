import pandas as pd
import matplotlib.pyplot as plt

from analysis_directory import CELLPATH
from analysis_directory import CELLDIRECTORY
from analysis_directory import FILENAME
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
import numpy as np

import matplotlib.patches as patches


df = pd.read_pickle(CELLPATH)

# df = df[df["size"] > 60]
df = df[df["size"] < 700]

# df = df[df["meanRedValue"] > 110]
df = df[df["meanRedValue"] < 350]

# print(df[["size","meanRedValue"]])

data = {"x": df["size"], "y": df["meanRedValue"]}

df2 = pd.DataFrame(data)


def addPopulationCharacterisation(df):
    data = {"x": df["size"], "y": df["meanRedValue"]}

    df2 = pd.DataFrame(data)

    kmeans = KMeans(n_clusters=2).fit(df2)
    centroids = kmeans.cluster_centers_
    print(centroids)

    # Used K - means clustering to kind the centriods 2 sub population
    # [[196.95771045 189.68542636]
    #  [479.8426798  240.08666979]]
    centroids = [[196.95771045, 185.42314231],[472.19301061, 235.09982935]]

    g_ell_center = centroids[0]
    g_ell_width = 100
    g_ell_height = 40
    angle = 10.0

    cos_angle = np.cos(np.radians(180.0 - angle))
    sin_angle = np.sin(np.radians(180.0 - angle))

    xc = df["size"] - g_ell_center[0]
    yc = df["meanRedValue"] - g_ell_center[1]

    xct = xc * cos_angle - yc * sin_angle
    yct = xc * sin_angle + yc * cos_angle

    df["rad_cc_low"] = (xct**2 / (g_ell_width / 2.0) ** 2) + (
        yct**2 / (g_ell_height / 2.0) ** 2
    )

    df["is_low_population"] = np.where(df["rad_cc_low"] <= 1.0, True, False)

    subpop = df[df["is_low_population"]]

    high_g_ell_center = centroids[1]
    high_g_ell_width = 100
    high_g_ell_height = 40
    high_angle = -10.0

    cos_angle = np.cos(np.radians(180.0 - high_angle))
    sin_angle = np.sin(np.radians(180.0 - high_angle))

    xc = df["size"] - high_g_ell_center[0]
    yc = df["meanRedValue"] - high_g_ell_center[1]

    xct = xc * cos_angle - yc * sin_angle
    yct = xc * sin_angle + yc * cos_angle

    df["rad_cc_high"] = (xct**2 / (high_g_ell_width / 2.0) ** 2) + (
        yct**2 / (high_g_ell_height / 2.0) ** 2
    )

    df["is_high_population"] = np.where(df["rad_cc_high"] <= 1.0, True, False)

    return df, centroids


df2, centroids = addPopulationCharacterisation(df)


# Function to map the colors as a list from the input list of x variables
def pltcolor(lst):
    cols = []
    for ind, l in lst.iterrows():
        if l["is_high_population"]:
            cols.append("red")
        elif l["is_low_population"]:
            cols.append("blue")
        else:
            cols.append("black")
    return cols


# Create the colors list using the function above
cols = pltcolor(df)

print(df[df["is_low_population"]])
print(df[df["is_high_population"]])


def graph():
    plt.scatter(df2["size"], df2["meanRedValue"], c=cols, s=50, alpha=0.003)
    # plt.scatter(centroids[:, 0], centroids[:, 1], c="green", s=50)
    plt.gcf().set_size_inches(16, 9)
    plt.axis([60, 700, 110, 350])
    plt.ylabel("Mean Red")
    plt.xlabel("Size")
    plt.title("{} Cell Scatter Graph - No cells {}".format(FILENAME, len(df)))
    plt.savefig(
        "{}/{} Cell Scatter K-means Graph.png".format(CELLDIRECTORY, FILENAME),
        bbox_inches="tight",
        dpi=200,
    )

# graph()

# c=kmeans.labels_.astype(float)
# c=cols
