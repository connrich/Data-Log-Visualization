from data_object import Data
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as dates
import matplotlib.colors as cm
import matplotlib as mpl
import matplotlib.image as img
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from datetime import datetime
from matplotlib import cycler
import calendar


class Infographic():
    def __init__(self, pnumber: int, rows: int):
        self.df = Data(pnumber).display()
        self.name = Data(pnumber).dispname()
        self.fig = plt.figure(figsize=(10, 12), dpi=100, constrained_layout=True)
        self.gs = self.fig.add_gridspec(nrows=rows+1, ncols=2)
        self.longtermaxis('PT270_Value')
        self.header()
    def header(self):
        ax = self.fig.add_subplot(self.gs[0,0:2],frameon = False)
        logo = img.imread('logo.png')
        imagebox = OffsetImage(logo, zoom = .85)
        ab = AnnotationBbox(imagebox, (0.47,0.7), pad = 0, frameon = False)
        ax.add_artist(ab)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        today = datetime.today()
        month = today.strftime('%B')
        day = today.strftime('%d')
        year = today.strftime('%G')
        date = month + ' ' + day + ', ' +year
        title = self.name + ' Remote Monitoring Report: ' + date
        ax.annotate(title,(0.5,0.15),va = 'center', ha = 'center',size = 24, weight = 'bold')

    def longtermaxis(self,key):
        ax = self.fig.add_subplot(self.gs[0,0:2],frameon = False)
        ax.get_yaxis().set_visible(False)
        x = self.df.loc[self.df['VarName'] == key].TimeString
        y = self.df.loc[self.df['VarName'] == key].VarValue*0
        ax.bar(x,y,label='_1',width = 1.5, align = 'edge', zorder = 1)
        ax.tick_params(axis="x", direction="out", which='major', width=2, length=15)
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # Show major tick every month
        ax.xaxis.set_major_formatter(dates.DateFormatter(""))  # Don't Show tick label
        alldays = x.dt.day_name()
        days = []
        for i,day in enumerate(alldays):
            if i == 0:
                days.append(day)
            elif days[-1] != day:
                days.append(day)
        for i,day in enumerate(days):
            ax.text(0.16 * (i * 5.4/(len(days)) + 1), -0.05, day,
                        verticalalignment='center', horizontalalignment='center',
                        fontsize=8, fontweight='bold',
                        transform=ax.transAxes)

    def add_plot(self, index, key, feature, units):
        ax = self.fig.add_subplot(self.gs[index+1,0:2],frameon= False)
        x = self.df.loc[self.df['VarName']==key].TimeString
        y = self.df.loc[self.df['VarName']==key].VarValue
        ax.plot(x, y)

        ax.spines['bottom'].set_color(None)
        ax.get_xaxis().set_ticks([])
        ax.set_ylabel(feature+ '\n' + '(' + units + ')', fontsize=10, fontweight='bold')

    def show(self):
        plt.show()

info = Infographic(607,3)
info.add_plot(0,'PT270_Value','Medium Pressure Storage','MPa')
info.add_plot(1,'LIT525_Value','Liquid Level', '%')
info.add_plot(2,'FC461A_FB_Value','Flow Rate', 'SLM')
info.show()







