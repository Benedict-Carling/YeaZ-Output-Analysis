import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

fov1 = pd.read_csv("tracking-analysis/fov1-0-30 copy.csv")

fov1_simple = fov1[["Cell", "Time", "Area"]]
fov1_simple = fov1[["Cell", "Time", "Area"]]

print(fov1_simple)
