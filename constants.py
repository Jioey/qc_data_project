'''
Constants
Including allowed ranges for tests, document template names, etc.
'''
# name of all parameters tested, in correct order
PARAMETERS = ['LEU', 'NIT', 'URO', 'PRO', 'pH', 'BLO', 'SG', 'KET', 'BIL', 'GLU']

# list of acceptable parameters for each control
# in order of PARAMETERS
'''
Turns a list in string format into list datatype

Args:
   s (str): The string to convert
   is2D (bool): Used to write tester name on the documents

Returns:
   list: str in list format
'''
def strToList(s:str, is2D:bool=False) -> list:
   # strips whitespace from both ends
   s = s.strip()

   # split based on comma
   if not is2D:
      # strips [] from both ends, if exsists
      s = s.replace('[', '')
      s = s.replace(']', '')
      l = s.split(', ')
      # strip '' from both ends of each entry
      for i in range(len(l)):
         l[i] = l[i][1:len(l[i])-1]
   else:
      # strips [] from both ends, if exsists
      s = s.replace('[[', '')
      s = s.replace(']]', '')
      l = s.split('], [')
      # turn inside str to list
      for i in range(len(l)):
         l[i] = strToList(l[i])

   # print(l)
   return l

# row and column name for dataframe (technically not dict too)
ROW_NAME = ['Control', 'KOVA I', 'KOVA II', 'KOVA III']
COL_NAME = PARAMETERS

# document template names
COA_TEMPLATE_NAME = 'COA Template.docx'
LABSHEET_TEMPLATE_NAME = 'Lab Worksheet Template.docx'
COA_FAILED_TEMPLATE_NAME = 'COA Template - Failed.docx'
LABSHEET_FAILED_TEMPLATE_NAME = 'Lab Worksheet Template - Failed.docx'