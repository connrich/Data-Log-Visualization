from data_object import Data
import matplotlib.pyplot as plt
import pandas as pd
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
    def __init__(self, pnumber: int, rows: int, key):
        self.df = Data(pnumber).display()
        self.name = Data(pnumber).dispname()
        # self.fig = plt.figure(figsize=(10, 12), dpi=100, constrained_layout=True)
        # self.gs = self.fig.add_gridspec(nrows=rows+1, ncols=2)
        self.key = key
        # self.longterm_axis()
        # self.header()
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

    def longterm_axis(self):
        ax = self.fig.add_subplot(self.gs[0,0:2],frameon = False)
        ax.get_yaxis().set_visible(False)
        x = self.df.loc[self.df['VarName'] == self.key].TimeString
        y = self.df.loc[self.df['VarName'] == self.key].VarValue*0
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
        x = self.df.loc[self.df['VarName'] == key].TimeString
        y = self.df.loc[self.df['VarName'] == key].VarValue
        ax.plot(x, y)

        ax.spines['bottom'].set_color(None)
        ax.get_xaxis().set_ticks([])
        ax.set_ylabel(feature+ '\n' + '(' + units + ')', fontsize=10, fontweight='bold')

    def show(self):
        plt.show()
    def purity(self):
        inlet_tag = "Purity Meter_DB_Purity Upstream"
        outlet_tag = "Purity Meter_DB_Purity Downstream"
        inlet_data = self.df.loc[self.df['VarName'] == inlet_tag].VarValue
        outlet_data = self.df.loc[self.df['VarName'] == outlet_tag].VarValue
        inlet_purity = np.mean(inlet_data)
        outlet_purity = np.mean(outlet_data)
        return inlet_purity, outlet_purity
    def ch_temp(self):
        tag1 = "TE510A_Value"
        tag2 = "TE510B_Value"
        tag3 = "TE511A_Value"
        tag4 = "TE511B_Value"
        tags = [tag1, tag2, tag3, tag4]
        full = 0
        for tag in tags:
            full += np.mean(self.df.loc[self.df['VarName'] == tag].VarValue)
        return full/4
    def liq_rate(self):
        tag1 = "FC461A_FB_Value"
        tag2 = "FC461B_FB_Value"
        tags = [tag1, tag2]
        value = 0
        for tag in tags:
            value += integrate(self.df.loc[self.df['VarName'] == tag].VarValue, 1/2)
        liquid = value/745
        run_hrs, hrs = self.liq_runtime()
        return (liquid/run_hrs*24)
    def liq_runtime(self):
        dates = (self.df.loc[self.df['VarName'] == self.key].TimeString).reset_index(drop = True)
        end = dates.size - 1
        hrs = round((dates[end] - dates[0]).total_seconds()/3600)
        states = self.df.loc[self.df['VarName'] == "Liquefier_DB_State"].VarValue.reset_index(drop = True)
        times = self.df.loc[self.df['VarName'] == "Liquefier_DB_State"].TimeString.reset_index(drop = True)
        on_times = []
        off_times = []
        dt = (times[1]-times[0]).total_seconds()/3600
        run_hrs = 0
        for state in states:
            if state == 4:
                run_hrs += dt
        run_hrs = round(run_hrs)
        return run_hrs, hrs
    def gb_cycles(self):
        heights = self.df.loc[self.df['VarName'] == "Level_Control_DB_GB_Level"].VarValue.reset_index(drop = True)
        top = max(heights)
        bottom = min(heights)
        mid = round((top-bottom)/2+bottom)
        value = 0
        for i in range(0,heights.size-1):
            x = round(heights[i])
            y = round(heights[i+1])
            if x == mid and y != x:
                value += 1
        run_hrs, hrs = self.liq_runtime()
        return round(value/hrs)*24
    def recovery_rate(self,leak_rate,conversion):
        tag1 = 'FC461A_FB_Value'
        tag2 = 'FC461B_FB_Value'
        tag3 = 'PT270_Value'
        tags = [tag1,tag2]
        out_flow = 0
        for tag in tags:
            out_flow += integrate(self.df.loc[self.df['VarName'] == tag].VarValue, 1/2)
        run_hrs, hrs = self.liq_runtime()
        leak = leak_rate*hrs*60
        pressure = self.df.loc[self.df['VarName'] == "PT270_Value"].VarValue.reset_index(drop = True)
        volume = (pressure[pressure.size - 1] - pressure[0]) * conversion
        recovered = volume - out_flow + leak
        liqeq = recovered/745
        rate = (liqeq/hrs)*24
        return rate







def integrate(vec, dt):
    value = 0
    for element in vec:
        value += dt * element
    return value



conv = 9.87
info = Infographic(607,3,"PT270_Value")
print(info.recovery_rate(36, conv))





