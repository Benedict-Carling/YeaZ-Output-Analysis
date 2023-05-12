from cell_scatter_analysis import getSubPopulationsMerged
import pandas as pd

from helper_analysis_path import EXPERIMENTNAME
from helper_analysis_path import CELLPATH
from helper_analysis_path import CELLDIRECTORY
from helper_analysis_path import FILENAME

rawdf = pd.read_pickle(CELLPATH)
df = getSubPopulationsMerged(rawdf, EXPERIMENTNAME)
df.to_csv(
    "{}/{} all cells.csv".format(CELLDIRECTORY, FILENAME),
)
