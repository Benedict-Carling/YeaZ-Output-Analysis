import numpy as np
import pandas as pd

LIBFOLDER = "Z_analysis/"
LIBPATH = LIBFOLDER + "tf-lib.csv"

def getTfDf():
    rawdf = pd.read_csv(LIBPATH)
    df = rawdf.set_index("image-index")
    return df
