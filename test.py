from data_object import Data
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as dates
from datetime import datetime


df = Data(607).display()
x = df.loc[df['VarName'] == 'PT270_Value'].TimeString
alldays = x.dt.day_name()
days = []
for i in alldays:
    if len(days)==0:
        days.append(i)
    elif days[-1]!=i:
        days.append(i)
print(days)