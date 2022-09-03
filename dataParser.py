import utils
import constants

'''
The dataParser file contains all the functionality needed to 
read, parse, process, and wirte the QC results form one machine
'''

# instance var to store serial number in case of error
sn = ''
isErrorMachine = False

"""
Main, driving function in this file. Combines all functions and parses all data in the given file
"""
def generateDocuments(filename:str, tester:str) -> None: 
  # gets list of string from openning the inner text file
  f = utils.openTextFile(filename)

  # keeping count for number of machines
  counter = 1
  # keep running until file runs out
  while f[0] != ['']:
    print("\nMachine %s --------------------------------------------------------------------" % counter)

    # get data
    idInfo = getIdInfo(f)
    rawData = getTests(f)
    print("Serial Number: " + idInfo[0])
    # print("raw data:")
    # for i in rawData:
    #   print(i)
    # print()

    # process data
    cleanData = processData(rawData) 
    print("clean data:")
    for i in cleanData:
      print(i)

    # write data
    writeData(idInfo, cleanData, tester)
    counter += 1

    # DEBUG: print remaining data
    # print("remaining file: ", end=" ")
    # print(f)
    # print()

'''
Must be run before getTests
'''
def getIdInfo(f:list[str]) -> list[str]:
  f = f.copy()
  # line 0 - serial number
  currentLine = f.pop(0)
  serialNum = currentLine[40:53]
  global sn
  sn = serialNum

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
def getTests(f:list[str]) -> list[list[str]]:
  # returning 2d array
  allData = []

  for i in range(6):
    # DEBUG: print("test %s" % (i+1))
    allData.append(utils.getTest(f))

  # print("\n")

  return allData


"""##processData(rawData)"""
def processData(rawData:list[list[str]]):
  # list for organized data
  translatedData = utils.translateData(rawData)

  # CATCH MACHINE ERRORS
  # run testParameters for each control
  utils.testParameters(translatedData, 0, constants.allowedRangesI, sn) # KOVA I
  utils.testParameters(translatedData, 2, constants.allowedRangesII, sn) # KOVA II
  utils.testParameters(translatedData, 4, constants.allowedRangesIII, sn) # KOVA III

  # combine the two tests and return it
  return [utils.combineTestInfo(translatedData[0], translatedData[1]), 
          utils.combineTestInfo(translatedData[2], translatedData[3]),
          utils.combineTestInfo(translatedData[4], translatedData[5])]


"""##writeData(idInfo, cleanData)"""
# writes data to new word doc using template
def writeData(idInfo:list[str], cleanData:list[list[str]], tester:str, hasFailed:bool) -> None:
  testerInitial = ''.join(s[0].upper() for s in tester.split(' '))

  if not hasFailed:
    # mail merge on COA and Lab Worksheet
    utils.mailmergeToTemplates(constants.COA_TEMPLATE_NAME, idInfo, cleanData, testerInitial)
    # mail merge on Lab Worksheet w tester's full name
    utils.mailmergeToTemplates(constants.LABSHEET_TEMPLATE_NAME, idInfo, cleanData, tester)
  else: 
    utils.mailmergeToTemplates(constants.COA_FAILED_TEMPLATE_NAME, idInfo, cleanData, testerInitial)
    utils.mailmergeToTemplates(constants.LABSHEET_FAILED_TEMPLATE_NAME, idInfo, cleanData, tester) 