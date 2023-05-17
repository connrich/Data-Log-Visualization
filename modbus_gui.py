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
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, \
                            QAction, QFileDialog, QGridLayout, QToolBar, \
                            QCheckBox, QPushButton, QLabel, QMenuBar, QMenu, \
                            QWidgetAction, QLineEdit, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QPointF, QTimer
from PyQt5.QtGui import QIcon, QCloseEvent

'''
Data analysis packages
'''
import pandas as pd

'''
Custom packages
'''
from gui_resources.graph_widget import GraphWidget
from gui_resources.resource_path import resource_path
from gui_resources.menu_input import MenuTextInputWidget, MenuComboInputWidget
from gui_resources.graph_layout_widget import ButtonGrid
from gui_resources.channel_selection_widget import ChannelSelectionWidget
from modbus_resources.ModbusLogging import ModbusLogger



class ModbusGui(QMainWindow):
    '''
    The main GUI window used for the Modbus viewer/logger
    '''
    def __init__(self) -> None:
        super().__init__()

        # Modbus class for data/connection management
        self.Logger = ModbusLogger(tag_map=[0 for _ in range(60)])
        self.pollTimer = QTimer()
        self.pollTimer.timeout.connect(lambda: print(self.Logger.readAllRegisters()))
        self.pollTimer.setInterval(1000)

        # Main window settings
        self.setWindowTitle('QuantumView')
        self.setWindowIcon(QIcon(resource_path('gui_resources\images\Quantum_icon.png')))

        # Construct and add the multigraph widget to the window
        #TODO implement across all classes
        self.GraphArraySize = (3, 3)
        self.Graphs = MultiGraphWidget()
        self.setCentralWidget(self.Graphs)

        # Construct and add the menu to the window
        self.constructMenuBar()

        # Construct and add the tool bar to the window
        self.constructToolbar()

        # Construct channel selection widget
        self.ChannelSelectionWidget = ChannelSelectionWidget(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.ChannelSelectionWidget)
    
    def constructMenuBar(self) -> None:
        # Create/add menu bar
        self.MenuBar = QMenuBar()
        self.setMenuBar(self.MenuBar)

        # Create/construct connection menu
        self.ConnectMenu = QMenu('Connect')
        self.constructConnectMenu()
        self.MenuBar.addMenu(self.ConnectMenu)

        # Create/construct settings menu
        self.SettingsMenu = QMenu('Settings')
        self.constructSettingsMenu()
        self.MenuBar.addMenu(self.SettingsMenu)

        # Create/construct view menu
        self.ViewMenu = QMenu('View')
        self.constructViewMenu()
        self.MenuBar.addMenu(self.ViewMenu)

    def constructConnectMenu(self) -> None:
        # Input for server IP
        self.ipInput = MenuTextInputWidget('Server IP')
        self.ipInput.setText('192.168.0.1')
        self.ConnectMenu.addAction(self.ipInput)

        # Input for port number
        self.portInput = MenuTextInputWidget('Port Number')
        self.portInput.setText('503')
        self.ConnectMenu.addAction(self.portInput)

        # Input for unit id
        self.unitIdInput = MenuTextInputWidget('Unit Id')
        self.unitIdInput.setText('2')
        self.ConnectMenu.addAction(self.unitIdInput)

        # Tag map selection
        self.tagMapCombo = MenuComboInputWidget('Select tag map')
        for file in os.listdir("modbus_resources\\Tag Maps"):
            if '.json' in file:
                self.tagMapCombo.addItem(os.path.splitext(file)[0])
        self.ConnectMenu.addAction(self.tagMapCombo)

        # Button to try initialize connection
        self.connectButton = QPushButton('Connect')
        self.connectButton.clicked.connect(self.connectModbus)
        self.connectAction = QWidgetAction(self.connectButton)
        self.connectAction.setDefaultWidget(self.connectButton)
        self.ConnectMenu.addAction(self.connectAction)
    
    def constructSettingsMenu(self) -> None:        
        # Checkbox for enabling logging
        self.enableLogging = QCheckBox(' Enable logging')
        self.enableLoggingAction = QWidgetAction(self.enableLogging)
        self.enableLoggingAction.setDefaultWidget(self.enableLogging)
        self.SettingsMenu.addAction(self.enableLoggingAction)

        # Path to log file
        self.logPathInput = MenuTextInputWidget('Log Path')
        self.SettingsMenu.addAction(self.logPathInput)

    def constructViewMenu(self) -> None:
        # Construct the button selector for graph display
        self.GraphView = ButtonGrid(*self.GraphArraySize, self.Graphs)
        self.GraphViewContainer = QWidgetAction(self.GraphView)
        self.GraphViewContainer.setDefaultWidget(self.GraphView)
        self.ViewMenu.addAction(self.GraphViewContainer)

    def constructToolbar(self) -> None:
        pass
        # # Create/add the toolbar
        # self.ToolBar = QToolBar()
        # self.addToolBar(self.ToolBar)

        # # Add options for number of displayed graphs
        # self.numGraphs = QComboBox()
        # self.ToolBar.addWidget(self.numGraphs)
        # self.numGraphs.addItem('1')
        # self.numGraphs.addItem('9')
        # self.numGraphs.currentTextChanged.connect(lambda num: self.Graphs.,(int(num)))
    
    def connectModbus(self) -> None:
        # Connect to logger using the settings
        self.Logger.connect(
            ip=self.ipInput.text(),
            port=int(self.portInput.text()),
            unit_id=int(self.unitIdInput.text())
        )

        # Start timer
        #TODO temporary
        self.pollTimer.start()
      


class MultiGraphWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Set layout of widget
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Iteratively create graphs
        self.initGraphs()

    def initGraphs(self) -> None:
        '''
        Initializes the graphs in the layout
        '''
        # Create 12 graphs and add them to the layout
        for row in range(3):
            self.layout.setRowStretch(row, 1)
            self.layout.setColumnStretch(row, 1)
            for col in range(3):
                graph = GraphWidget()
                graph.hide()
                self.layout.addWidget(graph, row, col)
        self.showAllGraphs()

    def graphAt(self, row: int, col: int) -> GraphWidget:
        '''
        Returns the graph widget at the coordinate
        (0, 0) is top left
        '''
        return self.layout.itemAtPosition(row, col).widget() 

    def showGraphs(self, row, col) -> None:
        '''
        Show a certain array of graphs 
        '''
        # Start by hising everything and then show what is needed
        self.hideAllGraphs()

        # Reset stretches
        for i in range(row+1):
            self.layout.setRowStretch(i, 1)
        for i in range(col+1):
            self.layout.setColumnStretch(i, 1)
        
        # Show all relevant graphs
        for i in range(row+1):
            for j in range(col+1):
                self.graphAt(i, j).show()
    
    def hideAllGraphs(self) -> None:
        '''
        Hides all graphs and reset row/column stretch
        '''
        # Reset column stretch
        for i in range(self.layout.columnCount()):
            self.layout.setColumnStretch(i, 0)
        
        # Reset row stretch
        for i in range(self.layout.rowCount()):
            self.layout.setRowStretch(i, 0)
        
        # Hide all widgets
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().hide()
    
    def showAllGraphs(self) -> None:
        '''
        Shows all graphs
        '''
        # Set column stretch
        for i in range(self.layout.columnCount()):
            self.layout.setColumnStretch(i, 1)
        
        # Set row stretch
        for i in range(self.layout.rowCount()):
            self.layout.setRowStretch(i, 1)
        
        # Show all widgets
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().show()



if __name__ == '__main__':
    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Create the appliction instance
    app = QApplication(sys.argv)

    window = ModbusGui()

    window.show()

    sys.exit(app.exec())
