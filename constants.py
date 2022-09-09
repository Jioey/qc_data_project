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

      self.loadYaml()

'''
Turns a list in string format into list datatype

Args:
   s (str): The string to convert
   is2D (bool): Used to write tester name on the documents

Returns:
   list: str in list format
'''
      kovaIII = tolerenceRanges[3][1:11]

   # print(l)
   return l


# for debug use
if __name__ == '__main__':
   c = constants()
   c.loadYaml()