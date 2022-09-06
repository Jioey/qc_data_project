import utils
import constants

'''
The dataParser file contains all the functionality needed to 
read, parse, process, and wirte the QC results form one machine
'''
class dataParser():
  def __init__(self) -> None:
# instance var to store serial number in case of error
    self.sn = ''
    # has machine failed QC
    self.hasFailed = False
    # list of error msgs displayed to usr
    self.errMsg = ''


"""
Main, driving function in this file. Combines all functions and parses all data in the given file
"""
  def generateDocuments(self, filename:str, tester:str) -> None: 
  # gets list of string from openning the inner text file
  f = utils.openTextFile(filename)

  # keeping count for number of machines
  counter = 1
  # keep running until file runs out
  while f[0] != ['']:
    print("\nMachine %s --------------------------------------------------------------------" % counter)

    # get data
      idInfo = self.getIdInfo(f)
      rawData = self.getTests(f)
    print("Serial Number: " + idInfo[0])
    # print("raw data:")
    # for i in rawData:
    #   print(i)
    # print()

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
Must be run before getTests
'''
  def getIdInfo(self, f:list[str]) -> list[str]:
  f = f.copy()
  # line 0 - serial number
  currentLine = f.pop(0)
  serialNum = currentLine[40:53]
    # set serial number to current one in class
    self.sn = serialNum

  # line 1 - no info
  f.pop(0)

  # line 2 - date and time
  currentLine = f.pop(0)                                # for new update in TC-201
  date = currentLine[15:25]                             # date = currentLine[22:30]
  # get yyyy/mm/dd format and add '-' in between          date = date[0:4] + "-" + date[4:6] + "-" + date[6:8]
  date = date[6:10] + '-' + date[0:2] + '-' + date[3:5] # time = currentLine[30:34]
  time = currentLine[26:31]                             # time = time[0:2] + ":" + time[2:4]

  # collect ID info
  return [serialNum, date, time]


"""##getData(f)"""
# gets data from f, disruptive
# returns dataset of 6 tests, and id info
  def getTests(self, f:list[str]) -> list[list[str]]:
  # returning 2d array
  allData = []

  for i in range(6):
    # DEBUG: print("test %s" % (i+1))
    allData.append(utils.getTest(f))

  # print("\n")

  return allData


"""##processData(rawData)"""
  def processData(self, rawData:list[list[str]]) -> list[list[str]]:
  # list for organized data
  translatedData = utils.translateData(rawData)

  # CATCH MACHINE ERRORS
  # run testParameters for each control
    self.testParameters(translatedData, 0, constants.allowedRangesI, self.sn) # KOVA I
    self.testParameters(translatedData, 2, constants.allowedRangesII, self.sn) # KOVA II
    self.testParameters(translatedData, 4, constants.allowedRangesIII, self.sn) # KOVA III

  # combine the two tests and return it
  return [utils.combineTestInfo(translatedData[0], translatedData[1]), 
          utils.combineTestInfo(translatedData[2], translatedData[3]),
          utils.combineTestInfo(translatedData[4], translatedData[5])]


"""##writeData(idInfo, cleanData)"""
# writes data to new word doc using template
  def writeData(self, idInfo:list[str], cleanData:list[list[str]], tester:str) -> None:
  testerInitial = ''.join(s[0].upper() for s in tester.split(' '))

    if not self.hasFailed:
    # mail merge on COA and Lab Worksheet
    utils.mailmergeToTemplates(constants.COA_TEMPLATE_NAME, idInfo, cleanData, testerInitial)
    # mail merge on Lab Worksheet w tester's full name
    utils.mailmergeToTemplates(constants.LABSHEET_TEMPLATE_NAME, idInfo, cleanData, tester)
  else: 
      # if has failed QC, then output using failed templates
    utils.mailmergeToTemplates(constants.COA_FAILED_TEMPLATE_NAME, idInfo, cleanData, testerInitial)
    utils.mailmergeToTemplates(constants.LABSHEET_FAILED_TEMPLATE_NAME, idInfo, cleanData, tester) 