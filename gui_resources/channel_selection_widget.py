from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, \
                            QGridLayout, QButtonGroup, QDockWidget
from pandas import DataFrame
import pyqtgraph as pg
import sys
import random
import numpy as np

from gui_resources.graph_layout_widget import SelectorButton



class ButtonGrid(QWidget):

    def __init__(self, rows: int, cols: int, parent: QWidget) -> None:
        super().__init__()

        # Parent widget
        self.parent = parent

        # Main layout for the grid
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Iteratively create the buttons and save to the array
        self.ButtonGroup = QButtonGroup()
        for row in range(rows):
            for col in range(cols):
                btn = SelectorButton(row, col, self)
                self.ButtonGroup.addButton(btn, row*3+col)
                self.layout.addWidget(btn, row, col)
    
    def buttonAt(self, row: int, col: int) -> SelectorButton:
        '''
        Returns the widget at (row, col)
        '''
        return self.layout.itemAt(row*self.layout.columnCount() + col).widget()
    


class ChannelSelectionWidget(QDockWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.widget = QWidget()
        self.setWidget(self.widget)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.widget.setLayout(self.layout)

        self.graphSelection = ButtonGrid(*parent.GraphArraySize, parent)
        self.graphSelection.setMaximumHeight(150)
        self.graphSelection.ButtonGroup.setExclusive(True)
        self.layout.addWidget(self.graphSelection)