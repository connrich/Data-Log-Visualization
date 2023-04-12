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
                            QWidgetAction, QLineEdit, QVBoxLayout
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
from gui_resources.style import StyleSheet as SS
from gui_resources.error_message import ErrorMessage
from gui_resources.date_time_input_widget import DateTimeInput
from gui_resources.resource_path import resource_path
from gui_resources.menu_text_input import MenuTextInputWidget
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

        # Construct and add the menu to the window
        self.constructMenuBar()

        # Construct and add the tool bar to the window
        self.constructToolbar()

        # Construct and add the graphs to the window
        self.Graphs = MultiGraphWidget()
        self.setCentralWidget(self.Graphs)
    
    def constructMenuBar(self) -> None:
        self.MenuBar = QMenuBar()
        self.setMenuBar(self.MenuBar)

        self.ConnectMenu = QMenu('Connect')
        self.constructConnectMenu()
        self.MenuBar.addMenu(self.ConnectMenu)

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

    def constructToolbar(self) -> None:
        self.ToolBar = QToolBar()
        self.addToolBar(self.ToolBar)



class MultiGraphWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Set layout of widget
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Iteratively create graphs
        self.createGraphs()

    def createGraphs(self) -> None:
        # Create 12 graphs and add them to the layout
        for row in range(3):
            for col in range(4):
                graph = GraphWidget()
                graph.hide()
                self.layout.addWidget(graph, row, col)
        # Only show 1 graph to start
        self.graphAt(0, 0).show() 

    def graphAt(self, row: int, col: int) -> GraphWidget:
        return self.layout.itemAtPosition(row, col).widget() 



if __name__ == '__main__':
    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Create the appliction instance
    app = QApplication(sys.argv)

    window = MODBUS_GUI()

    window.show()

    sys.exit(app.exec())
