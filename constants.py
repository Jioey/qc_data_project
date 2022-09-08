'''
Constants - Reads text file and loads the constants in them
Including allowed ranges for tests, document template names, etc.
'''
class constants():
   def __init__(self) -> None: 
# name of all parameters tested, in correct order
      self.PARAMETERS = ['LEU', 'NIT', 'URO', 'PRO', 'pH', 'BLO', 'SG', 'KET', 'BIL', 'GLU']

      # dictionary for translation
      self.dictSymbol = {'Small':'1+', 'Moderate':'2+', 'Large':'3+', 'Positive':'(+)', 'Negative':'(-)', 'Trace':'TRA', '>=':'\u2265'}

      # row and column name for dataframe (technically not dict too)
      self.ROW_NAME = ['Control', 'KOVA I', 'KOVA II', 'KOVA III']
      self.COL_NAME = self.PARAMETERS

      # document template names
      self.COA_TEMPLATE_NAME = 'COA Template.docx'
      self.LABSHEET_TEMPLATE_NAME = 'Lab Worksheet Template.docx'
      self.COA_FAILED_TEMPLATE_NAME = 'COA Template - Failed.docx'
      self.LABSHEET_FAILED_TEMPLATE_NAME = 'Lab Worksheet Template - Failed.docx'

# list of acceptable parameters for each control
# in order of PARAMETERS
      self.allowedRangesI = [['1+', '2+', '3+'], ['(+)'], ['4.0', '\u22658.0'], ['100', '\u2265300'], ['6.5', '7.0', '7.5', '8.0'], ['2+', '3+'], ['1.010', '1.015', '1.020', '1.025'], ['40', '\u226580'], ['2+', '3+'], ['500', '1000']]
      self.allowedRangesII = [['1+', '2+', '3+'], ['(+)'], ['0.2', '1.0'], ['TRA', '30'], ['7.0', '7.5', '8.0', '8.5'], ['1+', '2+'], ['1.005', '1.010', '1.015'], ['TRA', '15', '40'], ['(-)', '1+'], ['100', '250']]
      self.allowedRangesIII = [['(-)'], ['(-)'], ['0.2', '1.0'], ['(-)'], ['5.0', '5.5', '6.0', '6.5'], ['(-)'], ['1.005', '1.010', '1.015'], ['(-)'], ['(-)'], ['(-)']]


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


if __name__ == '__main__':
   c = constants()
   c.readConstants()