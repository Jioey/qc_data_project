"""
Take input from user
Error handling
Send to txtWriter
"""
# pseudo code
# open file button -> displays file name when loaded
# enttry where usr enters tester name
# submit button to generate the files

from tkinter import Button, Frame, Label, Tk, Entry, Text, messagebox, END, NORMAL, DISABLED
from tkinter import filedialog
import traceback
import sys

from dataParser import dataParser

class App(Tk):
   # init
   def __init__(self, parser:dataParser) -> None:
      super().__init__()
      # using instance variable to store filename
      self.filename = ''
      # reference to the parser obj
      self.parser = parser
      # setting window geometry
      self.geometry("680x470+400+150")
      # inituialize UI
      self.initUI()

   # initializing the gui
   def initUI(self) -> None:
      # packing self (the Frame)
      self.title("TECO")
      # another frame for tester input
      testerFrame = Frame(self)

      # button to load file
      loadButton = Button(self, text="Load File", command=self.onOpen)
      # displayed text to prompt tester name
      testerLabel = Label(testerFrame, text='Tester name: ')
      # text Entry to enter tester name
      testerEntry = Entry(testerFrame)
      # submit button that triggers generateDocuments and clears text widgets
      submitButton = Button(self, text="Submit", command=lambda:[self.onSubmit(testerEntry.get()), testerEntry.delete(0, END), self.txt.delete(1.0, END)])
      # Text widget that displays loaded file & read only
      self.txt = Text(self)
      self.txt.config(state=DISABLED)

      # packing
      self.txt.pack(ipadx=3, ipady=3, fill='both', expand=True)
      testerFrame.pack(fill='x')
      testerLabel.pack(ipadx=15, fill='both', side='left')
      testerEntry.pack(fill='both', side='right', expand=True)
      loadButton.pack(fill='both')      
      submitButton.pack(fill='both')


   # triggers when load button is hit
   # saves filename, reads the file and displays on Text widget
   def onOpen(self) -> None:
      # file types choosable in File Explorer
      ftypes = [('text files', '*.txt'), ('All files', '*')]
      # file dialog
      dlg = filedialog.Open(self, filetypes = ftypes)
      # reads filename
      fl = dlg.show()

      # if read filename is not empty
      if fl != '':
         # store filename in instance var
         self.filename = fl
         # opens the file
         with open(fl, "r") as f:
            # reads it and store it
            text = f.read()
         # displays read text on Text widget (make txtbox temporaily changable)
         self.txt.config(state=NORMAL)
         self.txt.delete(1.0, END)
         self.txt.insert(END, text)
         self.txt.config(state=DISABLED)


   # triggers when submit button is hit
   # runs generateDocuments with the needed info entered from the gui
   # raises Exception if either filename or tester entry is empty
   def onSubmit(self, tester:str) -> None:
      print("OnSubmit: ")
      print("filename: %s; tester: %s" % (self.filename, tester))

      if (self.filename == ''):
         messagebox.showerror("Error", "No file has been loaded")
         raise Exception("filename empty")
      elif (tester == ''):
         messagebox.showerror("Error", "No tester name has been entered")
         raise Exception("tester empty")
      else:
         try:
            self.parser.generateDocuments(self.filename, tester)
            # if (self.parser.isErrorMachine):
            messagebox.showinfo("TECO",  "Documents generated successfully")
         except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
            errorMsg = ''.join(tb.format_exception_only())
            traceback.print_exc()
            # errorMsg = "Code error: %s; close window and see full error (traceback) in terminal" % e
            messagebox.showerror("Error", errorMsg)


# main function that runs the gui
def main():
   # root of tkinter
   root = Tk()
   # creating Frame instance
   ex = Example()
   # setting window geometry
   root.geometry("680x470+400+150")
   # mainloop continuosly shows window until closed
   root.mainloop()

# shows warning text window
def warn(msg):
   messagebox.showwarning('Warning - Bad Machine', msg)