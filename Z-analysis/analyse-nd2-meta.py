import nd2
import pandas as pd
from analysis_directory import CELLDIRECTORY
from matplotlib import pyplot as plt

ND2FILE = CELLDIRECTORY + "ChannelMono,Red,Green,Blue_Seq0000.nd2"

def Nd2toDataFrame(path):
    f = nd2.ND2File(path)
    for i in range(192):
        location = f.frame_metadata(i*3).channels[0].position.stagePositionUm
        plt.plot(location[0],location[1])
        print(f"{location[0]:.2f}", f"{location[1]:.2f}")
    f.close()
    plt.show()

Nd2toDataFrame(ND2FILE)
