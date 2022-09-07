from tkinter import Button, Frame, Label, Tk, Entry, Text, messagebox, END, NORMAL, DISABLED
from tkinter import filedialog
import traceback

from dataParser import dataParser

'''
A simple Tkinter UI that loads a txt file and allows user to enter tester's name

Args:
      parser (dataParser): A dataParser object to use for processing the data

Attributes:
      filename (str): Instance variable that stores the input txt file's name
      parser (dataParser): Reference to the parser object
'''
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

   '''
   Initializes the UI with all its components
   '''
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
      submitButton = Button(self, text="Submit", command=lambda:[self.onSubmit(testerEntry.get()), self.txt.delete(1.0, END)])
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


   '''  
   Saves filename, reads the file and displays on Text widget
   Triggers when load button is hit
   '''
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


   '''
   Runs generateDocuments with the needed info entered from the gui
   Triggers when submit button is hit

   Raises:
         Exception: Either filename or tester entry is empty
   '''
   def onSubmit(self, tester:str) -> None:
      # DEBUG: usr input info printed in terminal
      # print("OnSubmit: ")
      # print("filename: %s; tester: %s" % (self.filename, tester))

      if (self.filename == ''):
         # if filename is empty
         messagebox.showerror("Error", "No file has been loaded")
         raise Exception("filename empty")
      elif (tester == ''):
         # if tester is empty
         messagebox.showerror("Error", "No tester name has been entered")
         raise Exception("tester empty")
      elif (len(tester.split(" ")) != 2):
         messagebox.showwarning("Warning", "Tester name has been entered incorrectly\nPlease use the 'FirstName LastInitial.' format")
         raise Exception("tester name incorrect")
      else:
         # if both fields are entered
         try:
            # try generating data
            self.parser.generateDocuments(self.filename, tester)
            # if (self.parser.isErrorMachine):
            #    # shows warning text window
            #    for msg in self.parser.errMsgList:
            #       messagebox.showwarning('Warning - Bad Machine', msg)
            # Generated documents comfirmation
            messagebox.showinfo("TECO",  "Documents generated successfully")
         except Exception as e:
            # print traceback msg
            traceback.print_exc()
            # show error msg to usr
            errorMsg = "Code error: %s; see full traceback in terminal" % e
            messagebox.showerror("Error", errorMsg)


'''
shows warning text window
'''
def warn(msg):
   messagebox.showwarning('Warning - Bad Machine', msg)