import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

INPUT_PATH = "input-data/feb22/8.csv"

data = pd.read_csv(INPUT_PATH)
redData = data[data["Channel"] == "Red"]

min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(redData)
df_normalized = pd.DataFrame(x_scaled)

print(redData)


# plt.hist(normalized_df["Mean"], density=True, bins=50)  # density=False would make counts
# plt.ylabel('Probability')
# plt.xlabel('Data');
# plt.title("Mean cell red value")
# plt.show()
