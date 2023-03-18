import pandas as pd
import matplotlib.pyplot as plt

df= pd.read_pickle("data/feb22/all-cells.pkl")

df= df[df["size"] > 40]
df= df[df["size"] < 400]

WellAverageAnalysis = pd.DataFrame(columns=["field-of-view", "cell-number", "mean-correlation","max-correlation","min-correlation"])
for key in df["field-of-view"].unique():
    subset = df[df["field-of-view"] == key]
    col = subset["greenBlueCorrelation"]
    print("Field of view {} - {}".format(key, len(subset)))
    print("low {}, mean {}, high {}".format(col.min(), col.mean(), col.max()))
    WellAverageAnalysis = WellAverageAnalysis.append(
                {
                   "field-of-view":key,
                    "cell-number":len(subset),
                    "mean-correlation":col.mean(),
                    "max-correlation":col.max(),
                   "min-correlation":col.min(),
                },
                ignore_index=True,
            )
    
# print(WellAverageAnalysis["field-of-view"].unique())
WellAverageAnalysis.sort_values(by=['mean-correlation'], ascending=True, inplace=True)
WellAverageAnalysis.sort_values(by=['mean-correlation'], ascending=True, inplace=True)
print(WellAverageAnalysis[30:40])

# plt.hist(WellAverageAnalysis["mean-correlation"], density=True, bins=200)  # density=False would make counts
# plt.ylabel("Probability")
# plt.xlabel("Data")
# plt.title("Mean green blue pearson correlation across by well")
# plt.show()

# plt.hist(df["greenBlueCorrelation"], density=True, bins=200)  # density=False would make counts
# plt.ylabel("Probability")
# plt.xlabel("Data")
# plt.title("Mean green blue pearson correlation across all wells")
# plt.show()


# plt.hist(df["size"], density=True, bins=200)  # density=False would make counts
# plt.ylabel("Probability")
# plt.xlabel("Data")
# plt.title("Average cell size")
# plt.show()
