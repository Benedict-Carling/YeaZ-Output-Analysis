import pandas as pd

import nd2
import numpy as np
import pandas as pd
import h5py
from scipy.ndimage import gaussian_filter, binary_erosion, binary_dilation
import sys

CELLDIRECTORY = sys.argv[1]

ND2FILE = CELLDIRECTORY + "ChannelMono,Red,Green,Blue_Seq0000.nd2"

f = nd2.ND2File(ND2FILE)
print(f.frame_metadata(0))

# absoluteJulianDayNumber=2460068.3315480077, relativeTimeMs=36832.8612999916


# rawdf = pd.read_pickle("data/20230503_205612_083/cells-ratio-with-nuc.pkl")
# rawdf2 = pd.read_pickle("data/20230503_205612_083/cells-ratio-with-nuc-check.pkl")

# print(rawdf[rawdf["image-index"]==1])
# print(rawdf2)
