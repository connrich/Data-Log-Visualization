from data_object import Data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as dates
from datetime import timedelta
from matplotlib import colors
from matplotlib import cm
import matplotlib as mpl
from matplotlib import patches
import matplotlib.image as img
from matplotlib import cycler
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
import os
import json
from datetime import datetime
from scipy import signal
from matplotlib import cycler
import calendar
import json


class Infographic():
    def __init__(self, pnumber: int):
        col = cycler('color',
                        ['#fc280f', '#5fdcff', '#f4ba26', '#85c54c', '#c6d7e0'])
        plt.rc('figure', facecolor='#474747')

        plt.rc('grid', color='#e3e3e3', linestyle='solid')
        plt.rc('xtick', direction='in', color='#e3e3e3')
        plt.rc('ytick', direction='in', color='#e3e3e3')
        plt.rc('patch', edgecolor='#e3e3e3')
        plt.rc('lines', linewidth=1.5)
        plt.rc('figure', facecolor='#474747')

        self.dic = load_project_json(pnumber)
        self.df = Data(pnumber).display()
        self.name = self.dic['project_name']
        self.fig = plt.figure(figsize=(12, 15), dpi=50, constrained_layout=True)
        self.gs = self.fig.add_gridspec(nrows=9, ncols=3)
        self.longterm_axis()
        plt.rc('axes', facecolor='#474747', edgecolor='#474747',
               axisbelow=True, grid=True,
               prop_cycle=col)  # "axisbelow" set axis ticks and gridlines are below all artists
        self.header()
        self.title()
        self.index = (2,0)
    def header(self):
        ax = self.fig.add_subplot(self.gs[0,0:3],frameon = False)
        logo = img.imread('logo.png')
        imagebox = OffsetImage(logo, zoom = 0.1,)
        ab = AnnotationBbox(imagebox, (0.5,0.5), pad = 0, frameon = False, annotation_clip = True)
        # (0.47,0.7)
        ax.add_artist(ab)
        ax.set_alpha(1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    def title(self):
        ax = self.fig.add_subplot(self.gs[1,0:3],frameon = False)
        today = datetime.today()
        month = today.strftime('%B')
        day = today.strftime('%d')
        year = today.strftime('%G')
        date = month + ' ' + day + ', ' + year
        title = self.name + ' Remote Monitoring Report: ' + date
        ax.annotate(title,(0.5,0.5),va = 'center', ha = 'center',size = 24, color='#e3e3e3')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    def longterm_axis(self):
        ax = self.fig.add_subplot(self.gs[1,0:3],frameon = False)
        ax.get_yaxis().set_visible(False)
        key = self.dic['Medium Pressure Storage'][0]
        x = self.df.loc[self.df['VarName'] == key].TimeString
        y = self.df.loc[self.df['VarName'] == key].VarValue*0
        ax.bar(x,y,label='_1',width = 0.01, align = 'edge', zorder = 1)
        ax.tick_params(axis="x", direction="out", which='major', width=2, length=10)
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # Show major tick every day
        ax.xaxis.set_major_formatter(dates.DateFormatter(""))  # Don't Show tick label
        alldays = x.dt.day_name()
        days = []
        for i,day in enumerate(alldays):
            if i == 0:
                days.append(day)
            elif days[-1] != day:
                days.append(day)
        days = days[0:len(days)-1]
        for i,day in enumerate(days):
            ax.text(0.17 * (i * 6.35/(len(days)+1) + 1), -0.05, day,
                        verticalalignment='center', horizontalalignment='center',
                        fontsize=8, fontweight='bold',
                        transform=ax.transAxes, color='#e3e3e3')

    def add_plot(self, feature):
        ax = self.fig.add_subplot(self.gs[self.index[0],0:3],frameon= False)
        self.index= (self.index[0]+1,self.index[1])
        key = self.dic[feature]
        tag = key[0]
        units = key[1]
        if type(tag) != list:
            x = self.df.loc[self.df['VarName'] == tag].TimeString
            y = self.df.loc[self.df['VarName'] == tag].VarValue
            color = cm.RdYlBu_r(y / max(y))
            plot = ax.scatter(x, y, color = color)
            sz = np.ones(x.size)
            plot.set_sizes(sz)
        if type(tag) == list:
            x = self.df.loc[self.df['VarName'] == tag[0]].TimeString
            y = ''
            for i,data in enumerate(tag):
                if i == 0:
                    y = self.df.loc[self.df['VarName'] == data].VarValue.reset_index(drop =True)
                else:
                    y0 = self.df.loc[self.df['VarName'] == data].VarValue.reset_index(drop =True)
                    y = y + y0
            color = cm.RdYlBu_r(y / max(y))
            plot = ax.scatter(x, y, color=color)
            sz = np.ones(x.size)
            plot.set_sizes(sz)
        ax.spines['bottom'].set_color(None)
        ax.get_xaxis().set_ticks([])
        ax.set_title(feature, fontsize=10, fontweight='bold', color='#e3e3e3')
        ax.set_ylabel(units, fontsize=10, color='#e3e3e3')
        ax.tick_params(axis="x", direction="out", which='major', width=0, length=15)
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # Show major tick every day
        ax.xaxis.set_major_formatter(dates.DateFormatter(""))  # Don't Show tick label

    def add_bubble(self,feature):
        ax = self.fig.add_subplot(self.gs[self.index[0]:(self.index[0]+2), self.index[1]],frameon= True)
        if self.index[1]==2:
            self.index = (self.index[0]+2,0)
        else:
            self.index = (self.index[0],self.index[1]+1)
        # color = cm.Pastel1(np.random.rand())
        color = '#2B5AA0'
        box = patches.FancyBboxPatch((0.3, 0.3), width=0.4, height=0.4, boxstyle='circle, pad = 0.2',
                                         fc=color, ec = '#e3e3e3', zorder=1, alpha=0.8)
        ax.add_artist(box)
        if feature == "Inlet Purity" or feature == "Outlet Purity":
            value = self.purity(feature)
            fs = 'x-large'
            ax.text(0.5, 0.7, 'Average', ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.6, feature, ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.4, str(round(value * 100) / 100) + str(self.dic[feature][1]),
                    ha='center', fontsize='x-large', color='#e3e3e3')
        if feature == "Cold Head Temperature":
            value = self.ch_temp(feature)
            ax.text(0.5, 0.8, 'Average', ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.7, 'Cold Head', ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5,0.6, 'Temperature', ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.4, str(round(value * 100) / 100) +"° "+str(self.dic[feature][1]),
                    ha='center', fontsize='x-large', color='#e3e3e3')
        if feature == 'Liquefaction Rate':
            value = self.liq_rate()
            ax.text(0.5, 0.7, 'Average', ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.6, 'Liquefaction Rate', ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.25, str(round(value * 100) / 100) + '\n' + "Liters of Liquid" + "\n" + "Helium per Day",
                    ha='center', fontsize='x-large', color='#e3e3e3')
        if feature == 'Gas Bag Cycles':
            value = self.gb_cycles()
            ax.text(0.5, 0.7, 'Average', ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.6, feature, ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.4, str(value) + " Cycles per Day",
                    ha='center', fontsize='x-large', color='#e3e3e3')
        if feature == 'Liquefier Run Time':
            run_hrs,hrs = self.liq_runtime()
            value = run_hrs/hrs*100
            ax.text(0.5, 0.6, 'Liquefier Run Time', ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.4, str(round(value * 100) / 100) + "%",
                    ha='center', fontsize='x-large', color='#e3e3e3')

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)





    def show(self):
        plt.show()
    def purity(self,feature):
        key = self.dic[feature]
        data = self.df.loc[self.df['VarName'] == key[0]].VarValue
        purity = np.mean(data)
        return purity
    def ch_temp(self, feature):
        key = self.dic[feature]
        tags = key[0]
        full = 0
        for tag in tags:
            full += np.mean(self.df.loc[self.df['VarName'] == tag].VarValue)
        return full/4
    def liq_rate(self):
        key = self.dic['Liquefier Inlet Flow']
        tags = key[0]
        value = 0
        for tag in tags:
            value += integrate(self.df.loc[self.df['VarName'] == tag].VarValue, 1/2)
        liquid = value/745
        run_hrs, hrs = self.liq_runtime()
        return (liquid/run_hrs*24)
    def liq_runtime(self):
        key = self.dic['Medium Pressure Storage'][0]
        dates = (self.df.loc[self.df['VarName'] == key].TimeString).reset_index(drop = True)
        end = dates.size - 1
        hrs = round((dates[end] - dates[0]).total_seconds()/3600)
        key = self.dic['liquefier_state']
        states = self.df.loc[self.df['VarName'] == key[0]].VarValue.reset_index(drop = True)
        times = self.df.loc[self.df['VarName'] == key[0]].TimeString.reset_index(drop = True)
        dt = self.dt('Medium Pressure Storage')
        run_hrs = 0
        for state in states:
            if state == 4:
                run_hrs += dt
        run_hrs = round(run_hrs)
        return run_hrs, hrs
    def gb_cycles(self):
        key = self.dic['Gas Bag Storage Level']
        heights = self.df.loc[self.df['VarName'] == key[0]].VarValue.reset_index(drop = True)
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
        return int(round(value/hrs)*24)
    def recovery_rate(self,leak_rate,conversion):
        key = self.dic['Liquefier Inlet Flow']
        tag3 = 'PT270_Value'
        tags = key[0]
        out_flow = 0
        for tag in tags:
            out_flow += integrate(self.df.loc[self.df['VarName'] == tag].VarValue, 1/2)
        run_hrs, hrs = self.liq_runtime()
        leak = leak_rate*hrs*60
        pressure_key = self.dic['Medium Pressure Storage'][0]
        pressure = self.df.loc[self.df['VarName'] == "PT270_Value"].VarValue.reset_index(drop = True)
        volume = (pressure[pressure.size - 1] - pressure[0]) * conversion
        recovered = volume - out_flow + leak
        liqeq = recovered/745
        rate = (liqeq/hrs)*24
        return rate
    def leak_rate(self):
        liq_key = "liquefier_state"
        tag1 = self.dic[liq_key][0]
        liq_dates= (self.df.loc[self.df['VarName'] == tag1].TimeString).reset_index(drop = True)
        storage_key = "Medium Pressure Storage"
        tag2 = self.dic[storage_key][0]
        raw_states = (self.df.loc[self.df['VarName'] == tag1].VarValue).reset_index(drop = True)
        raw_pressure = (self.df.loc[self.df['VarName'] == tag2].VarValue).reset_index(drop = True)
        pres_dates = (self.df.loc[self.df['VarName'] == tag2].TimeString).reset_index(drop = True)
        bools1 = liq_dates.isin(pres_dates)
        states=[]
        for i, boo in enumerate(bools1):
            if boo:
                states.append(raw_states[i])
        bools2 = pres_dates.isin(liq_dates)
        pressures = []
        for i, boo in enumerate(bools2):
            if boo:
                pressures.append(raw_pressure[i])
        off_pressure = []
        tmp = []
        stor = 2
        for i, state in enumerate(states):
            if (state == 2 and stor != 2 and len(tmp) != 0):
                off_pressure.append(tmp)
                tmp = []
                tmp.append(pressures[i])
            if (state == 2):
                tmp.append(pressures[i])
            stor = state
        psa = self.psa_swing()
        peak = []
        valley = []
        for i,list in enumerate(peak):
            pdata, _ = signal.find_peaks(off_pressure[i], height=0, distance=10*psa)
            peak.append(pdata)
            vdata, _ = signal.find_peaks(off_pressure[i]*-1, height=0, distance=10*psa)
            valley.append(vdata)





        return peak, valley
    def dt(self, feature):
        key = self.dic[feature]
        times = (self.df.loc[self.df['VarName'] == key[0]].TimeString).reset_index(drop=True)
        return (times[1]-times[0])/timedelta(minutes=1)
    def psa_swing(self):
        tag = self.dic['Medium Pressure Storage']
        y = (self.df.loc[self.df['VarName'] == tag[0]].VarValue).reset_index(drop=True)
        raw_peaks, _ = signal.find_peaks(y, height = 0, distance = 2)
        stor = 0
        dt = self.dt('Medium Pressure Storage')
        peaks = []
        for peak in raw_peaks:
            if (peak-stor)*dt<=4:
                peaks.append(peak)
            stor = peak
        delta = []
        for i,peak in enumerate(peaks):
            if i != 0:
                delta.append(peak-peaks[i-1])
        swing = np.mean(delta)
        return int(round(swing))






def integrate(vec, dt):
    value = 0
    for element in vec:
        value += dt * element
    return value


# Example for loading the json
def load_project_json(proj_number: int) -> dict:
    # Location of the project's json
    path = f'Infographic Settings\{proj_number}.json'
    
    # Open json and load as a dictionary
    with open(path, 'r') as json_file:
        settings = json.load(json_file)
    
    # Return the json dictionary
    return settings

if __name__ == '__main__':
    info = Infographic(607)
    # info.add_plot('Medium Pressure Storage')
    # info.add_plot('Liquefier Storage Level')
    # info.add_plot('Liquefier Inlet Flow')
    # info.add_bubble('Inlet Purity')
    # info.add_bubble('Outlet Purity')
    # info.add_bubble('Cold Head Temperature')
    # info.add_bubble('Liquefaction Rate')
    # info.add_bubble('Gas Bag Cycles')
    # info.add_bubble('Liquefier Run Time')
    # info.show()
    # lists = info.leak_rate()
    print(info.leak_rate())










