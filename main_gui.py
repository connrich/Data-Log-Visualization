'''
Standard Python packages
'''
import sys
from datetime import datetime
import os
import json
import ctypes
from platform import system

'''
PyQt packages
'''
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

'''
Custom packages
'''
from gui_resources.style import StyleSheet as SS
from gui_resources.error_message import ErrorMessage
from gui_resources.resource_path import resource_path
from csv_gui import CSV_GUI
from modbus_gui import MODBUS_GUI



class MAIN_GUI(QMainWindow):
    '''
    Main GUI for containing the csv viewer and Modbus viewer/logger
    '''
    def __init__(self):
        super().__init__()
        # Main window settings
        self.setWindowTitle('QuantumView')
        self.setWindowIcon(QIcon(resource_path('gui_resources\images\Quantum_icon.png')))

        self.TabWidget = QTabWidget()
        self.TabWidget.setStyleSheet('QTabBar {font-size: 10pt; font-weight: bold;}')
        self.setCentralWidget(self.TabWidget)

        self.CSVWindow = CSV_GUI()
        self.TabWidget.addTab(self.CSVWindow, 'CSV Viewer')

        self.ModbusWindow = MODBUS_GUI()
        self.TabWidget.addTab(self.ModbusWindow, 'Modbus')



if __name__ == '__main__':
    # Needed to set task bar icon on Windows
    if system() == 'Windows':
        myappid = 'Quantum_Data_logger'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Create the appliction instance
    app = QApplication(sys.argv)

    window = MAIN_GUI()

    window.show()
    
    sys.exit(app.exec())