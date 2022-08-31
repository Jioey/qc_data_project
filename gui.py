from tkinter import *
from utils import save, clearTextFile, closeWindow

# root of tkinter window
root = Tk()

# store tester info
tester = StringVar()

# returns tester name
def getTester():
   return tester.get()

# Comfirming the generation of documents after entering tester name
def confirm():
   from functions import generateDocuments
   generateDocuments()
   clearTextFile()

# pop up window to enter tester name and comfirm generating file
def toplevelWindow():
   # root of toplevel window
   window = Toplevel(root)

   l = Label(window, text='Enter tester initials:')
   # entry to get tester initial
   e1 = Entry(window, textvariable=tester)

   # trigger confirm function when button pressed, then close the toplevel window
   b1 = Button(window, text = "Generate", command=lambda:[confirm(), closeWindow(window)])

   # packing everything
   l.pack()
   e1.pack()
   b1.pack()

   # display the window
   window.grab_set()
   
# code for 'Next' button, where it prompts
# also validates input 
def next(T):
   # if text box is not empty, save what's in there
   if not (T.compare("end-1c", "==", "1.0")):
      save(T)

   # 

   # pop up new window to enter tester name and confirm
   toplevelWindow()

# main window that pastes results in
def mainWindow():
   # header of window
   root.title("TECO")
   # default window size of gui
   root.geometry("900x500")
   
   # text shown on window
   l = Label(root, 
         text ="Instructions: \nPaste (Ctrl+V) test results in here\n Hit save to save on text file (clears the textbox)\n Hit next when ready to proceed",
         font=("Ariel", 15))

   # text box
   T = Text(root, height=15, width=80)

   # 'lambda:' also allows to use args in func for command
   # 'Save' Button
   b1 = Button(root, text = "Save", command=lambda:save(T)) # TODO: save confirmation
   # 'Next' Button
   b2 = Button(root, text = "Next", command=lambda:next(T))

   # triggers event when Text is modified (only once tho)
   # T.bind('<<Modified>>', lambda e: printSmth())
   
   # packing everything (in order of displaying - important)
   l.pack()
   T.pack()
   b1.pack()
   b2.pack()

   # mainloops tells the code to keep displaying 
   root.mainloop()