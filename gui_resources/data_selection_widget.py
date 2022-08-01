from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, \
                            QPushButton, QColorDialog, QCheckBox, QLabel
from pandas import DataFrame
import pandas as pd
import pyqtgraph as pg
import sys
import random
import numpy as np
from datetime import datetime

from gui_resources.style import StyleSheet as SS
from gui_resources.style import Font



class DataSelectionWidget(QWidget):
    '''
    Widget subclass for containing the list of loaded data sets
    '''
    def __init__(self, graph: pg.PlotWidget) -> None:
        super().__init__()

        # Save pointer to the corresponding graph
        self.graph = graph

        # Set layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        # Settings
        self.setMinimumWidth(200)
    
    def addDataSet(self, name: str, data: DataFrame, graph: pg.PlotWidget,
                   color: tuple=None, trendline: bool=False) -> None:
        '''
        Add new data set object to the widget display using provided parameters
        '''
        self.layout.addLayout(
            DataSet(
                name, data, graph, color=color, trendline=trendline
            )
        )
    
    def clearDatasets(self) -> None:
        '''
        Iterates through the data set objects in the widget and deletes them
        '''
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).delete()



class DataSet(QHBoxLayout):
    '''
    Horizontal layout subclass for containing data set information
    i.e. plotting color, data set name, plot item used for graphing
    '''
    def __init__(self, name: str, data: DataFrame, graph: pg.PlotWidget,
                 color: tuple=None, trendline: bool=False) -> None:        
        super().__init__()

        # Pointer to parent graph
        self.graph = graph

        # Construct a plot item that can be shown/hidden on the parent graph
        self.PlotDataItem = pg.PlotDataItem(
            data.index,
            data['VarValue'].to_list(),
            )

        # Construct display color widget
        self.color = QPushButton()
        self.color.setStyleSheet("QPushButton:hover{border: 1px solid rgb(0, 0, 0);}")
        self.color.setFixedSize(20, 20)
        if type(color) == tuple:
            self.setColor(color)
        else:
            self.setColor((random.randint(0, 255), 
                            random.randint(0, 255), 
                            random.randint(0, 255)))
        self.color.clicked.connect(self.colorSelectionMenu)
        self.addWidget(self.color)

        # Construct name widget
        self.name = QPushButton()
        self.name.setFixedHeight(20)
        self.name.setCheckable(True)
        self.name.setText(name)
        self.name.setStyleSheet(SS.name_button)
        self.name.setFont(Font.name_button)
        # Connect click to hide/show the data set on the parent graph
        self.name.clicked.connect(lambda: self.showData(self.name.isChecked()))
        self.addWidget(self.name)

        # Check box for displaying a trendline
        self.TrendlineActive = QCheckBox('TL')
        self.TrendlineActive.clicked.connect(self.trendlineButtonClicked)
        self.addWidget(self.TrendlineActive)

        # Trendline slope and intercept if loaded
        self.TrendlineSlopeIntercerpt = QLabel()
        self.addWidget(self.TrendlineSlopeIntercerpt)

        # Trendline data structure
        if trendline:
            self.setTrendline()
        else:
            self.trendline = None

        # Signal/slot for updating trendline when x axis is rescaled
        self.graph.sigRangeChanged.connect(self.updateTrendline)
    
    def setColor(self, color: tuple) -> None:
        '''
        Set the display color for the data set
        '''
        r, g, b = color
        self.PlotDataItem.setPen(pg.mkPen(color, width=2))
        self.color.setStyleSheet(f"QPushButton {{ \
            background-color: rgb({r}, {g}, {b}); \
            border-radius: 5px; \
            }} \
            QPushButton:hover{{ \
            border: 1px solid rgb(0, 0, 0); \
            }};") 

    def updateTrendline(self) -> None:
        '''
        Called when x range is changed. Updates the trendline to match currently shown data
        '''
        if self.trendline is None:
            return
        else:
            self.removeTrendline()
            self.setTrendline(*self.graph.xaxis.range)

    def setTrendline(self, start: float, end: float, ) -> None:
        '''
        Creates a trendline for a subset of the data
        '''
        # x and y data currently plotted
        x_data = self.PlotDataItem.xData
        y_data = self.PlotDataItem.yData

        # Currently shown y range
        ymin, ymax = self.graph.getAxis('left').range

        # Trim data to x axis range
        y1 = []
        x1 = []
        xrange = end-start
        xpad = xrange*0
        for i in range(0, len(x_data)):
            if start-xpad <= x_data[i] <= end+xpad:
                x1.append(x_data[i])
                y1.append(y_data[i])
        xmid = int((len(x1))/2)

        # Trim data to y axis range
        yupper = []
        xupper = []
        yrange = ymax-ymin
        ypad = yrange*.1
        for i in range(xmid, len(x1)):
            if ymin-ypad <= y1[i] <= ymax+ypad:
                xupper.append(x1[i])
                yupper.append(y1[i])
            else:
                break
        xtemp = []
        ytemp = []
        for i in range(xmid,-1,-1):
            if ymin*0.95 <= y1[i] <= ymax*1.05:
                xtemp.append(x1[i])
                ytemp.append(y1[i])
            else:
                break
        xlower = []
        ylower = []
        for i in range(len(xtemp)-1, -1,-1):
            xlower.append(xtemp[i])
            ylower.append(ytemp[i])
        x = xlower+xupper
        y = ylower+yupper

        # Generate trendline
        x2 = np.arange(0, len(x))
        A = np.vstack([x2, np.ones(len(x))])
        m, b = np.linalg.lstsq(A.T, y, rcond=None)[0]
        trend = m*x2+b

        # Update the slope and intercept values displayed
        self.TrendlineSlopeIntercerpt.setText('m = {:.3f} : b = {:.3f}'.format(m*6, b))

        # Save the trendline to the object and plot on graph
        self.trendline = pg.PlotDataItem(x, trend)
        self.trendline.setPen(pg.mkPen(self.getColor(), width=2, style=Qt.DashLine))
        self.graph.addItem(self.trendline)
    
    def removeTrendline(self) -> None:
        '''
        Removes the trendline from the graph and object
        '''
        if self.trendline is not None:
            self.graph.removeItem(self.trendline)
            self.trendline = None
            self.TrendlineSlopeIntercerpt.setText('')
    
    def trendlineButtonClicked(self) -> None:
        '''
        Slot for activating/deactivating a trendline
        '''
        if self.TrendlineActive.isChecked() and self.name.isChecked():
            x_range = self.graph.xaxis.range
            self.setTrendline(*x_range)
        elif not self.name.isChecked():
            self.TrendlineActive.setChecked(False)
        else:
            self.removeTrendline()

    def colorSelectionMenu(self) -> None:
        '''
        Opens a QColorDialog color picker for selecting display color
        '''
        color = QColorDialog.getColor()
        if color is not None:
            self.setColor((color.red(), color.green(), color.blue()))
    
    def getColor(self) -> tuple:
        '''
        Returns current display color
        '''
        color = self.color.palette().window().color()
        return (color.red(), color.green(), color.blue())
    
    def setName(self, name: str) -> None:
        '''
        Set display name 
        '''
        self.name.setText(name)
    
    def showData(self, show: bool) -> None:
        '''
        Displays the data set on the parent graph if True 
        '''
        if show:
            self.graph.addItem(self.PlotDataItem)
        else:
            self.graph.removeItem(self.PlotDataItem)
            self.removeTrendline()
            self.TrendlineActive.setChecked(False)
        
    def delete(self) -> None:
        '''
        Iterates through widgets in layout in reverse order and deletes them
        '''
        for i in reversed(range(self.count())):
            self.itemAt(i).widget().deleteLater()
        self.deleteLater()



if __name__ == '__main__':
    # Helps with scaling when using two screens with diffirent DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Initialize application
    app = QApplication(sys.argv)
    
    # Construct test widget
    w = DataSelectionWidget()
    w.layout.addLayout(DataSet('test', (255,0,0), {}))
    w.show()

    # Terminated when the application is closed 
    sys.exit(app.exec())