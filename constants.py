'''
Constants - Reads text file and loads the constants in them
Including allowed ranges for tests, document template names, etc.
'''
class constants():
   def __init__(self) -> None: 
   '''
   Reads constants.txt 
   '''
   def getConstantsFromTxt(self) -> bool:
      with open("constants.txt", "r") as f:
         fList = f.readlines()

      self.PARAMETERS = strToList(fList[1])
      # print(self.PARAMETERS)

      self.COA_TEMPLATE_NAME, self.LABSHEET_TEMPLATE_NAME, self.COA_FAILED_TEMPLATE_NAME, self.LABSHEET_FAILED_TEMPLATE_NAME = strToList(fList[4])
      # # print(self.LABSHEET_FAILED_TEMPLATE_NAME)

      self.allowedRangesI = strToList(fList[8], True)
      self.allowedRangesII = strToList(fList[10], True)
      self.allowedRangesIII = strToList(fList[12], True)
      # print(self.allowedRangesI)

      return True


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