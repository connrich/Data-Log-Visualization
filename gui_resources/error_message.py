from PyQt5.QtWidgets import QMessageBox

class ErrorMessage(QMessageBox):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle('Error')
        self.setText(text)
        self.setIcon(QMessageBox.Critical)
        self.exec_()