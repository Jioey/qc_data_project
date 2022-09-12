from tkinter import Frame, Menu, Toplevel, Button, Label, Tk, Entry, Text, messagebox, END, NORMAL, DISABLED, LEFT
from tkinter import filedialog
import traceback

from dataParser import dataParser
from constants import constants

'''
A simple Tkinter UI that loads a txt file and allows user to enter tester's name

Args:
      parser (dataParser): A dataParser object to use for processing the data
      c (constants): reference to the constants obj

Attributes:
      filename (str): Instance variable that stores the input txt file's name
      parser (dataParser): Reference to the parser object
'''
class App(Tk):
   # init
   def __init__(self, parser:dataParser, c:constants) -> None:
      super().__init__()
      # using instance variable to store filename
      self.filename = ''
      self.c = c
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
      self.title("TECO")
      
      # menu bar
      menubar = Menu(self)
      configMenu = Menu(menubar, tearoff=0)
      configMenu.add_command(label="Update Constants from Config File", command=lambda:[self.c.loadYaml(), self.c.updateTemplateRange(), showConfirm('Constants loaded and templates updated')])
      # configMenu.add_command(label="Update Configs from COA Template", command=lambda:[self.c.updateConstants, showConfirm('Configs updated')])
      configMenu.add_command(label="Show Allowed Ranges", command=self.showConfig)
      menubar.add_cascade(label="Config", menu=configMenu)
      
      self.config(menu=menubar)

      # button to load file
      loadButton = Button(self, text="Load File", command=self.onOpen)
      # displayed text to prompt tester name
      # add a frame for tester input
      testerFrame = Frame(self)
      testerLabel = Label(testerFrame, text='Tester name: ')
      # text Entry to enter tester name
      testerEntry = Entry(testerFrame)
      # submit button that triggers generateDocuments and clears text widgets
      submitButton = Button(self, text="Submit", command=lambda:[self.onSubmit(testerEntry.get()), self.clearTextWidget(self.txt)])
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

   Args:
         tester (str): Tester name to be written on the documents

   Raises:
         Exception: Either filename or tester entry is empty

   Returns:
         None
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
      elif (len(tester.strip().split(" ")) != 2):
         messagebox.showwarning("Warning", "Tester name has been entered incorrectly\nPlease use the 'FirstName LastInitial.' format")
         raise Exception("tester name incorrect")
      else:
         # if both fields are entered
         try:
            # try generating data
            self.parser.generateDocuments(self.filename, tester)
            # Generated documents comfirmation
            showConfirm("Documents generated")
         except Exception as e:
            # print traceback msg
            traceback.print_exc()
            # show error msg to usr
            errorMsg = "Code error: %s; see full traceback in terminal" % e
            messagebox.showerror("Error", errorMsg)

   
   '''
   Clears Text widget in gui
   Used to do so after onSubmit()

   Args:
         txt (Text): The Text widget to clear

   Returns:
         None
   '''
   def clearTextWidget(self, txt:Text) -> None:
      txt.config(state=NORMAL)
      txt.delete(1.0, END)
      txt.config(state=DISABLED)

   
   def showConfig(self) -> None:
      top = Toplevel(self)
      top.title('Allowed Ranges')
      l1 = Label(top, justify=LEFT, font=16,
                  text= 'KOVA I: %s\nKOVA II: %s\nKOVA III: %s' %
                  (str(self.c.allowedRangesI), str(self.c.allowedRangesII), str(self.c.allowedRangesIII)))
      l1.pack()
      top.mainloop()


'''
Shows Bad Machine warning text window (messagebox) with msg
Then writes it to machineErrors.txt

Args:
      msg (str): Warning message to be displayed on the messagebox

Returns:
      None
'''
def warn(msg:str) -> None:
   messagebox.showwarning('Warning - Bad Machine', msg)
   with open('machineErrors.txt', 'a', encoding="utf-8") as f:
      f.write(msg + '\n')

def showConfirm(action:str='') -> None:
   messagebox.showinfo("TECO",  action + ' successfully')
