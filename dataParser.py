import utils
from constants import constants


class dataParser():
  '''
  The dataParser file contains all the functionality needed to 
  read, parse, process, and wirte the QC results

  Attributes:
    sn (str): storing the serial number of the current machine
    hasFailed (bool): stores if the current machine has failed QC
    c (constants): reference to the constants obj
  '''
  def __init__(self, c:constants) -> None:
    # instance var to store serial number in case of error
    self.sn = ''
    self.hasFailed = False
    self.c = c


  '''
  Main, driving function of this object
  Combines all functions and parses all data in the given file

  Args:
      filename (str): Used to open the txt file storing results
      tester (str): Used to write tester name on the documents

  Returns:
      None
  '''
  def generateDocuments(self, filename:str, tester:str) -> None: 
    # gets list of string from openning the inner text file
    f = utils.openTextFile(filename)

    # keeping count for number of machines
    counter = 1
    # keep running until file runs out
    while f[0] != '':
      print("\nMachine %s --------------------------------------------------------------------" % counter)
      # get data
      idInfo = self.getIdInfo(f)
      rawData = self.getTests(f)
      print("Serial Number: " + idInfo[0])
      # print("raw data:")
      # for i in rawData:
      #   print(i)
      # print()
      
      # initialize hasFailed
      self.hasFailed = False
      # set serial number for each machine
      self.sn = idInfo[0]

      # process data
      cleanData = self.processData(rawData) 
      print("clean data:")
      for i in cleanData:
        print(i)

      # write data
      self.writeData(idInfo, cleanData, tester)
      counter += 1

      # DEBUG: print remaining data
      # print("remaining file: ", end=" ")
      # print(f)
      # print()


  '''
  Gets serial number, date, and time from the txt file
  Must be run before getTests!!

  Args:
      f (list[str]): txt file in the format of a list of str

  Returns:
      list[str]: A list storing, in order, the serial number, date, and time
  '''
  def getIdInfo(self, f:list[str]) -> list[str]:
    f = f.copy()
    # line 0 - serial number
    currentLine = f.pop(0)
    # split current line by seperator
    currentLine = list(currentLine.split("|"))
    serialNum = currentLine[3][10:23]

    # line 1 - no info
    f.pop(0)

    # line 2 - date and time
    currentLine = f.pop(0) 
    # split current line by seperator
    currentLine = list(filter(None, currentLine.split("|")))
    # get the item; it has date AND time
    date = currentLine[4]
    # get and format the date
    date = date[0:4] + "-" + date[4:6] + "-" + date[6:8]
    # get and format the time
    time = date[8:10] + ":" + date[10:12]

    # collect ID info
    return [serialNum, date, time]


  '''
  Gets the test data of one machine from f and turns it into a 2D list
  WARNING: deletes each line as the code traverses through f

  Args:
      f (list[str]): txt file in the format of a list of str
  
  Returns:
      list[list[str]]: A 2D list of string containing results of all tests performed on one machine
  '''
  def getTests(self, f:list[str]) -> list[list[str]]:
    # returning 2d array
    allData = []

    for i in range(6):
      # DEBUG: print("test %s" % (i+1))
      allData.append(utils.getTest(f))
    # print("\n")

    # reorganize data list in KOVA I, II, III, I, II, III order
    kovaOrder = [0, 3, 1, 4, 2, 5]
    allData = [allData[i] for i in kovaOrder]
    for i in allData:
      print(i)    

    return allData


  '''
  Processes the 2D list outputted by getTests to the format to be written on the documents.
  Including sorting the list in KOVA order, 'translate' to symbols (when necessary, e.g. (+)), error check, 
  and combines two lists (tests) of one KOVA to one list

  Args:
      rawData (list[str]): 2D list of test results, taken straight from the txt
  
  Returns:
      list[list[str]]: A 2D list of string of results of tests from one machine, after processing it to the format written on the documents
  '''
  def processData(self, rawData:list[list[str]]) -> list[list[str]]:
    # list for organized data
    translatedData = utils.translateData(rawData, self.c.dictSymbol)

    # ERROR CHECK MACHINES
    # run testParameters for each control
    self.testParameters(translatedData, 0, self.c.allowedRangesI, self.sn) # KOVA I
    self.testParameters(translatedData, 2, self.c.allowedRangesII, self.sn) # KOVA II
    self.testParameters(translatedData, 4, self.c.allowedRangesIII, self.sn) # KOVA III

    # combine the two tests and return it
    return [utils.combineTestInfo(translatedData[0], translatedData[1]), 
            utils.combineTestInfo(translatedData[2], translatedData[3]),
            utils.combineTestInfo(translatedData[4], translatedData[5])]


  '''
  Test parameters for two tests and prints & edits item if it's wrong

  Args:
      f (list[str]): txt file in the format of a list of str
  
  Returns:
      list[list[str]]: A 2D list of string containing results of all tests performed on one machine
  '''
  def testParameters(self, data:list[list[str]], startInd:int, allowedRanges:list[str], sn:str) -> None:
    # for two tests
    for i in range(startInd, startInd + 2):
      # for each parameter in each test (10 of them)
      for j in range(10):
        current = data[i][j]
        # if parameter is not in accepted ranges, then warns usr
        if current not in allowedRanges[j]:
          from gui import warn
          self.hasFailed = True
          indexMapping = {0:'0', 1:'3', 2:'1', 3:'4', 4:'2', 5:'5'}
          warn("Machine %s error in test %s, KOVA %s, on element %s, value is %s, should be within %s" % (sn, indexMapping.get(i), int((startInd/2)+1), self.c.PARAMETERS[j], current, allowedRanges[j]))
   
        
  '''
  Writes data to new word doc (COA and Lab Worksheet) using templates

  Args:
      idInfo (list[str]): serial num, date, and time in a list (as outputted by getIdInfo())
      cleanData (list[str]): txt file in the format of a list of str
      tester (str): tester name to be written on to the documents
  
  Returns:
      None
  '''
  # writes data to new word doc using template
  def writeData(self, idInfo:list[str], cleanData:list[list[str]], tester:str) -> None:
    testerInitial = ''.join(s[0].upper() for s in tester.split(' '))

    if not self.hasFailed:
      # mail merge on COA and Lab Worksheet
      utils.mailmergeToTemplates(self.c.COA_TEMPLATE_NAME, idInfo, cleanData, testerInitial, self.c)
      # mail merge on Lab Worksheet w tester's full name
      utils.mailmergeToTemplates(self.c.LABSHEET_TEMPLATE_NAME, idInfo, cleanData, tester, self.c)
    else: 
      # if has failed QC, then output using failed templates
      utils.mailmergeToTemplates(self.c.COA_FAILED_TEMPLATE_NAME, idInfo, cleanData, testerInitial, self.c)
      utils.mailmergeToTemplates(self.c.LABSHEET_FAILED_TEMPLATE_NAME, idInfo, cleanData, tester, self.c) 