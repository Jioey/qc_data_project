# -*- coding: utf-8 -*-
'''
Pydoc in 'Google Style'
Refrence: https://www.datacamp.com/tutorial/docstrings-python
'''
import gui
import dataParser
from constants import constants


if __name__ == '__main__':
    '''
    For 905 update of the TC-201
    '''
    c = constants()
    # root of tkinter
    ui = gui.App(dataParser.dataParser(c), c)
    # mainloop continuosly shows window until closed
    ui.mainloop()