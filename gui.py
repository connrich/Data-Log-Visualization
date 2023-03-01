'''
Standard Python packages
'''
import sys
from datetime import datetime
import os
import json
import ctypes
from platform import system
import pickle

'''
PyQt packages
'''
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QMenuBar, \
                            QAction, QFileDialog, QScrollArea, QToolBar, \
                            QCheckBox, QPushButton, QLabel, QMenu
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QIcon, QCloseEvent

'''
Data analysis packages
'''
import pandas as pd

'''
Custom packages
'''
from gui_resources.graph_widget import GraphWidget
from gui_resources.data_selection_widget import DataSelectionWidget
from gui_resources.settings_window import SettingsWindow
from gui_resources.style import StyleSheet as SS
from gui_resources.error_message import ErrorMessage
from gui_resources.infographic_options_page import InfographicOptions
from gui_resources.date_time_input_widget import DateTimeInput
from gui_resources.resource_path import resource_path



class MainWindow(QMainWindow):
    '''
    The main GUI window used for the application
    '''
    def __init__(self) -> None:
        super().__init__()

        # Global application settings
        self.loadSettings()

        # Main window settings
        self.setWindowTitle('QuantumView')
        self.setWindowIcon(QIcon(resource_path('gui_resources\Quantum_icon.png')))

        # Add graphing widget
        self.GraphWidget = GraphWidget()
        # Connect slot for getting coordinates when hovering over graph 
        self.GraphWidget.getPlotItem().scene().sigMouseMoved.connect(self.onMouseMoved)
        self.setCentralWidget(self.GraphWidget)

        # Construct the dock used for selecting data sets to display
        self.constructDataSelectionDock()

        # Constructs top menu 
        self.constructMenu()

        # Constructs tool bar
        self.constructToolBar()

        # Initialize data structures
        self.loadedData = None

        # Initialize infographic generation window 
        self.InfographicWindow = InfographicOptions(main_window=self)
    
    def loadSettings(self) -> None:
        '''
        Loads in settings from a json file and constructs the settings window
        '''
        # Load settings from json
        with open(os.path.join(os.path.dirname(__file__), 'gui_resources\\settings.json'), 'r') as json_file:
            self.settings = json.load(json_file)

        # Construct settings window
        self.SettingsWindow = SettingsWindow(settings=self.settings)

    def constructDataSelectionDock(self) -> None:
        '''
        Initial construction for data selection dock widget
        '''
        # Construct dock widget
        self.DataSelectionDock = QDockWidget()
        self.DataSelectionDock.setWindowTitle('Data Selection')
        self.DataSelectionDock.setMinimumWidth(200)
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

        # Add 'File' meu option
        self.FileMenu = QMenu('File')
        self.MenuBar.addMenu(self.FileMenu)

        # Add 'Edit' menu option
        self.EditMenu = QMenu('Data')
        self.MenuBar.addMenu(self.EditMenu)

        # Add 'View' menu option
        self.ViewMenu = QMenu('View')
        self.MenuBar.addMenu(self.ViewMenu)

        # Add action for opening settings window
        self.SettingsAction = QAction('Settings')
        self.SettingsAction.triggered.connect(self.SettingsWindow.show)
        self.FileMenu.addAction(self.SettingsAction)

        # Add action for loading a dataset
        self.loadDataAction = QAction('Load Dataset')
        self.loadDataAction.triggered.connect(
            lambda: self.loadData(QFileDialog.getOpenFileName()[0])
            )
        self.EditMenu.addAction(self.loadDataAction)

        # Add action for clearing loaded dataset
        self.clearDatasetAction = QAction('Clear Dataset')
        self.clearDatasetAction.triggered.connect(self.clearLoadedDatasets)
        self.EditMenu.addAction(self.clearDatasetAction)

        # Add action for showing data selection widget
        self.dataSelectionShow = QAction('Show Data Selection Menu')
        self.dataSelectionShow.triggered.connect(self.DataSelectionDock.show)
        self.ViewMenu.addAction(self.dataSelectionShow)

        # Add action for generating an infographic
        self.generateInfographicAction = QAction('Generate Infographic')
        self.generateInfographicAction.triggered.connect(self.generateInfographic)
        self.FileMenu.addAction(self.generateInfographicAction)
    
    def constructToolBar(self) -> None:
        '''
        Initial construction for tool bar
        '''
        # Create tool bar
        self.ToolBar = QToolBar()
        self.addToolBar(self.ToolBar)

        # Clear all shown data 
        self.ClearGraph = QPushButton('Clear Graph')
        self.ClearGraph.clicked.connect(self.DataSelectionWidget.clearGraph)
        self.ToolBar.addWidget(self.ClearGraph)

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
        
        # Add option to show legend
        self.ShowLegend = QCheckBox('Show legend')
        self.ShowLegend.clicked.connect(lambda: self.GraphWidget.showLegend(self.ShowLegend.isChecked()))
        self.ToolBar.addWidget(self.ShowLegend)
        self.ToolBar.addSeparator()

        # Start date/time to show on graph
        self.StartTimeLabel = QLabel('   Start Time: ')
        self.ToolBar.addWidget(self.StartTimeLabel)
        self.StartTime = DateTimeInput()
        self.ToolBar.addWidget(self.StartTime)

        # End date/time to show on graph
        self.EndTimeLabel = QLabel('   End Time: ')
        self.ToolBar.addWidget(self.EndTimeLabel)
        self.EndTime = DateTimeInput()
        self.ToolBar.addWidget(self.EndTime)

        # Button for applying the date/time range
        self.SetXRange = QPushButton('Set Range')
        self.SetXRange.clicked.connect(self.scaleXRange)
        self.ToolBar.addWidget(self.SetXRange)
        self.ToolBar.addSeparator()

    def scaleXRange(self) -> None:
        '''
        Scales the x axis to a particular range using UNIX timestamps
        Connected to start and end time DateTimeEdit widgets
        '''
        # Get range from date/time inputs 
        lower_unix = self.StartTime.getUNIX()
        upper_unix = self.EndTime.getUNIX()

        # Verfiy time range
        if lower_unix > upper_unix:
            ErrorMessage('Invalid date/time range. Check your start and end date/time.')
            return

        # Set the new x range on the graph
        self.GraphWidget.setXRange(lower_unix, upper_unix)

        # Scale y axis to fit data
        self.GraphWidget.enableAutoRange(axis='y')

    def loadData(self, path: str) -> None:
        '''
        Loads new CSV data into the application
        Clears the previously loaded data
        '''
        # Check if path is empty
        if path == '':
            return

        # Get the type of file
        filetype = path.split('/')[-1].split('.')[-1]

        # Import depending on file type
        if filetype == 'pickle':
            df = ''
            try:
                with open(path, "rb") as f:
                    df = pickle.load(f)
            except Exception as ex:
                print("Error during unpickling object (Possibly unsupported): ", ex)
            #dates to UNIX
            df[self.settings['time_header_title']] = df[self.settings['time_header_title']].map(pd.Timestamp.timestamp)
        elif filetype == 'csv':
            try:
                # Read the CSV file at the path
                # Also catches on_bad_lines/error_bad_lines deprecation error
                # on_bad_lines is Pandas version 1.3.0+
                try:
                    df = pd.read_csv(path, 
                        delimiter=self.settings['delimiter'],
                        decimal=self.settings['decimal'], 
                        low_memory=False,
                        on_bad_lines='skip')
                except Exception as ex:
                    df = pd.read_csv(path, 
                        delimiter=self.settings['delimiter'],
                        decimal=self.settings['decimal'], 
                        low_memory=False,
                        error_bad_lines=False)

                # Catch empty data frame
                if df.empty:
                    raise Exception('Loaded csv file is empty')

                # Convert times to Pandas TimeStamp, removes failed conversions 
                date_time_format = self.settings['date_time_format']
                time_header_title = self.settings['time_header_title']
                df[time_header_title] = pd.to_datetime(df[time_header_title], format=date_time_format, errors='coerce')
                df = df.dropna(subset=[time_header_title])

                if df.empty:
                    raise Exception((
                        f'Error with date/time formatting \n'
                        f'Current format: {date_time_format}'
                        ))
                # Convert times to UNIX integer format 
                df[time_header_title] = df[time_header_title].map(pd.Timestamp.timestamp)

            except Exception as ex:
                ErrorMessage(f"Failed to load csv file. \nException:  {ex} \n\nAlso check if the correct delimiter and decimal character have been selected in settings. \n \
                            Current delimiter:   {self.settings['delimiter']} \n \
                            Current decimal:   {self.settings['decimal']} ")
                return
        else:
            ErrorMessage(f'Invalid file type: {filetype} \nOnly accepts csv or pickle data frames')
            return

        # If load was succesful we can clear old data and the graph
        self.clearLoadedDatasets()
        self.GraphWidget.clear()

        # Save new data
        self.loadedData = df

        # Check if the data is from a Siemens log
        # If it is we pivot it so it is easier to work with
        if 'VarName' in df.columns:
            # Pivot the dataframe so it is easier to select data by tag name
            pivot_table = pd.pivot_table(data=df, index=['VarName', 'TimeString'])

            # Find all unique device tags and store the data in a dictionary
            # Dictionary key = tag string
            # Dictionary value = dataframe with time and device value
            for name in pivot_table.index.unique(level='VarName'):
                self.DataSelectionWidget.addDataSet(name, pivot_table.loc[(name, )], self.GraphWidget)
        else:
            for name in df.columns:
                self.DataSelectionWidget.addDataSet(name, df, self.GraphWidget)


    def clearLoadedDatasets(self) -> None:
        '''
        Clears all loaded data
        '''
        self.loadedData = {}
        self.DataSelectionWidget.clearDatasets()
        self.GraphWidget.clear()

    def onMouseMoved(self, point: QPointF) -> None:
        '''
        Slot for getting mouse coordinates over the graph widget
        '''
        # Get a point object containing coordinates mapped to the graph view space
        p = self.GraphWidget.getPlotItem().vb.mapSceneToView(point)

        # Try formatting x value to a date/time format
        try:
            x_val = str(datetime.utcfromtimestamp(p.x()).strftime('%m/%d/%Y %H:%M:%S'))
        except:
            x_val = p.x()
        
        # Display the coordinates on the bottom status bar
        self.statusBar().showMessage(
                "[x], (y) = [{}],   ({:0.5f})".format(x_val, p.y())
            )
    
    def generateInfographic(self) -> None:
        '''
        Generates an infographic and displays the output
        '''
        if self.loadedData is None or self.loadedData.empty:
             ErrorMessage('No data is currently loaded. Please load data and try again.')
        else:
            self.InfographicWindow.show()
        return
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        '''
        Overwrite of close event to close the other windows
        '''
        self.InfographicWindow.close()
        self.SettingsWindow.close()
        return super().closeEvent(a0)



if __name__ == '__main__':
    # Needed to set task bar icon on Windows
    if system() == 'Windows':
        myappid = 'Quantum_Data_logger'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Initialize application
    app = QApplication(sys.argv)

    # Create window
    MainWindow = MainWindow()
    MainWindow.show()

    # MainWindow.loadData("P619_2022_05_020.csv")
    # MainWindow.loadData("Logs/System_Sensor_log0.csv")

    # Terminated when the application is closed 
    sys.exit(app.exec())