import FlowCal
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import math
import os

folders = [
    "flow_data_analysis/data/Nlim1_Plate_1_4hrs/",
    "flow_data_analysis/data/Nlim1_Plate_2_4hrs/"
]

# folders = [
#     "flow_data_analysis/data/exponentialplate1/",
#     "flow_data_analysis/data/exponentialplate2/"
# ]

flow_frame = pd.DataFrame()

for folder in folders:
    for filename in os.listdir(folder):
        if filename.endswith(".fcs"):
            s = FlowCal.io.FCSData(folder + filename)
            frame = pd.DataFrame(s, columns=s.channels)
            flow_frame = pd.concat([flow_frame, frame])

def graph(df, name, axis=False):
    plt.clf()
    plt.cla()
    # df["logged"] = np.log(df["7-AAD-A"])
    plt.scatter(df["SSC-A"], df["7-AAD-A"], color="green", s=5, alpha=0.002)
    # plt.scatter(centroids[:, 0], centroids[:, 1], c="green", s=50)
    plt.gcf().set_size_inches(16, 9)
    if axis:
        plt.axis(axis)
    plt.xlabel("SSC-A")
    plt.ylabel("7-AAD-A")
    plt.title("scatter")
    plt.savefig(
        "Scatter-4hour.png",
        bbox_inches="tight",
        dpi=200,
    )

def scatter_with_histograms(df, x_col, y_col):
    # Create figure and axes for scatter plot and histograms
    fig, (ax_scatter, ax_hist_x, ax_hist_y) = plt.subplots(
        nrows=1, ncols=3, figsize=(10, 4), 
        gridspec_kw={'width_ratios': [4, 1, 1]}
    )

    # Create scatter plot
    ax_scatter.scatter(df[x_col], df[y_col])

    # Create histogram along x-axis
    ax_hist_x.hist(df[x_col], bins=20)
    ax_hist_x.set_xlim(ax_scatter.get_xlim())
    ax_hist_x.set_yticks([])

    # Create histogram along y-axis
    ax_hist_y.hist(df[y_col], bins=20, orientation='horizontal')
    ax_hist_y.set_ylim(ax_scatter.get_ylim())
    ax_hist_y.set_xticks([])

    # Set axis labels
    ax_scatter.set_xlabel(x_col)
    ax_scatter.set_ylabel(y_col)

    plt.savefig(
        "Scatter-withhist.png",
        bbox_inches="tight",
        dpi=200,
    )

# Size is FSC-A
# Red is 7-AAD-A

# Stage 1 do the gating7-AAD-A
# Plot the scatter graphs

graph(flow_frame,"FSC-A",[0,10_000,0,2500])

print(flow_frame)