from PyQt5.QtGui import QFont



class StyleSheet:
    '''
    Data structure for storing CSS style sheets for GUI elements
    '''
    name_button = ("""
        QPushButton{
            background-color: rgb(220, 220, 220);
            border-radius: 5px;
        }
        QPushButton:hover{
            border: 1px solid rgb(0, 0, 0);
        }
        QPushButton:checked{
            background-color: rgba(66, 176, 245, 0.3);
        }
        """)

    scroll_area = ("""
        QScrollBar:vertical
        {
            background-color: rgb(200, 200, 200);
            width: 15px;
            margin: 15px 3px 15px 3px;
            border: 1px transparent #2A2929;
            border-radius: 4px;
        }

        QScrollBar::handle:vertical
        {
            background-color: rgb(150, 150, 150);         /* #605F5F; */
            min-height: 5px;
            border-radius: 4px;
        }

        QScrollBar::sub-line:vertical
        {
            margin: 3px 0px 3px 0px;
            border-image: url(:/images/up_arrow_disabled.png);        /* # <-------- */
            height: 10px;
            width: 10px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

        QScrollBar::add-line:vertical
        {
            margin: 3px 0px 3px 0px;
            border-image: url(:/images/down_arrow_disabled.png);       /* # <-------- */
            height: 10px;
            width: 10px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
        {
            border-image: url(:/images/up_arrow.png);                  /* # <-------- */
            height: 10px;
            width: 10px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

        QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
        {
            border-image: url(:/images/down_arrow.png);                /* # <-------- */
            height: 10px;
            width: 10px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
        {
            background: none;
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
        {
            background: none;
        }
        """)



class Font:
    '''
    Data structure for holding PyQt fonts used in GUI elements
    '''
    name_button = QFont('yu Gothic Medium', 8)

    settings_title = QFont('yu Gothic Medium', 10, QFont.Bold)

    settings_label = QFont('yu Gothic Medium', 8)