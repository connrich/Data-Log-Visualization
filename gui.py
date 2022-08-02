'''
Standard Python packages
'''
import sys
from datetime import datetime
import os
import json

'''
PyQt packages
'''
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QMenuBar, \
                            QAction, QFileDialog, QScrollArea, QToolBar, \
                            QCheckBox, QPushButton, QDateTimeEdit, QLabel
from PyQt5.QtCore import Qt, QPointF, QDateTime

'''
Data analysis packages
'''
import pandas as pd

'''
Custom packages
'''
from data_object import Data
from gui_resources.graph_widget import GraphWidget
from gui_resources.data_selection_widget import DataSelectionWidget
from gui_resources.settings_window import SettingsWindow
from gui_resources.style import StyleSheet as SS
from gui_resources.error_message import ErrorMessage



class MainWindow(QMainWindow):
    '''
    The main GUI window used for the application
    '''
    def __init__(self) -> None:
        super().__init__()

        # Global application settings
        self.loadSettings()

        # Main window settings
        self.setWindowTitle('Trends')

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
        self.loadedData = {}
    
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

        # Add action for opening settings window
        self.SettingsAction = QAction('Settings')
        self.SettingsAction.triggered.connect(self.SettingsWindow.showWindow)
        self.MenuBar.addAction(self.SettingsAction)

        # Add action for loading a dataset
        self.loadDataAction = QAction('Load Dataset')
        self.loadDataAction.triggered.connect(
            lambda: self.loadData(QFileDialog.getOpenFileName()[0])
            )
        self.MenuBar.addAction(self.loadDataAction)

        # Add action for showing data selection widget
        self.dataSelectionShow = QAction('Open Data Selection')
        self.dataSelectionShow.triggered.connect(self.DataSelectionDock.show)
        self.MenuBar.addAction(self.dataSelectionShow)

        # Add action for generating an infographic
        self.generateInfographicAction = QAction('Generate Infographic')
        self.generateInfographicAction.triggered.connect(self.generateInfographic)
        self.MenuBar.addAction(self.generateInfographicAction)
    
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
            ErrorMessage('Invalid date/time range. Check you start and end date/time.')
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

        # If load was succesful we can clear old data and the graph
        self.clearLoadedDatasets()
        self.GraphWidget.clear()

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

    def onMouseMoved(self, point: QPointF) -> None:
        '''
        Slot for getting mouse coordinates over the graph widget
        '''
        # Get a point object containing coordinates mapped to the graph view space
        p = self.GraphWidget.getPlotItem().vb.mapSceneToView(point)

        # Try formatting x value to a date/time format
        try:
            x_val = str(datetime.fromtimestamp(p.x()).strftime('%m/%d/%Y %H:%M:%S'))
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
        # Add infographic functionality here
        return 



class DateTimeInput(QDateTimeEdit):
    ''''
    Custom subclass for inputting date/time
    '''
    def __init__(self, format:str ="MM/dd/yyyy HH:mm") -> None:
        super().__init__()

        # Set minimum size so full date and time can be seen
        self.setMinimumWidth(100)

        # Set how the date/time is displayed 
        if format is not None: 
            self.setDisplayFormat(format)
        
        # Show a calendar when clicked 
        self.setCalendarPopup(True)
        
        # Default to the current date and time 
        self.setDateTime(QDateTime.currentDateTime())

    def getUNIX(self) -> int:
        """
        Returns the current date/time in UNIX integer format
        """
        return self.dateTime().toTime_t()


if __name__ == '__main__':
    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Initialize application
    app = QApplication(sys.argv)
    # Create window
    MainWindow = MainWindow()
    MainWindow.show()

    # Terminated when the application is closed 
    sys.exit(app.exec())