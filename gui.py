import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QMenuBar, QMenu, QAction, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import pandas as pd
from datetime import datetime




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window settings
        self.setWindowTitle('Trends')
        self.setMinimumSize(800, 800)

        # Add graphing widget
        self.GraphWidget = GraphWidget()
        self.setCentralWidget(self.GraphWidget)

        # Initialize data structures
        self.loadedData = {}

        # Load a csv file 
        self.loadData('System_Sensor_log0.csv')

        # Plot a data set
        self.GraphWidget.plot(
            self.loadedData['TE510B_Value'].index, 
            self.loadedData['TE510B_Value']['VarValue'].to_list(),
            pen=pg.mkPen('blue')
            )
        
        # Plot a data set
        self.GraphWidget.plot(
            self.loadedData['TE511A_Value'].index, 
            self.loadedData['TE511A_Value']['VarValue'].to_list(),
            pen=pg.mkPen('red')
            )
            

    def loadData(self, path):
        # Read the CSV file at the path
        df = pd.read_csv(path, delimiter=';', low_memory=False, decimal=',')

        # Convert times to Pandas TimeStamp
        df['TimeString'] = pd.to_datetime(df['TimeString'], format='%d.%m.%Y %H:%M:%S')
        # Convert times to UNIX integer format 
        df['TimeString'] = df['TimeString'].map(pd.Timestamp.timestamp)

        # Pivot the dataframe so it is easier to select data by tag name
        table = pd.pivot_table(data=df, index=['VarName', 'TimeString'])

        # Find all unique device tags and store the data in a dictionary
        # Dictionary key = tag string
        # Dictionary value = dataframe with time and device value
        for i in table.index.unique(level='VarName'):
            self.loadedData[i] = table.loc[(i, )]
        print(self.loadedData.keys())

    def clearLoadedData(self):
        self.loadedData = {}

    def loadNewData(self, path):
        self.clearLoadedData()
        self.loadData(path)



class GraphWidget(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        
        # Set the graph background 
        self.setBackground('w')
        self.showGrid(x=True, y=True)

        # Set graph title
        self.setTitle('Trends', color='black')

        self.xaxis = TimeAxisItem('bottom')
        self.setAxisItems({'bottom': self.xaxis})

        # Set axis labels
        self.setLabel('left', 'Value', color='black')
        self.setLabel('bottom', 'Time', color='black')

        # Set axis colors
        self.getAxis('left').setPen('black')
        self.getAxis('left').setTextPen('black')
        self.getAxis('bottom').setPen('black')
        self.getAxis('bottom').setTextPen('black')


# Used for displaying date/time format for x-axis ticks
class TimeAxisItem(pg.AxisItem):
    def __init__(self, placement):
        super(TimeAxisItem, self).__init__(placement)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [str(datetime.fromtimestamp(value).strftime('%d.%m.%Y %H:%M:%S')) for value in values]



if __name__ == '__main__':
    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Initialize application
    app = QApplication(sys.argv)
    # Create window
    MainWindow = MainWindow()
    MainWindow.show()
    # Terminated when the application is closed 
    sys.exit(app.exec())