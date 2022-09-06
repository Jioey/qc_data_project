# -*- coding: utf-8 -*-

"""##Packages"""
import gui
import dataParser

'''
For 901 update of the TC-201
'''
if __name__ == '__main__':
    # root of tkinter
    ui = gui.App(dataParser.dataParser())
    # mainloop continuosly shows window until closed
    ui.mainloop()