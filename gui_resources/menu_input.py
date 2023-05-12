from PyQt5.QtWidgets import QLineEdit, QLabel, QWidgetAction, QWidget, QVBoxLayout, QComboBox


class MenuTextInputWidget(QWidgetAction):
    '''
    Custom sublass for text input in QMenus
    '''
    def __init__(self, label: str):
        # Container widget
        self.widget = QWidget()
        super().__init__(self.widget)
        self.setDefaultWidget(self.widget)

        # Layout for container widget
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        # Label for specifying input information
        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        # Text input 
        self.line_edit = QLineEdit()
        self.layout.addWidget(self.line_edit)
    
    def text(self) -> str:
        return self.line_edit.text()

    def setText(self, text: str) -> None:
        self.line_edit.setText(text)



class MenuComboInputWidget(QWidgetAction):
    '''
    Custom sublass for text input in QMenus
    '''
    def __init__(self, label: str):
        # Container widget
        self.widget = QWidget()
        super().__init__(self.widget)
        self.setDefaultWidget(self.widget)

        # Layout for container widget
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        # Label for specifying input information
        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        # Text input 
        self.combo_box = QComboBox()
        self.layout.addWidget(self.combo_box)

    def addItem(self, text) -> None:
        self.combo_box.addItem(text)
