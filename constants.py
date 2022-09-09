'''
Constants - Reads text file and loads the constants in them
Including allowed ranges for tests, document template names, etc.
'''
import yaml

class constants():
   '''
   Initializes instance variables and sets them by reading the yaml
   Called when object is created
   '''   
   def __init__(self) -> None: 
      # initializing constants 
      self.PARAMETERS:list
      self.dictSymbol:dict
      # template names
      self.COA_TEMPLATE_NAME:str
      self.LABSHEET_TEMPLATE_NAME:str
      self.COA_FAILED_TEMPLATE_NAME:str
      self.LABSHEET_FAILED_TEMPLATE_NAME:str
      # allowed ranges
      self.allowedRangesI:list
      self.allowedRangesII:list
      self.allowedRangesIII:list

      self.loadYaml()

   '''
   Load all constants from config.yaml
   '''
   def loadYaml(self) -> None:
      # open and read config.yaml
      with open("config.yaml", "r") as file:
         stream:dict # type hinting dictionary
         stream = yaml.safe_load(file) # safely load the yaml file

      # setting constants   
      self.PARAMETERS = stream.get('PARAMETERS')
      self.dictSymbol = stream.get('dictSymbol')
      # template names
      self.COA_TEMPLATE_NAME = stream.get('COA_TEMPLATE_NAME')
      self.LABSHEET_TEMPLATE_NAME = stream.get('LABSHEET_TEMPLATE_NAME')
      self.COA_FAILED_TEMPLATE_NAME = stream.get('COA_FAILED_TEMPLATE_NAME')
      self.LABSHEET_FAILED_TEMPLATE_NAME = stream.get('LABSHEET_FAILED_TEMPLATE_NAME')
      # allowed ranges
      self.allowedRangesI = stream.get('allowedRangesI')
      self.allowedRangesII = stream.get('allowedRangesII')
      self.allowedRangesIII = stream.get('allowedRangesIII')

   '''
   Read COA Template docx and write new ranges onto yaml, then reload the yaml
   '''
   def updateConstants(self):
      from docx2python import docx2python
      # extract docx content
      doc_result = docx2python('templates/COA Template.docx').body
      # get separate components of the document
      tolerenceRanges = doc_result[7]
      kovaI = tolerenceRanges[1][1:11]
      kovaII = tolerenceRanges[2][1:11]
      kovaIII = tolerenceRanges[3][1:11]

      for i in kovaI:
         print(i)
      print("\n")
      for i in kovaII:
         print(i)
      print("\n")
      for i in kovaIII:
         print(i)


# for debug use
if __name__ == '__main__':
   c = constants()