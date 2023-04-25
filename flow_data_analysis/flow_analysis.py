import FlowCal
import pandas as pd
import os

flow_frame = pd.DataFrame()

for filename in os.listdir("flow_data_analysis/data/Nlim1_Plate_1_4hrs/"):
    if filename.endswith(".fcs"): 
         s = FlowCal.io.FCSData('flow_data_analysis/data/Nlim1_Plate_1_4hrs/'+filename)
         frame = pd.DataFrame(s,columns=s.channels)
         flow_frame = pd.concat([flow_frame,frame])

print(flow_frame)