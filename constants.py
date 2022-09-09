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
      self.PARAMETERS:list
      self.TEMPLATE_NAMES:list
      self.allowedRangesI:list
      self.allowedRangesII:list
      self.allowedRangesIII:list
      self.dictSymbol:dict

      self.loadYaml()

   '''
   Load constants from yaml
   '''
   def loadYaml(self):
      with open("example.yaml", "r") as stream:
         try:
            print(yaml.safe_load(stream))
         except yaml.YAMLError as exc:
            print(exc)

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
   c.loadYaml()