from typing import Any
import pyqtgraph as pg
from datetime import datetime



class GraphWidget(pg.PlotWidget):
    '''
    Plot widget subclass to allow for better control
    '''
    def __init__(self) -> None: 
        super().__init__()
        
        # Set the graph background 
        self.setBackground('w')
        self.showGrid(x=True, y=True)

        # Set graph title
        self.setTitle('Trends', color='black')

        # Use custom axis for x axis
        self.xaxis = TimeAxisItem('bottom')
        self.setAxisItems({'bottom': self.xaxis})

        # Set axis labels
        self.setLabel('left', 'Value', color='black')
        self.setLabel('bottom', 'Time', color='black')

        # Set axis colors
        self.getAxis('left').setPen('black')
        self.getAxis('left').setTextPen('black')
        self.getAxis('bottom').setPen('black')
        self.getAxis('bottom').setTextPen('black')



class TimeAxisItem(pg.AxisItem):
    '''
    Axis item subclass to allow display of date/time format
    Can pass a string format to use for display 
    i.e. '%d.%m.%Y %H:%M:%S' or '%Y/%m/%d %H:%M'
    '''
    def __init__(self, placement: Any, datetime_format: str=None) -> None:
        super(TimeAxisItem, self).__init__(placement)

        # Better display of large numbers
        self.enableAutoSIPrefix(False)
        
        # Set string formatting
        if datetime_format is None:
            self.str_format = '%d.%m.%Y %H:%M:%S'
        else:
            self.str_format = datetime_format

    def tickStrings(self, values: Any, scale: Any, spacing: Any) -> None:
        '''
        Returns a list of date/time formatted strings for display on axis
        '''
        try: 
            return [str(datetime.fromtimestamp(value).strftime(self.str_format)) for value in values]
        except:
            return []