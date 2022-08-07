from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtCore import QDateTime


class DateTimeInput(QDateTimeEdit):
    ''''
    Custom subclass for inputting date/time
    '''
    def __init__(self, format:str="MM/dd/yyyy HH:mm") -> None:
        super().__init__()

        # Set minimum size so full date and time can be seen
        self.setMinimumWidth(110)

        # Set how the date/time is displayed 
        if format is not None: 
            self.setDisplayFormat(format)
        
        # Show a calendar when clicked 
        self.setCalendarPopup(True)
        
        # Default to the current date and time 
        self.setDateTime(QDateTime.currentDateTime())

    def getUNIX(self) -> int:
        """
        Returns the current date/time in UNIX integer format
        """
        return self.dateTime().toTime_t()