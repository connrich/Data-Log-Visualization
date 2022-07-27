from data_object import Data
import matplotlib.pyplot as plt
import numpy as np



class Infographic():
    def __init__(self, pnumber: int):
        self.table = Data(pnumber).pivot()
        self.dic = {}
        for i in self.table.index.unique(level='VarName'):
            self.dic[i] = self.table.loc[(i,)]
        self.fig = plt.figure(figsize=(10, 12), dpi=300, constrained_layout=True)
        self.gs = self.fig.add_gridspec(nrows=2, ncols=2)

    def add_plot(self, index, key):
        ax = self.fig.add_subplot(self.gs[index,0:2])
        x = np.array((self.dic[key].index))
        y = self.table['VarValue'][key].to_list()
        ax.plot(x,y)

    def show(self):
        plt.show()

info = Infographic(607)
info.add_plot(1,'PT270_Value')
info.show()







