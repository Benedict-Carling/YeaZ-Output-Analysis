import math
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from clean_cells import getCleanCells

newdf = getCleanCells(newOnly = True,oldOnly = False)

# create new column names
column_names = ['' + str(i+1) for i in range(60)]

newpro = newdf[newdf["Site"]=="PRO"]
newprotable = pd.pivot_table(newpro, values=["Area"], columns=["Time"], index="Cell")
newprotable = newprotable.apply(lambda x: sorted(x, key=pd.isnull), 1)
newprosorted = pd.DataFrame(newprotable.to_list(), columns=column_names)
newpromean = newprosorted.mean()

newgln = newdf[newdf["Site"]=="GLN"]
newglntable = pd.pivot_table(newgln, values=["Area"], columns=["Time"], index="Cell")
newglntable = newglntable.apply(lambda x: sorted(x, key=pd.isnull), 1)
newglnsorted = pd.DataFrame(newglntable.to_list(), columns=column_names)
newglnmean = newglnsorted.mean()

newctrl = newdf[newdf["Site"]=="CTRL"]
newctrltable = pd.pivot_table(newctrl, values=["Area"], columns=["Time"], index="Cell")
newctrltable = newctrltable.apply(lambda x: sorted(x, key=pd.isnull), 1)
newctrlsorted = pd.DataFrame(newctrltable.to_list(), columns=column_names)
newctrlmean = newctrlsorted.mean()

# create a figure and axis
fig, ax = plt.subplots()

# plot each array with a label and different color
ax.plot(newpromean, label='Proline', color='red')
ax.plot(newglnmean, label='Glutamine', color='green')
ax.plot(newctrlmean, label='Control', color='blue')

# set the title and labels
ax.set_title('Growth Trajectories')
ax.set_xlabel('Time')
ax.set_ylabel('Value')

# enable the legend
ax.legend()

# display the plot
plt.show()