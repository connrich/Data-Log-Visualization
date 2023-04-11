import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QToolBar
from PyQt5.QtCore import Qt

from csv_gui import CSV_GUI



if __name__ == '__main__':
    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Create the appliction instance
    app = QApplication(sys.argv)

    # graph = GraphWidget()
    # graph.show()
    window = QMainWindow()

    w = CSV_GUI()

    window.setCentralWidget(w)

    d = QDockWidget()
    d.setWindowTitle('Test')
    window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, d)

    t = QToolBar()
    window.addToolBar(t)

    window.show()
    

    sys.exit(app.exec())
