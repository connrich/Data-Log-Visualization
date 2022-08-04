from data_object import Data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as dates
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
from matplotlib import cycler
import calendar
import json


class Infographic():
    def __init__(self, pnumber: int, rows: int):
        col = cycler('color',
                        ['#fc280f', '#5fdcff', '#f4ba26', '#85c54c', '#c6d7e0'])
        plt.rc('figure', facecolor='#222222')

        plt.rc('grid', color='#e3e3e3', linestyle='solid')
        plt.rc('xtick', direction='in', color='#e3e3e3')
        plt.rc('ytick', direction='in', color='#e3e3e3')
        plt.rc('patch', edgecolor='#e3e3e3')
        plt.rc('lines', linewidth=1.5)
        plt.rc('figure', facecolor='#222222')
        self.dic = load_project_json(pnumber)
        self.df = Data(pnumber).display()
        self.name = self.dic['project_name']
        self.fig = plt.figure(figsize=(10, 12), dpi=100, constrained_layout=True)
        self.gs = self.fig.add_gridspec(nrows=rows+1, ncols=2)
        self.longterm_axis()
        plt.rc('axes', facecolor='#222222', edgecolor='#222222',
               axisbelow=True, grid=True,
               prop_cycle=col)  # "axisbelow" set axis ticks and gridlines are below all artists
        self.header()
        self.title()
    def header(self):
        ax = self.fig.add_subplot(self.gs[0,0:2],frameon = False)
        logo = img.imread('header.png')
        imagebox = OffsetImage(logo, zoom = .5,)
        ab = AnnotationBbox(imagebox, (0.5,0.5), pad = 0, frameon = False, annotation_clip = True)
        # (0.47,0.7)
        ax.add_artist(ab)
        ax.set_alpha(1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    def title(self):
        ax = self.fig.add_subplot(self.gs[1,0:2],frameon = False)
        today = datetime.today()
        month = today.strftime('%B')
        day = today.strftime('%d')
        year = today.strftime('%G')
        date = month + ' ' + day + ', ' + year
        title = self.name + ' Remote Monitoring Report: ' + date
        ax.annotate(title,(0.5,0.5),va = 'center', ha = 'center',size = 24, color = '#e3e3e3')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    def longterm_axis(self):
        ax = self.fig.add_subplot(self.gs[1,0:2],frameon = False)
        ax.get_yaxis().set_visible(False)
        key = self.dic['Medium Pressure Storage'][0]
        x = self.df.loc[self.df['VarName'] == key].TimeString
        y = self.df.loc[self.df['VarName'] == key].VarValue*0
        ax.bar(x,y,label='_1',width = 0.01, align = 'edge', zorder = 1)
        ax.tick_params(axis="x", direction="out", which='major', width=2, length=15)
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # Show major tick every day
        ax.xaxis.set_major_formatter(dates.DateFormatter(""))  # Don't Show tick label
        alldays = x.dt.day_name()
        days = []
        for i,day in enumerate(alldays):
            if i == 0:
                days.append(day)
            elif days[-1] != day:
                days.append(day)
        for i,day in enumerate(days):
            ax.text(0.17 * (i * 6.35/(len(days)) + 1), -0.05, day,
                        verticalalignment='center', horizontalalignment='center',
                        fontsize=8, fontweight='bold',
                        transform=ax.transAxes, color='#e3e3e3')

    def add_plot(self,index,feature):
        ax = self.fig.add_subplot(self.gs[index+2,0:2],frameon= False)
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
        key = self.dic["Cold Head Temperatures"]
        tags = key[0]
        full = 0
        for tag in tags:
            full += np.mean(self.df.loc[self.df['VarName'] == tag].VarValue)
        return full/4
    def liq_rate(self):
        key = self.dic["Liquefier Inlet Flow"]
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
        states = self.df.loc[self.df['VarName'] == key].VarValue.reset_index(drop = True)
        times = self.df.loc[self.df['VarName'] == key].TimeString.reset_index(drop = True)
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
        key = self.dic['Gas Bag Storage Level']
        heights = self.df.loc[self.df['VarName'] == key].VarValue.reset_index(drop = True)
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


info = Infographic(607,5)
info.add_plot(1,'Medium Pressure Storage')
info.add_plot(2,'Liquefier Storage Level')
info.add_plot(3,'Liquefier Inlet Flow')
info.show()











