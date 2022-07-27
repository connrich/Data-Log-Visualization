from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, \
                            QPushButton, QColorDialog
from pandas import DataFrame
import pandas as pd
import pyqtgraph as pg
import sys
import random
import numpy as np
from datetime import datetime

from gui_resources.style import StyleSheet as SS
from gui_resources.style import Font




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

        # Construct a plot item that can be shown/hidden on the parent graph
        self.PlotDataItem = pg.PlotDataItem(
            data.index,
            data['VarValue'].to_list(),
            )

        # Construct display color widget
        self.color = QPushButton()
        self.color.setFixedSize(20, 20)
        if type(color) == tuple:
            self.setColor(color)
        else:
            self.setColor((random.randint(0, 255), 
                            random.randint(0, 255), 
                            random.randint(0, 255)))
        self.color.clicked.connect(self.colorSelectionMenu)
        self.addWidget(self.color)

        # Future variable for trendline management
        self.trendline = trendline
    
    def setColor(self, color: tuple) -> None:
        '''
        Set the display color for the data set
        '''
        r, g, b = color
        self.color.setStyleSheet(f"QPushButton {{ \
                                    background-color: rgb({r}, {g}, {b}); \
                                    border-radius: 5px; \
                                    }};") 
        self.PlotDataItem.setPen(pg.mkPen(color, width=2))

    def trendline(self,data,key,start,end):
        '''
        Creates a trendline for a subset of the data
        '''
        #For Connor:
        #Takes in unpivoted pandas dataframe, key (as a string), and start and end date (datetime objects)
        #returns x and y lists, x is a list of datetime objects
        table = pd.pivot_table(data=self.data, index=['VarName', 'TimeString'])
        dic = {}
        for i in table.index.unique(level='VarName'):
            dic[i] = table.loc[(i,)]
        start = datetime.fromtimestamp(start()).strftime('%m/%d/%Y %H:%M:%S')
        end = datetime.fromtimestamp(end()).strftime('%m/%d/%Y %H:%M:%S')
        fully = table['VarValue'][key].to_list()
        fullx = (dic[key].index).to_pydatetime()
        y = []
        x = []
        for i in range(0, len(fullx)):
            if start <= fullx[i] <= end:
                x.append(fullx[i])
                y.append(fully[i])
        x1 = np.arange(0, len(x))
        A = np.vstack([x1, np.ones(len(x))])
        m, b = np.linalg.lstsq(A.T, y, rcond=None)[0]
        trend = m*x1+b
        return x, trend

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
        Displays the data set on the parent graph
        '''
        if show:
            self.graph.addItem(self.PlotDataItem)
        else:
            self.graph.removeItem(self.PlotDataItem)
        
    def delete(self) -> None:
        '''
        Iterates through widgets in layout in reverse order and deletes them
        '''
        for i in reversed(range(self.count())):
            self.itemAt(i).widget().deleteLater()
        self.deleteLater()



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
        self.setMinimumWidth(130)
    
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