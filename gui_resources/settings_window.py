import sys
import os
import json

from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout, QPushButton,  
                            QRadioButton, QHBoxLayout, QCheckBox, QButtonGroup, 
                            QLineEdit, QApplication)
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore

from gui_resources.style import StyleSheet as SS
from gui_resources.style import Font


class SettingsWindow(QWidget):
    '''
    Custom window for application settings
    '''
    def __init__(self, settings: dict) -> None:
        super().__init__()

        # Global app settings
        self.settings = settings

        # Fonts for settings
        self.TitleFont = QFont()
        self.TitleFont.setBold(True)
        self.TitleFont.setPointSize(9)

        # Window settings
        self.setWindowTitle('Settings')
        self.setWindowIcon(QIcon("gui_resources/Quantum_icon.png"))
        self.setMinimumWidth(300)

        # Main layout for settings window
        self.MainLayout = QGridLayout()
        self.MainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.MainLayout)

        # Add options for CSV imports
        self.CSVimportLabel = QLabel('CSV Import Settings')
        self.CSVimportLabel.setFont(Font.settings_title)
        self.CSVimportLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MainLayout.addWidget(self.CSVimportLabel)
        self.MainLayout.addLayout(self.constructCSVsettings(), 1, 0)

        # Button to apply the settings 
        self.ApplyButton = QPushButton('Apply')
        self.ApplyButton.clicked.connect(self.settingsApply)
        self.MainLayout.addWidget(self.ApplyButton)

    def showWindow(self) -> None:
        '''
        Opens the settings window and populates it with the current settings
        '''
        # Populate current settings to window
        self.DelimiterSelection.setText(self.settings['delimiter'])
        self.DecimalSelection.setText(self.settings['decimal'])

        # Show the settings window 
        self.show()
        self.activateWindow()
    
    def settingsApply(self) -> None:
        '''
        Saves the current settings and stores them in a json file
        '''
        # Save csv import settings
        self.settings['delimiter'] = self.DelimiterSelection.text()
        self.settings['decimal'] = self.DecimalSelection.text()

        # Write settings to the settings file
        with open(os.path.join(os.path.dirname(__file__), 'settings.json'), 'w+') as json_file:
            json.dump(self.settings, json_file)

    def constructCSVsettings(self) -> QGridLayout:
        '''
        Convenience function for constructing widgets pertaining to csv import settings
        '''
        self.CSVLayout = QGridLayout()

        # Input for setting the CSV delimiter
        self.DelimiterSelectionLabel = QLabel('Delimiter')
        self.CSVLayout.addWidget(self.DelimiterSelectionLabel, 0, 0)
        self.DelimiterSelection = QLineEdit()
        self.CSVLayout.addWidget(self.DelimiterSelection, 0, 1)

        # Input for setting the CSV comma character
        self.DecimalSelectionLabel = QLabel('Decimal')
        self.CSVLayout.addWidget(self.DecimalSelectionLabel, 1, 0)
        self.DecimalSelection = QLineEdit()
        self.CSVLayout.addWidget(self.DecimalSelection, 1, 1)

        return self.CSVLayout



if __name__ == '__main__':
    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Initialize application
    app = QApplication(sys.argv)
    # Create window
    MainWindow = SettingsWindow({})
    MainWindow.show()
    # Terminated when the application is closed 
    sys.exit(app.exec())