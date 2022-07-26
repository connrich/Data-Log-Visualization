from gui import MainWindow

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5 import QtCore

import sys



class window(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QGridLayout()

        for i in range(3):
            mw = MainWindow()
            mw.setStyleSheet('QMainWindow{background-color: rgb(130, 130, 130)}')
            layout.addWidget(mw, i, 0)

            mw = MainWindow()
            mw.setStyleSheet('QMainWindow{background-color: rgb(130, 130, 130)}')
            layout.addWidget(mw, i, 1)

        self.setLayout(layout)

if __name__ == '__main__':
    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Initialize application
    app = QApplication(sys.argv)

    w = window()
    w.show()

    # Terminated when the application is closed 
    sys.exit(app.exec())