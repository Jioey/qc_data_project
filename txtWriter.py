"""
Helper for gui
Writes to inner text file
"""
from constants import INNER_FILE_NAME

def writeTextFile(text):
   # open file, in append mode
   f = open(INNER_FILE_NAME, 'a')
   # write to file
   f.write(text)
   # close file
   f.close()

# empties 'all results.txt'
def clearTextFile():
   f = open(INNER_FILE_NAME,'w')
   f.close()

def save(text):
   # write to file
   writeTextFile(text)
   print("file saved")