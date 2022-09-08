# -*- coding: utf-8 -*-
'''
Pydoc in 'Google Style'
Refrence: https://www.datacamp.com/tutorial/docstrings-python
'''
import gui
import dataParser
import constants

'''
For 901 update of the TC-201
'''
if __name__ == '__main__':
    c = constants()
    # root of tkinter
    ui = gui.App(dataParser.dataParser())
    # mainloop continuosly shows window until closed
    ui.mainloop()