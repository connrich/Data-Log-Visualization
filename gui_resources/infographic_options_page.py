import json
import os

from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QScrollArea, \
                            QVBoxLayout, QLabel, QPushButton, QListWidget, \
                            QListWidgetItem, QMainWindow, QComboBox
from PyQt5.QtGui import QIcon
from matplotlib.pyplot import plot_date

from infographic import Infographic
from gui_resources.style import StyleSheet as SS



class InfographicOptions(QWidget):
    def __init__(self, main_window: QMainWindow):
        super().__init__()

        # Save pointer to parent window 
        self.MainWindow = main_window

        # Window settings
        self.setWindowTitle('Generate Infographic')
        self.setWindowIcon(QIcon('gui_resources\Quantum_icon.png'))
        self.setMinimumWidth(250)

        # Create layout 
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Add project number title
        self.ProjectNumberTitle = QLabel('Select project number: ')
        self.layout.addWidget(self.ProjectNumberTitle)

        # Add dropdown for selecting project number
        self.ProjectNumberCombo = QComboBox()
        self.populateProjectNumbers()
        self.ProjectNumberCombo.currentTextChanged.connect(lambda text: self.populatePlotList(text))
        self.layout.addWidget(self.ProjectNumberCombo)

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
        with open('Infographic Settings\\bubbles.json', 'r') as json_file:
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
        for file_name in os.listdir('Infographic Settings'):
            file_name = file_name.split('.')[0]
            if file_name.isnumeric():
                self.ProjectNumberCombo.addItem(file_name)

    def populatePlotList(self, project_number: str) -> None:
        '''
        Populates a list of plot types based on the Inforgrpahic Settings json file
        '''
        # Load list of plot types
        with open(f'Infographic Settings\\{project_number}.json', 'r') as json_file:
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
    
    def generateInfographic(self):
        '''
        Calls the Infographic script with the chosen settings
        '''
        t = []
        t[:] = map(lambda x: x.text(), self.PlotList.selectedItems())

        t[:] = map(lambda x: x.text(), self.BubbleList.selectedItems())

        infographic = Infographic(
            int(self.ProjectNumberCombo.currentText()),
            data=self.MainWindow.loadedData
        )

    def showWindow(self) -> None:
        '''
        Shows the infographic options window and loads the current tags
        '''
        # Clear old tags from the list
        self.PlotList.clear()

        # Populate plots based on current project number
        self.populatePlotList(self.ProjectNumberCombo.currentText())

        # Show the window 
        self.show()