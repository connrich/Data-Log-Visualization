from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QButtonGroup
from PyQt5.QtCore import QEvent


class SelectorButton(QPushButton):
    unselected_ss = '''
        QPushButton {
            background-color: gray;
            color: white;
            border: 2px solid transparent;
            border-radius: 8px;
            padding: 8px 16px;
        }
    '''

    selected_ss = '''
        QPushButton {
            background-color: #cbe8f5;
            color: white;
            border: 2px solid black;
            border-radius: 8px;
            padding: 8px 16px;
        }
    '''

    def __init__(self, row: int, col: int, parent: QWidget=None) -> None:
        super().__init__()
        # Save location and parent information
        self.row = row
        self.col = col
        self.parent = parent
        
        # Show button as unselected initially
        self.setStyleSheet(self.unselected_ss)

    def selected(self) -> None:
        '''
        Shows the button as selected
        '''
        self.setStyleSheet(self.selected_ss)

    def unselected(self) -> None:
        '''
        Shows the button as unselected
        '''
        self.setStyleSheet(self.unselected_ss)

    def enterEvent(self, a0: QEvent) -> None:
        '''
        Triggers when the mouse enters the bounds of the button
        '''
        self.parent.buttonHovered(self)
        return super().enterEvent(a0)

    def leaveEvent(self, a0: QEvent) -> None:
        '''
        Triggers when the mouse leaves the bounds of the button
        '''
        self.parent.buttonUnhovered(self)
        return super().leaveEvent(a0)



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
        self.ButtonGroup.buttonClicked.connect(lambda btn: self.parent.showGraphs(btn.row, btn.col))
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
    
    def buttonHovered(self, btn: SelectorButton):
        '''
        Called by a child button when it is hovered over
        '''
        for row in reversed(range(btn.row+1)):
            for col in reversed(range(btn.col+1)):
                self.buttonAt(row, col).selected()
    
    def buttonUnhovered(self, btn: SelectorButton):
        '''
        Called by a child button when it is hovered over
        '''
        for row in reversed(range(btn.row+1)):
            for col in reversed(range(btn.col+1)):
                self.buttonAt(row, col).unselected()