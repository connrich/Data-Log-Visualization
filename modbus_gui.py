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



class MODBUS_GUI(QMainWindow):
    '''
    The main GUI window used for the Modbus viewer/logger
    '''
    def __init__(self) -> None:
        super().__init__()

        # Main window settings
        self.setWindowTitle('QuantumView')
        self.setWindowIcon(QIcon(resource_path('gui_resources\images\Quantum_icon.png')))





if __name__ == '__main__':
    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Create the appliction instance
    app = QApplication(sys.argv)

    # graph = GraphWidget()
    # graph.show()
    window = MODBUS_GUI()

    d = QDockWidget()
    d.setWindowTitle('Test')
    window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, d)

    t = QToolBar()
    window.addToolBar(t)

    window.show()
    

    sys.exit(app.exec())
