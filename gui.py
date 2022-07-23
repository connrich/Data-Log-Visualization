import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QMenuBar, \
                            QAction, QFileDialog, QScrollArea
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
from datetime import datetime

from gui_resources.graph_widget import GraphWidget
from gui_resources.data_selection_widget import DataSelectionWidget, DataSet
from gui_resources.style import StyleSheet as SS



class MainWindow(QMainWindow):
    '''
    The main GUI window used for the application
    '''
    def __init__(self):
        super().__init__()

        # Main window settings
        self.setWindowTitle('Trends')
        self.setMinimumSize(800, 800)

        # Add graphing widget
        self.GraphWidget = GraphWidget()
        self.setCentralWidget(self.GraphWidget)

        # Construct the dock used for selecting data sets to display
        self.constructDataSelectionDock()

        # Constructs top menu 
        self.constructMenu()

        # Initialize data structures
        self.loadedData = {}

        # Load a csv file 
        self.loadData('System_Sensor_log0.csv')
            
    def constructDataSelectionDock(self):
        '''
        Initial construction for data selection dock widget
        '''
        # Construct dock widget
        self.DataSelectionDock = QDockWidget()
        self.DataSelectionDock.setWindowTitle('Data Selection')
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.DataSelectionDock)

        # Set dock widget settings
        self.DataSelectionDock.setAllowedAreas(
            Qt.DockWidgetArea.RightDockWidgetArea |
            Qt.DockWidgetArea.LeftDockWidgetArea
        )

        # Construct scrollable area for data sets
        self.DockScrollArea = QScrollArea()
        self.DockScrollArea.setStyleSheet(SS.scroll_area)
        self.DockScrollArea.setWidgetResizable(True)
        self.DataSelectionDock.setWidget(self.DockScrollArea)

        # Construct data selection widget which holds data sets
        self.DataSelectionWidget = DataSelectionWidget(graph=self.GraphWidget)

        # Place the data selection widget in the scroll area 
        self.DockScrollArea.setWidget(self.DataSelectionWidget)
    
    def constructMenu(self):
        '''
        Initial construction for menu
        '''
        # Create menu bar
        self.MenuBar = QMenuBar()
        self.setMenuBar(self.MenuBar)

        # Add action for loading a dataset
        self.loadDataAction = QAction('Load Dataset')
        self.loadDataAction.triggered.connect(
            lambda: self.loadData(QFileDialog.getOpenFileName()[0])
        )
        # lambda: self.loadData(QFileDialog.getOpenFileName()[0].split('/')[-1])
        self.MenuBar.addAction(self.loadDataAction)

        # Add action for showing data selection widget
        self.dataSelectionShow = QAction('Open Data Selection')
        self.dataSelectionShow.triggered.connect(self.DataSelectionDock.show)
        self.MenuBar.addAction(self.dataSelectionShow)

    def loadData(self, path):
        '''
        Loads new CSV data into the application
        Clears the previously loaded data
        '''
        # Clear old data before loading new data
        self.clearLoadedDatasets()

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
        for name in table.index.unique(level='VarName'):
            self.loadedData[name] = table.loc[(name, )]
            self.DataSelectionWidget.addDataSet(name, self.loadedData[name], self.GraphWidget)

    def clearLoadedDatasets(self):
        '''
        Clears all loaded data
        '''
        self.loadedData = {}
        self.DataSelectionWidget.clearDatasets()



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