from data_object import Data
import matplotlib.pyplot as plt




class Infographic():
    def __init__(self, pnumber: int):
        self.table = Data(pnumber).pivot()
        self.x_dic = {}
        for i in self.table.index.unique(level='VarName'):
            self.x_dic[i] = self.table.loc[(i,)]
        self.fig = plt.figure(figsize=(10, 12), dpi=300, constrained_layout=True)
        self.gs = self.fig.add_gridspec(nrow=2, ncols=2)

    def add_plot(self, index, key):
        ax = self.fig.add_subplot(self.gs[index+1,0:2])
        ax.plot()






