import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QMenuBar, \
                            QAction, QFileDialog, QScrollArea, QToolBar, \
                            QCheckBox, QPushButton
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
from datetime import datetime
import os
import json
from data_object import Data
from gui_resources.graph_widget import GraphWidget
from gui_resources.data_selection_widget import DataSelectionWidget, DataSet
from gui_resources.settings_window import SettingsWindow
from gui_resources.style import StyleSheet as SS
from gui_resources.error_message import ErrorMessage



class MainWindow(QMainWindow):
    '''
    The main GUI window used for the application
    '''
    def __init__(self):
        super().__init__()

        # Global application settings
        self.loadSettings()

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

        # Constructs tool bar
        self.constructToolBar()

        # Initialize data structures
        self.loadedData = {}

        # # Load a csv file 
        # self.loadData('System_Sensor_log0.csv')
    
    def loadSettings(self) -> None:
        '''
        Loads in settings from a json file and constructs the settings window
        '''
        # Load settings from json
        with open(os.path.join(os.path.dirname(__file__), 'gui_resources\\settings.json'), 'r') as json_file:
            self.settings = json.load(json_file)

        # Construct settings window
        self.SettingsWindow = SettingsWindow(settings=self.settings)
        # self.SettingsWindow.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'Resources\\SettingsGear.png')))

    def constructDataSelectionDock(self) -> None:
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
    
    def constructMenu(self) -> None:
        '''
        Initial construction for menu
        '''
        # Create menu bar
        self.MenuBar = QMenuBar()
        self.setMenuBar(self.MenuBar)

        # Add action for opening settings window
        self.SettingsAction = QAction('Settings')
        self.SettingsAction.triggered.connect(self.SettingsWindow.showWindow)
        self.MenuBar.addAction(self.SettingsAction)

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
    
    def constructToolBar(self):
        '''
        Initial construction for tool bar
        '''
        # Create tool bar
        self.ToolBar = QToolBar()
        self.addToolBar(self.ToolBar)

        # Scale to fit all data in graph view
        self.AutoScale = QPushButton('Auto Scale')
        self.AutoScale.clicked.connect(self.GraphWidget.getViewBox().autoRange)
        self.ToolBar.addWidget(self.AutoScale)
        self.ToolBar.addSeparator()

        # Freeze x axis zooming
        self.LockXAxis = QCheckBox('Freeze X axis')
        self.LockXAxis.clicked.connect(lambda: self.GraphWidget.setMouseEnabled(x=(not self.LockXAxis.isChecked())))
        self.ToolBar.addWidget(self.LockXAxis)

        # Feeze y axis zooming 
        self.LockYAxis = QCheckBox('Freeze Y axis')
        self.LockYAxis.clicked.connect(lambda: self.GraphWidget.setMouseEnabled(y=(not self.LockYAxis.isChecked())))
        self.ToolBar.addWidget(self.LockYAxis)
        self.ToolBar.addSeparator()

    def loadData(self, path: str) -> None:
        '''
        Loads new CSV data into the application
        Clears the previously loaded data
        '''
        # Clear old data before loading new data
        self.clearLoadedDatasets()

        # Get the type of file
        filetype = path.split('/')[-1].split('.')[-1]

        # Import depending on file type
        if filetype == 'pickle':
            file = Data(607)
            #loads pivoted dataframe
            df = file.display()
            #dates to UNIX
            df['TimeString'] = df['TimeString'].map(pd.Timestamp.timestamp)
        elif filetype == 'csv':
            try:
                # Read the CSV file at the path
                df = pd.read_csv(path, 
                                delimiter=self.settings['delimiter'],
                                decimal=self.settings['decimal'], 
                                low_memory=False)
                # Convert times to Pandas TimeStamp
                df['TimeString'] = pd.to_datetime(df['TimeString'], format='%d.%m.%Y %H:%M:%S')
                # Convert times to UNIX integer format 
                df['TimeString'] = df['TimeString'].map(pd.Timestamp.timestamp)
            except Exception as ex:
                ErrorMessage(f"Failed to load csv file. Check the correct delimiter and decimal character have been selected in settings. \n \
                            Current delimiter:   {self.settings['delimiter']} \n \
                            Current decimal:   {self.settings['decimal']}")
                return
        else:
            ErrorMessage(f'Invalid file type: {filetype} \n Only accepts csv or pickle data frames')
            return

        # Pivot the dataframe so it is easier to select data by tag name
        table = pd.pivot_table(data=df, index=['VarName', 'TimeString'])

        # Find all unique device tags and store the data in a dictionary
        # Dictionary key = tag string
        # Dictionary value = dataframe with time and device value
        for name in table.index.unique(level='VarName'):
            self.loadedData[name] = table.loc[(name, )]
            self.DataSelectionWidget.addDataSet(name, self.loadedData[name], self.GraphWidget)

    def clearLoadedDatasets(self) -> None:
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