from data_object import Data
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as dates
import matplotlib.colors as cm
import matplotlib as mpl

class Infographic():
    def __init__(self, pnumber: int):
        self.table = Data(pnumber).pivot()
        self.dic = {}
        for i in self.table.index.unique(level='VarName'):
            self.dic[i] = self.table.loc[(i,)]
        mpl.style.use('dark_background')
        self.fig = plt.figure(figsize=(8.5, 11), dpi=100, constrained_layout=True)
        self.fig.set_facecolor('#4d4d4d')
        self.gs = self.fig.add_gridspec(nrows=2, ncols=2)

    def add_plot(self, index, key):
        ax = self.fig.add_subplot(self.gs[index,0:2])
        x = self.dic[key].index
        y = np.array(self.table['VarValue'][key].to_list())
        ax.plot(x, y)
        ax.xaxis.set_minor_locator(dates.HourLocator(interval=2))  # every 4 hours
        ax.xaxis.set_minor_formatter(dates.DateFormatter(''))  # hours and minutes
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # every day
        ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y'))
        ax.set_ylabel('MPa')


    def show(self):
        plt.show()

info = Infographic(607)
info.add_plot(1,'PT270_Value')
info.show()







