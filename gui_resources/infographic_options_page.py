import json
import os

from PyQt5.QtWidgets import QWidget, QGridLayout, \
                            QLabel, QPushButton, QListWidget, \
                            QListWidgetItem, QMainWindow, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime

import pandas as pd

from gui_resources.infographic_logging.infographic import Infographic
from gui_resources.date_time_input_widget import DateTimeInput
from gui_resources.error_message import ErrorMessage
from gui_resources.resource_path import resource_path



class InfographicOptions(QWidget):
    ''''
    Window for setting infographic settings
    '''
    def __init__(self, main_window: QMainWindow) -> None:
        super().__init__()

        # Save pointer to parent window 
        self.MainWindow = main_window

        # Window settings
        self.setWindowTitle('Generate Infographic')
        self.setWindowIcon(QIcon('gui_resources\Quantum_icon.png'))
        self.setMinimumWidth(300)

        # Create layout 
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Add project number title
        self.ProjectNumberTitle = QLabel('Select project number: ')
        self.layout.addWidget(self.ProjectNumberTitle)

        # Add dropdown for selecting project number
        self.ProjectNumberCombo = QComboBox()
        self.populateProjectNumbers()
        self.ProjectNumberCombo.currentTextChanged.connect(
            lambda text: self.populateWindow(text)
            )
        self.layout.addWidget(self.ProjectNumberCombo)

        # Add start date selection
        self.StartDateTime = DateTimeInput()
        self.layout.addWidget(self.StartDateTime)

        # Add end date selection
        self.EndDateTime = DateTimeInput()
        self.layout.addWidget(self.EndDateTime)

        # Create title for tag list 
        self.PlotTitle = QLabel('Select plots to add:')
        self.layout.addWidget(self.PlotTitle)

        # Create list for tags
        self.PlotList = QListWidget()
        self.PlotList.setSelectionMode(2) # Enables multiple selections
        self.layout.addWidget(self.PlotList)

        # Add title for bubbles
        self.BubbleTitle = QLabel('Select bubbles to add:')
        self.layout.addWidget(self.BubbleTitle)

        # Creat list for bubble types
        self.BubbleList = QListWidget()
        self.BubbleList.setSelectionMode(2)
        self.layout.addWidget(self.BubbleList)

        # Load list of possible bubbles
        with open(resource_path('gui_resources\\infographic_logging\\Infographic Settings\\bubbles.json'), 'r') as json_file:
            bubbles = json.load(json_file)

        # Add checkboxes for each bubble
        for bubble in bubbles:
            self.BubbleList.addItem(QListWidgetItem(bubble))

        # Add button to submit selections
        self.GenerateButton = QPushButton('Generate')
        self.GenerateButton.clicked.connect(self.generateInfographic)
        self.layout.addWidget(self.GenerateButton)
    
    def populateProjectNumbers(self) -> None:
        '''
        Iterates through the Infographic Settings folder and populates the
        drop down menu
        '''
        for file_name in os.listdir(resource_path('gui_resources\\infographic_logging\\Infographic Settings')):
            file_name = file_name.split('.')[0]
            # Check if name is a number
            if file_name.isnumeric():
                self.ProjectNumberCombo.addItem(file_name)

    def populateWindow(self, project_number: str) -> None:
        '''
        Populates a list of plot types based on the Infographic Settings json file
        '''
        # Update the time window to the current min/max of loaded data
        self.StartDateTime.setDateTime(
            QDateTime.fromTime_t(int(self.MainWindow.loadedData.iloc[0]['TimeString']))
        )
        self.EndDateTime.setDateTime(
            QDateTime.fromTime_t(int(self.MainWindow.loadedData.iloc[-1]['TimeString']))
        )

        # Load list of plot types
        path = f'Infographic Settings\\{project_number}.json'
        with open(resource_path(path), 'r') as json_file:
            plot_types = json.load(json_file)

        # Clear old values
        self.PlotList.clear()
        
        # Populate the list widget with the available plot types 
        for plot in plot_types:
            # Skip keys that do not relate to plots 
            if 'project' in plot:
                continue
            # Add the item to the list 
            self.PlotList.addItem(QListWidgetItem(plot))
    
    def getTimeFilteredData(self, start: float, end: float) -> pd.DataFrame:
        '''
        Returns a segment of the currently loaded data between start to end
        start and end should be UNIX time stamps
        '''
        # Verfiy time range
        if start > end:
            ErrorMessage('Invalid date/time range. Check your start and end date/time.')
            return None
        
        data = self.MainWindow.loadedData.copy()

        data = data[data.TimeString > start]
        data = data[data.TimeString < end]

        return data
    
    def generateInfographic(self) -> None:
        '''
        Calls the Infographic script with the chosen settings
        '''
        # Trim data to selected start time 
        data = self.getTimeFilteredData(
            start=self.StartDateTime.getUNIX(),
            end=self.EndDateTime.getUNIX()
            )
        if data is None:
            return

        # Create infographic object
        infographic = Infographic(
            int(self.ProjectNumberCombo.currentText()),
            data=data
        )

        # Add all selected plots to infographic
        for plot in self.PlotList.selectedItems():
            infographic.add_plot(plot.text())
        
        # Add all selected bubbles to infographic 
        for bubble in self.BubbleList.selectedItems():
            infographic.add_bubble(bubble.text())
        
        # Display the infographic 
        infographic.show()

    def show(self) -> None:
        '''
        Shows the infographic options window and loads the current tags
        '''
        # Clear old tags from the list
        self.PlotList.clear()

        # Populate plots based on current project number
        self.populateWindow(self.ProjectNumberCombo.currentText())

        # Show the window 
        super().show()