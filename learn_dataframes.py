import numpy as np
import pandas as pd


df = pd.DataFrame(columns=["A", "B"])

print(df)

for i in range(5):
    df = df.append({"A": i, "B": "hello"}, ignore_index=True)

print(df)

df = df.reset_index()
for index, item in df.iterrows():
    print(item)
    print(item["A"])
    print(item["B"])

df.to_pickle("my_data.pkl")
