import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle("data/mar15/cells.pkl")

df = df[df["size"] > 65]
df = df[df["size"] < 600]

df = df[df["meanRedValue"] > 50]
df = df[df["meanRedValue"] < 150]

# print(df)

lowPopulation = df[df["meanRedValue"] > 78]
lowPopulation = lowPopulation[lowPopulation["meanRedValue"] < 93]

highPopulation = df[df["meanRedValue"] > 95]
highPopulation = highPopulation[highPopulation["meanRedValue"] < 122]

print(lowPopulation)
print(highPopulation)


plt.hist(df["meanRedValue"], density=True, bins=1000)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell red value")
plt.show()
