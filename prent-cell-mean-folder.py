import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np
import math

INPUT_FOLDER = "input-data/feb22"


def plotHistogram(data):
    plt.hist(data, density=True, bins=140)  # density=False would make counts
    plt.ylabel("Probability")
    plt.xlabel("Data")
    plt.title("Cell Size")
    plt.show()


def getCSVFiles():
    myfiles = []
    for subdir, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            if filepath.endswith(".csv"):
                myfiles.append(filepath)
    df = pd.concat(map(pd.read_csv, myfiles))
    return df


df = getCSVFiles()
data = df[df["Channel"] == "Red"]
print(data)
Big = data[data["Area"] >= 147]
Small = data[data["Area"] <= 147]
print(np.mean(Big["Area"]))
print(np.mean(Small["Area"]))
# meanCellSize = data["Area"]
