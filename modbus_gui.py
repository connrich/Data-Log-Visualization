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
from gui_resources.resource_path import resource_path
from gui_resources.menu_text_input import MenuTextInputWidget
from gui_resources.graph_selection_widget import ButtonGrid
from modbus_resources.ModbusLogging import ModbusLogger



class MODBUS_GUI(QMainWindow):
    '''
    The main GUI window used for the Modbus viewer/logger
    '''
    def __init__(self) -> None:
        super().__init__()

        # Modbus class for data/connection management
        self.Logger = ModbusLogger()

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
    
    def constructMenuBar(self) -> None:
        # Create/add menu bar
        self.MenuBar = QMenuBar()
        self.setMenuBar(self.MenuBar)

        # Create/construct connection menu
        self.ConnectMenu = QMenu('Connect')
        self.constructConnectMenu()
        self.MenuBar.addMenu(self.ConnectMenu)

        # Create/construct view menu
        self.ViewMenu = QMenu('View')
        self.constructViewMenu()
        self.MenuBar.addMenu(self.ViewMenu)

    def constructConnectMenu(self) -> None:
        # Input for server IP
        self.ipInput = MenuTextInputWidget('Server IP')
        self.ConnectMenu.addAction(self.ipInput)

        # Input for port number
        self.portInput = MenuTextInputWidget('Port Number')
        self.ConnectMenu.addAction(self.portInput)

        # Input for unit id
        self.unitIdInput = MenuTextInputWidget('Unit Id')
        self.ConnectMenu.addAction(self.unitIdInput)

        # Button to try initialize connection
        self.connectButton = QPushButton('Connect')
        self.connectAction = QWidgetAction(self.connectButton)
        self.connectAction.setDefaultWidget(self.connectButton)
        self.ConnectMenu.addAction(self.connectAction)

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
        # self.numGraphs.currentTextChanged.connect(lambda num: self.Graphs.showGraphs(int(num)))


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
        # self.hideAllGraphs()
        print(row, col)
    
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

    window = MODBUS_GUI()

    window.show()

    sys.exit(app.exec())