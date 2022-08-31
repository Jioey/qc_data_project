"""
Take input from user
Error handling
Send to txtWriter
"""

from tkinter import *
from txtWriter import save
from constants import EXPECTED_LINES

# root of tkinter window
root = Tk()

# store tester info
testerName = StringVar()

# TODO: organize widgets

# main window that pastes results in
def mainWindow():
   # header of window
   root.title("TECO")
   # default window size of gui
   root.geometry("900x500")

   # frames for placing widgets and pack them
   textFrame = Frame(root)
   buttonsFrame = Frame(root)
   textFrame.pack()
   buttonsFrame.pack()

   # Text Frame
   # text for instructions
   l1 = Label(textFrame, 
         text ="Instructions: \nPaste (Ctrl+V) test results in here\n Hit save to save on text file (clears the textbox)\n Hit next when ready to proceed",
         font=("Ariel", 15))
   # text box for data
   T = Text(textFrame, width='90', height='15')
   vsb = Scrollbar(textFrame, orient="vertical", command=T.yview)
   T.configure(yscrollcommand=vsb.set)
   # packing
   l1.pack()
   T.pack(side="left")
   vsb.pack(side="right", fill="y")

   # Buttons Frame
   # text for tester name
   l2 = Label(buttonsFrame, text="Tester name:")
   # entry for tester name 
   E1 = Entry(buttonsFrame, textvariable=testerName)
   # 'lambda:' also allows to use args in func for command
   # 'Save' Button - when clicked, writes input to txt file, clear input, then shows a save confirmation
   # b1 = Button(buttonsFrame, text = "Save", command=lambda:[save(getTextInput(T)), T.delete('1.0', END), showString('File saved')]) - maybe don't need save feature?
   # 'Next' Button - continues to handling/checking input errors
   b2 = Button(buttonsFrame, text = "Next", command=lambda:[inputErrorHandling(getTextInput(T)), T.delete('1.0', END)])
   # packing everything (in order of displaying - important)
   l2.grid(row=0, column=0)
   E1.grid(row=0, column=1)
   # b1.grid(row=1, column=0)
   b2.grid(row=1, column=1) 

   # mainloops tells the code to keep displaying 
   root.mainloop()

# checks and handles input errors
def inputErrorHandling(input):
   try:
      lines = input.splitlines()
      # DEBUG
      # for line in lines:
      #    print(line)
      lineCount = len(lines)
      extraLines = lineCount%EXPECTED_LINES
      if (extraLines != 0):
         raise Exception()
      save(input)
   except:
      showString("Incorrect line numbers! Should be divisible by %i but there are %i extra lines, and %i lines in total." % (EXPECTED_LINES, extraLines, lineCount))
      
# gets all input text in the text box T
def getTextInput(T):
   return T.get("1.0", "end-1c")

def showString(string):
   # TODO: show on gui
   print(string)

# closes window
def closeWindow(window):
    window.destroy()
    window.update()