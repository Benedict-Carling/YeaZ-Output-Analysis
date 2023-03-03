import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "input-data/feb22/8.csv"

data = pd.read_csv(INPUT_PATH)
redData = data[data["Channel"] == "Red"]


plt.hist(redData["Mean"], density=True, bins=50)  # density=False would make counts
plt.ylabel("Probability")
plt.xlabel("Data")
plt.title("Mean cell red value")
plt.show()
