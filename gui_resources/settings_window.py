import sys
import os
import json

from PyQt5.QtWidgets import (QWidget, QLabel, QGridLayout, QPushButton, 
                            QLineEdit, QApplication, QComboBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from gui_resources.style import StyleSheet as SS
from gui_resources.style import Font


#TODO
# Combobox selection for delimiter character and decimal character
# Default import configuration options 


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
        self.setMinimumWidth(350)

        # Main layout for settings window
        self.MainLayout = QGridLayout()
        self.MainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.MainLayout)

        # Add options for CSV imports
        self.CSVimportLabel = QLabel('CSV Import Settings')
        self.CSVimportLabel.setFont(Font.settings_title)
        self.CSVimportLabel.setAlignment(Qt.AlignCenter)
        self.MainLayout.addWidget(self.CSVimportLabel)

        # Add selection for default settings
        # self.defaultSettingsLabel = QLabel('Default Settings')
        # self.MainLayout.addWidget(self.defaultSettingsLabel, 1, 0)
        self.defaultSettingsCombo = QComboBox()
        self.defaultSettingsCombo.addItems(['Default Settings', 'Siemens', 'StrideLinx'])
        self.defaultSettingsCombo.textActivated.connect(self.defaultSettings)
        self.MainLayout.addWidget(self.defaultSettingsCombo, 1, 0)   

        # Add csv import settings
        csv_settings = self.constructCSVsettings()
        self.MainLayout.addLayout(csv_settings, 2, 0)

        # Button to apply the settings 
        self.ApplyButton = QPushButton('Apply')
        self.ApplyButton.clicked.connect(self.settingsApply)
        self.MainLayout.addWidget(self.ApplyButton)

    def show(self) -> None:
        '''
        Opens the settings window and populates it with the current settings
        '''
        # Populate current settings to window
        self.DelimiterSelection.setText(self.settings['delimiter'])
        self.DecimalSelection.setText(self.settings['decimal'])
        self.TimeHeaderString.setText(self.settings['time_header_title'])
        self.DateTimeFormatComboBox.clear()
        self.DateTimeFormatComboBox.addItems(self.settings['recent_date_time_format'])
        self.DateTimeFormatLineEdit.setText(self.settings['date_time_format'])

        # Show the settings window 
        super().show()
        super().activateWindow()
    
    def settingsApply(self) -> None:
        '''
        Saves the current settings and stores them in a json file
        '''
        # Save csv import settings
        self.settings['delimiter'] = self.DelimiterSelection.text()
        self.settings['decimal'] = self.DecimalSelection.text()
        self.settings['time_header_title'] = self.TimeHeaderString.text()
        self.settings['date_time_format'] = self.DateTimeFormatLineEdit.text()

        date_time_formats = [
            self.DateTimeFormatComboBox.itemText(i) for i in range(self.DateTimeFormatComboBox.count())
            ][:6]
        if self.settings['date_time_format'] not in date_time_formats:
            date_time_formats.insert(0, self.settings['date_time_format'])
            self.DateTimeFormatComboBox.addItem(self.DateTimeFormatLineEdit.text())
        self.settings['recent_date_time_format'] = date_time_formats

        # Write settings to the settings file
        with open(os.path.join(os.path.dirname(__file__), 'csv_settings.json'), 'w+') as json_file:
            json.dump(self.settings, json_file)

    def constructCSVsettings(self) -> QGridLayout:
        '''
        Convenience function for constructing widgets pertaining to csv import settings
        '''
        # Create layout of csv settings
        self.CSVLayout = QGridLayout()

        # Input for setting the CSV delimiter
        self.DelimiterSelectionLabel = QLabel('Delimiter')
        self.DelimiterSelectionLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.CSVLayout.addWidget(self.DelimiterSelectionLabel, 0, 0)
        self.DelimiterSelection = QLineEdit()
        self.CSVLayout.addWidget(self.DelimiterSelection, 0, 1)

        # Input for setting the CSV comma character
        self.DecimalSelectionLabel = QLabel('Decimal')
        self.CSVLayout.addWidget(self.DecimalSelectionLabel, 0, 2)
        self.DecimalSelection = QLineEdit()
        self.CSVLayout.addWidget(self.DecimalSelection, 0, 3)

        # Input for the time column header
        self.TimeHeaderStringLabel = QLabel('Time Header Title')
        self.CSVLayout.addWidget(self.TimeHeaderStringLabel, 1, 0)
        self.TimeHeaderString = QLineEdit()
        self.CSVLayout.addWidget(self.TimeHeaderString, 1, 1, 1, 3)

        # Input for date/time format of the data
        self.DateTimeFormatLabel = QLabel('Date/Time Format')
        self.CSVLayout.addWidget(self.DateTimeFormatLabel, 2, 0)
        self.DateTimeFormatComboBox = QComboBox()
        self.DateTimeFormatLineEdit = QLineEdit()
        self.DateTimeFormatComboBox.setLineEdit(self.DateTimeFormatLineEdit)
        self.CSVLayout.addWidget(self.DateTimeFormatComboBox, 2, 1, 1, 3)

        return self.CSVLayout

    def defaultSettings(self) -> None:
        selected = self.defaultSettingsCombo.currentText()

        if selected == 'Siemens':
            self.DelimiterSelection.setText(';')
            self.DecimalSelection.setText(',')
            self.TimeHeaderString.setText('TimeString')
            self.DateTimeFormatLineEdit.setText('%d.%m.%Y %H:%M:%S')

        elif selected == 'StrideLinx':
            self.DelimiterSelection.setText(',')
            self.DecimalSelection.setText('.')
            self.TimeHeaderString.setText('time')
            self.DateTimeFormatLineEdit.setText('%Y-%m-%d %H:%M:%S.%f')



if __name__ == '__main__':
    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Initialize application
    app = QApplication(sys.argv)
    # Create window
    MainWindow = SettingsWindow({})
    MainWindow.show()
    # Terminated when the application is closed 
    sys.exit(app.exec())