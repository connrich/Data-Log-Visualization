from data_object import Data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as dates
from datetime import timedelta
from matplotlib import cm
from matplotlib import patches
import matplotlib.image as img
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from datetime import datetime
from scipy import signal
from matplotlib import cycler
import json

# Infographic Object
class Infographic():

    # Initializes with two inputs, the project number and the data frame (data frame is optional)
    def __init__(self, pnumber: int, data: pd.DataFrame=None):

        # Initialize the plt format
        col = cycler('color',
                        ['#fc280f', '#5fdcff', '#f4ba26', '#85c54c', '#c6d7e0'])
        plt.rc('figure', facecolor='#474747')
        plt.rc('grid', color='#e3e3e3', linestyle='solid')
        plt.rc('xtick', direction='in', color='#e3e3e3')
        plt.rc('ytick', direction='in', color='#e3e3e3')
        plt.rc('patch', edgecolor='#e3e3e3')
        plt.rc('lines', linewidth=1.5)
        plt.rc('figure', facecolor='#474747')
        plt.rc('axes', facecolor='#474747', edgecolor='#474747',
               axisbelow=True, grid=True,
               prop_cycle=col)  # "axisbelow" set axis ticks and gridlines are below all artists

        # Allows already loaded data to be passed in as an argument 
        if data is None:
            self.df = Data(pnumber).display()
        elif isinstance(data, pd.DataFrame):
            if data['TimeString'].dtype == np.float64:
                data['TimeString'] = pd.to_datetime(data['TimeString'], unit='s')
            self.df = data

        # Pull the correct json file
        self.dic = load_project_json(pnumber)
        self.name = self.dic['project_name']

        # Create the figure and layout
        self.fig = plt.figure(figsize=(12, 15), dpi=50, constrained_layout=True)
        self.gs = self.fig.add_gridspec(nrows=9, ncols=3)

        # Adds long term axis, header, and title
        self.longterm_axis()
        self.header()
        self.title()
        self.index = (2, 0)

        # Header function. Adds quantum logo to top of page
    def header(self):

        ax = self.fig.add_subplot(self.gs[0,0:3],frameon = False)

        # Read in logo, throw it in a box, put that box on the axis
        logo = img.imread('logo.png')
        imagebox = OffsetImage(logo, zoom = 0.1,)
        ab = AnnotationBbox(imagebox, (0.5,0.5), pad = 0, frameon = False, annotation_clip = True)
        ax.add_artist(ab)

        # Axis visibility
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Title function. Adds title below quantum logo
    def title(self):

        ax = self.fig.add_subplot(self.gs[1,0:3],frameon = False)

        # Creates date string
        today = datetime.today()
        month = today.strftime('%B')
        day = today.strftime('%d')
        year = today.strftime('%G')
        date = month + ' ' + day + ', ' + year

        # Create title and add to axis
        title = self.name + ' Remote Monitoring Report: ' + date
        ax.annotate(title, (0.5, 0.5),va = 'center', ha = 'center',size = 24, color='#e3e3e3')

        # Axis visibility
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    # Long term axis function. Adds long term axis to title section
    def longterm_axis(self):

        ax = self.fig.add_subplot(self.gs[1,0:3],frameon = False)

        # Pull data for axis
        key = self.dic['Medium Pressure Storage'][0]
        x = self.df.loc[self.df['VarName'] == key].TimeString
        y = self.df.loc[self.df['VarName'] == key].VarValue*0

        # Create empty bar graph with x-axis formatting for long-term axis
        ax.bar(x,y,label='_1',width = 0.01, align = 'edge', zorder = 1)
        ax.tick_params(axis="x", direction="out", which='major', width=2, length=10)
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # Show major tick every day
        ax.xaxis.set_major_formatter(dates.DateFormatter("%m/%d"))  # Tick label formatting

        # Axis Visibility
        ax.grid(False)
        ax.get_yaxis().set_visible(False)

    # Adds a long-term plot, defined by the feature argument.
    def add_plot(self, feature):

        ax = self.fig.add_subplot(self.gs[self.index[0],0:3],frameon= False)

        # Increments the index so plots don't overlap
        self.index= (self.index[0]+1,self.index[1])

        # Pulls data using the keys from JSON file
        key = self.dic[feature]
        tag = key[0]
        units = key[1]
        x = 0
        y = 0
        if type(tag) != list:  # Single sensor case
            x = self.df.loc[self.df['VarName'] == tag].TimeString
            y = self.df.loc[self.df['VarName'] == tag].VarValue

        if type(tag) == list:  # Multiple sensor case. Adds the data from each sensor
            x = self.df.loc[self.df['VarName'] == tag[0]].TimeString
            y = ''
            for i,data in enumerate(tag):
                if i == 0:
                    y = self.df.loc[self.df['VarName'] == data].VarValue.reset_index(drop =True)
                else:
                    y0 = self.df.loc[self.df['VarName'] == data].VarValue.reset_index(drop =True)
                    y = y + y0

        # Plot data with color gradient
        color = cm.RdYlBu_r(y / max(y))
        plot = ax.scatter(x, y, color=color)
        sz = np.ones(x.size)
        plot.set_sizes(sz)

        # Set axis formatting
        ax.spines['bottom'].set_color(None)
        ax.get_xaxis().set_ticks([])
        ax.set_title(feature, fontsize=10, fontweight='bold', color='#e3e3e3')
        ax.set_ylabel(units, fontsize=10, color='#e3e3e3')
        ax.tick_params(axis="x", direction="out", which='major', width=0, length=15)
        ax.xaxis.set_major_locator(dates.DayLocator(interval=1))  # Show major tick every day
        ax.xaxis.set_major_formatter(dates.DateFormatter(""))  # Don't Show tick label

    # Adds a bubble with the feature requested. Bubbles are used to return a single value
    def add_bubble(self,feature):

        ax = self.fig.add_subplot(self.gs[self.index[0]:(self.index[0]+2), self.index[1]],frameon= True)

        # Updates to the correct index for future bubbles/plots
        if self.index[1]==2:
            self.index = (self.index[0]+2,0)
        else:
            self.index = (self.index[0],self.index[1]+1)

        # Creates and adds bubble
        box = patches.FancyBboxPatch((0.3, 0.3), width=0.4, height=0.4, boxstyle='circle, pad = 0.2',
                                         fc='#2B5AA0', ec = '#e3e3e3', zorder=1, alpha=0.8)
        ax.add_artist(box)

        # Handles the case for each possible feature
        # Evaluates for correct feature and prints out with descriptor and units on bubble
        if feature == "Inlet Purity" or feature == "Outlet Purity":
            value = self.purity(feature)
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
            value = round(run_hrs/hrs*100,2)
            ax.text(0.5, 0.6, 'Liquefier Run Time', ha='center', fontsize='x-large',
                    fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.4, str(value) + "%",
                    ha='center', fontsize='x-large', color='#e3e3e3')

        if feature == 'Recovery Rate':
            value = self.recovery_rate()
            ax.text(0.5, 0.7, 'Average', ha='center', fontsize='x-large',
                        fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.6, 'Liquefaction Rate', ha='center', fontsize='x-large',
                        fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.25, str(value) + '\n' + "Liters of Liquid" + "\n" + "Helium per Day",
                        ha='center', fontsize='x-large', color='#e3e3e3')

        if feature == 'Leak Rate':
            value = self.leak_rate()
            ax.text(0.5, 0.7, 'Average', ha='center', fontsize='x-large',
                        fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.6, 'Leak Rate', ha='center', fontsize='x-large',
                        fontweight='semibold', color='#e3e3e3')
            ax.text(0.5, 0.25, str(value)+" SLM",
                        ha='center', fontsize='x-large', color='#e3e3e3')

        # Set axis visibility
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    # Displays the figure
    def show(self):

        plt.show()

    # Returns average of purity values for requested feature
    def purity(self, feature):

        key = self.dic[feature]
        data = self.df.loc[self.df['VarName'] == key[0]].VarValue
        purity = np.mean(data)
        return purity

    # Returns the average cold head temp
    def ch_temp(self, feature):

        key = self.dic[feature]
        tags = key[0]
        full = 0
        for tag in tags:
            full += np.mean(self.df.loc[self.df['VarName'] == tag].VarValue)
        return full/len(tags)

    # Returns the average liquefaction rate
    def liq_rate(self):

        key = self.dic['Liquefier Inlet Flow']
        tags = key[0]

        # Integrates inlet flow to get total flow into liquefier
        value = 0
        for tag in tags:
            value += integrate(self.df.loc[self.df['VarName'] == tag].VarValue, 1/2)

        # Converts to liquid with expansion ratio
        liquid = value/745

        run_hrs, hrs = self.liq_runtime()
        return liquid / run_hrs * 24

    # Returns number of hours liquefier is on, and number of total hours
    def liq_runtime(self):

        key = self.dic['Liquefier State']
        states = self.df.loc[self.df['VarName'] == key[0]].VarValue.reset_index(drop=True)
        dt = self.dt('Liquefier State')

        # Iterates through dataframe to find total time, as well as total time liquefier is on (State 4)
        hrs = 0
        run_hrs = 0
        for state in states:
            hrs += dt
            if state == 4:
                run_hrs += dt

        run_hrs = round(run_hrs/60)
        hrs = round(hrs/60)
        return run_hrs, hrs

    # Returns the average number of gas bag cycles per day
    def gb_cycles(self):

        key = self.dic['Gas Bag Storage Level']
        heights = self.df.loc[self.df['VarName'] == key[0]].VarValue.reset_index(drop = True)

        # Records the number of times the gas bag passes a midpoint to get number of cycles
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

    # Returns average recovery rate
    def recovery_rate(self):

        key = self.dic['Liquefier Inlet Flow']
        tags = key[0]
        storage_key = "Medium Pressure Storage"

        # Get total volume leaving storage for liquefier
        out_flow = 0
        for tag in tags:
            out_flow += integrate(self.df.loc[self.df['VarName'] == tag].VarValue, self.dt("Liquefier Inlet Flow"))

        # Get estimate of volume leaked
        run_hrs, hrs = self.liq_runtime()
        leak = self.leak_rate()*hrs*60

        # Get total change in pressure over time period
        pressure_key = self.dic[storage_key][0]
        pressure = self.df.loc[self.df['VarName'] == pressure_key].VarValue.reset_index(drop = True)
        volume = (pressure[pressure.size - 1] - pressure[0])*self.dic[storage_key][2]  # Adjusts for volume of storage

        # Adjusts for pressure units
        if self.dic[storage_key][1] == 'kPa':
            volume = volume / 101.325

        # Compute total recovered volume
        recovered = volume + out_flow + leak
        liquid = recovered/745
        rate = (liquid/hrs)*24
        return round(rate, 1)

    # Return estimated leak rate. Does not account for leak back into PSA
    def leak_rate(self):

        # Pull down liquefier states
        liq_key = "Liquefier State"
        tag1 = self.dic[liq_key][0]
        liq_dates= (self.df.loc[self.df['VarName'] == tag1].TimeString).reset_index(drop = True)
        raw_states = (self.df.loc[self.df['VarName'] == tag1].VarValue).reset_index(drop = True)

        # Pull down storage values
        storage_key = "Medium Pressure Storage"
        tag2 = self.dic[storage_key][0]
        raw_pressure = (self.df.loc[self.df['VarName'] == tag2].VarValue).reset_index(drop = True)
        pres_dates = (self.df.loc[self.df['VarName'] == tag2].TimeString).reset_index(drop = True)

        # Return series of bools, true where liquefier state timestamp is also a storage timestamp
        # Data has to be pruned to account for different sampling rates
        # New states list is pruned to only include what is also in storage
        bools1 = liq_dates.isin(pres_dates)
        states=[]
        for i, boo in enumerate(bools1):
            if boo:
                states.append(raw_states[i])

        # Do the same thing as above, but true when storage timestamp is also in the revised liquefier timestamp
        # New pressure list is pruned to be the same lenght at states list
        bools2 = pres_dates.isin(liq_dates)
        pressures = []
        for i, boo in enumerate(bools2):
            if boo:
                pressures.append(raw_pressure[i])

        # Find pressures when liquefier is off
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

        # Find length of psa swing
        psa = self.psa_swing()

        # Find indices of peaks and valleys
        peak = []
        valley = []
        for i,list in enumerate(off_pressure):
            pdata, _ = signal.find_peaks(list, height=0, distance=15*psa)
            peak.append(pdata)
            flip = [num * -1 for num in list]
            pos = [num + max(list) for num in flip]
            vdata, _ = signal.find_peaks(pos, height=0, distance=15*psa)
            valley.append(vdata)

        # Find slope between peak and valley after pressure settles
        slopes = []
        for i in range(0, len(peak)):
            if len(valley[i])<2:
                pass
            elif (valley[i])[0]<(peak[i])[0]:
                rg = int((valley[i][1]-peak[i][0])/2)
                for index, j in enumerate(valley[i]):
                    if j!= 0:
                        stop = index
                        start = index-rg
                        y = off_pressure[i][start:stop]
                        m, b = trendline(y)
                        slopes.append(m)
            elif (valley[i])[0]>(peak[i])[0]:
                rg = int((valley[i][0]-peak[i][0])/2)
                for index, j in enumerate(valley[i]):
                    stop = index
                    start = index-rg
                    y = off_pressure[i][start:stop]
                    m, b = trendline(y)
                    slopes.append(m)

        # Find average slope and convert units to return
        xunit = self.dt(storage_key)
        storage = self.dic[storage_key][2]
        slope = sum(slopes)*storage/(len(slopes)*xunit)
        if self.dic[storage_key][1] == 'kPa':
            final = round((slope/101.325),2)
            return abs(final)

    # Return the time interval between samples
    def dt(self, feature):

        key = self.dic[feature][0]
        if type(key) == list:
            times = (self.df.loc[self.df['VarName'] == key[0]].TimeString).reset_index(drop=True)
            return (times[1] - times[0]) / timedelta(minutes=1)
        else:
            times = (self.df.loc[self.df['VarName'] == key].TimeString).reset_index(drop=True)
            return (times[1] - times[0]) / timedelta(minutes=1)

    # Return the average length of a PSA swing
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





# Basic discrete integration function
def integrate(vec, dt):

    value = 0
    for element in vec:
        value += dt * element
    return value

# Numpy trendline function
def trendline(y):

    x = np.arange(0, len(y))
    A = np.vstack([x, np.ones(len(x))])
    m, b = np.linalg.lstsq(A.T, y, rcond=None)[0]
    return m, b

# Example for loading the json
def load_project_json(proj_number: int) -> dict:
    # Location of the project's json
    path = f'Infographic Settings\{proj_number}.json'
    
    # Open json and load as a dictionary
    with open(path, 'r') as json_file:
        settings = json.load(json_file)
    
    # Return the json dictionary
    return settings











