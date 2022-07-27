from data_object import Data
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as dates
import datetime

file = Data(607)
table = file.pivot()
#'2022-07-24 19:55:32'
#'2022-07-26 15:25:40'

dic = {}
for i in table.index.unique(level='VarName'):
    dic[i] = table.loc[(i,)]

startdate = datetime.datetime.strptime('2022-07-25 8:55:32','%Y-%m-%d %H:%M:%S')
enddate = datetime.datetime.strptime('2022-07-26 15:25:40','%Y-%m-%d %H:%M:%S')

fig,ax = plt.subplots()
fully = table['VarValue']['PT270_Value'].to_list()
fullx = (dic['PT270_Value'].index).to_pydatetime()
x_data = np.array((dic['PT270_Value'].index))

y = []
x = []
for i in range(0,len(x_data)):
    if  startdate<= fullx[i] <= enddate:
        x.append(fullx[i])
        y.append(fully[i])
x1 = np.arange(0,len(x))
A = np.vstack([x1,np.ones(len(x))])

m, b = np.linalg.lstsq(A.T, y, rcond = None)[0]
plt.plot(fullx,fully,label='Original Data')
plt.plot(x,m*x1+b,'r',label="Fitted Line")
ax.plot_date(fullx, fully, '-')

ax.xaxis.set_minor_locator(dates.HourLocator(interval=2))   # every 4 hours
ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
ax.xaxis.set_major_locator(dates.DayLocator(interval=1))    # every day
ax.xaxis.set_major_formatter(dates.DateFormatter('\n%m-%d-%Y'))

plt.legend()
plt.show()