import numpy as np
import pandas as pd

LIBFOLDER = "pipeline/"
LIBPATH = LIBFOLDER + "tf-lib.csv"


def getTfDf():
    rawdf = pd.read_csv(LIBPATH)
    df = rawdf.set_index("image-index")
    return df


tf = getTfDf()

print(tf)
