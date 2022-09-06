"""
# Util functions
"""
import lxml
from mailmerge import MailMerge
# import constants
import constants

"""openFile()"""
def openTextFile(filename:str) -> list[str]:
  # open file
  rawFile = open(filename, "r")
  # DEBUG: rawFile = open("demotextOld.txt", "r")

  # turn into list of string and have a copy of original
  f = rawFile.readlines()

  # add an empty line - don't know why but fixed bug?
  f.append([''])

  # close file
  rawFile.close()

  # returns a copy of the list of string
  return f.copy()

"""
The getTest function gets unprocessed data from file
and processes one test
Returns data of 1 test, in correct order for COA

Args:
  f (list): The arg is used as reference to the full file

Returns:
  data 
"""
def getTest(f:list[str]) -> list[str]:
  # pop out info lines (top)
  f.pop(0)
  f.pop(0)
  f.pop(0)

  # get the data
  data = []
  for i in range(10):
    # removes top-most line and stores in currentLine
    currentLine = f.pop(0)
    # parses line by the char '|'
    currentLine = list(filter(None, currentLine.split("|")))
    # DEBUG: print(currentLine)
    # add the data to the data list
    data.append(parseResultStr(currentLine[5]))

  # DEBUG: print(''.join(data, '\n'))

  # removes an extra line if there is 
  checkWarningLine(f)
  
  return data

'''
The parseResultStr function takes a unparsed string of a data point
and extracts the substring of the data point

Args:
  s (str): The arg is the unparsed string

Returns:
  s (str): The parsed string
'''
def parseResultStr(s:str) -> str:
  # split into list of words
  s = s.split(' ')
  # get rid of empty items in list
  s = [i for i in s if i]
  # remove '*' if it's in list
  if '*' in s: s.remove('*')
  # remove '*' if it's in the word (index 0 would be the data we're interested in)
  s = s[0].replace('*', '')

  return s

'''
The checkWarningLine function checks if there is a CSR warning line at the end of a test
and removes it if there is 

Args:
  f (list): The arg is used as reference to the full file

Returns:
  True if a CSR line is removed and False if not
'''
def checkWarningLine(f:list[str]) -> bool:
  # empty string considered False
  # if line is not empty (meaning it's CSR Warning), then pop another line
  # if not then if-statement pop takes away empty line 14  
  if f.pop(0)[0:3] == 'NTE':
    # DEBUG: print('CSR Line found')
    f.pop(0)
    return True
  return False


"""
##testParameters(data, startInd:int, allowedRanges)
Test parameters for two tests and prints & edits item if it's wrong
Returns modified data set
"""
def testParameters(data:list[list[str]], startInd:int, allowedRanges:list[str], sn:str) -> None:
  # for two tests
  for i in range(startInd, startInd + 2):
    # for each parameter in each test (10 of them)
    for j in range(10):
      current = data[i][j]
      # if parameter is not in accepted ranges, then warns usr
      if current not in allowedRanges[j]:
        from gui import warn
        warn("Machine %s error in test %s of KOVA %s, on element %s, value is %s, should be within %s" % (sn, i%2, round(i/2)+1, constants.PARAMETERS[j], current, allowedRanges[j]))


def translateData(rawData:list[list[str]]) -> list[list[str]]:
  data = []
  # TRANSLATION (size, +/-, and trace)
  # for each test in rawData
  for test in rawData:
    # for each item in test
    # reset tempList
    tempList = []
    for item in test:
      # DEBUG: print("item: " + item, end=" ")
      for word, symbol in constants.dictSymbol.items():
        # replace item string
        item = item.replace(word, symbol)
      # DEBUG: print("trans: " + item, end=" ")
      # store the replaced string to tempList
      tempList.append(item)
    # add tempList to data
    data.append(tempList)

    # DEBUG: printing the translated list
    # print("translated list:")
    # for i in data:
    #   print(i)
    # print('\n\n')

  return data

"""
##combineTestInfo(test1, test2)
Combine two tests into one list
Returns combined, clean list
"""
def combineTestInfo(test1:list[str], test2:list[str]) -> list[str]:
  # reset tempList
  tempList = []
  # index for adding \n in SG parameter
  index = 0

  # for every item in first two tests
  for a, b in zip(test1, test2):
    # combine to one string, add '/', then add to tempList
    if index == 6:
      # add a \n btwn for SG (param index 6)
      tempList.append(a + '/\n' + b)
    else:
      tempList.append(a + '/' + b)
    index += 1

  # return combined list
  return tempList

def mailmergeToTemplates(templateName:str, idInfo:list[str], cleanData:list[list[str]], tester:str) -> None:
  # open the template using MailMerge
  document = MailMerge('templates/' + templateName)
  # DEBUG: print(document.get_merge_fields())

  # merge id info & tester
  document.merge(
    **{'serial_number':idInfo[0],
    'date':idInfo[1],
    'tester':tester}
    )

  # for each of the 3 controls 
  kovaNumber = 'I'
  for i in range(3):
    # for each parameter in each control
    for j in range(10):
      # concatinate merge field/name; starting with 'KOVA-I_LEU' (KOVA-[controlNumber]_[parameterName])
      mergeField = 'KOVA-' + kovaNumber + '_' + constants.PARAMETERS[j]
      # merge added field to corresponding data of index
      document.merge(**{mergeField:cleanData[i][j]})
    kovaNumber = kovaNumber + 'I'

  # set filename based on if QC failed and which document it is (using template name)
  if (templateName == constants.COA_TEMPLATE_NAME):
    fname = 'documents/' + str(idInfo[0]) + '.docx'
  elif (templateName == constants.LABSHEET_TEMPLATE_NAME):
    fname = 'documents/' + str(idInfo[0]) + ' QC Lab Worksheet' + '.docx'
  elif (templateName == constants.COA_FAILED_TEMPLATE_NAME):
    fname = 'failed documents/!' + str(idInfo[0]) + ' - Failed QC' + '.docx'
  elif (templateName == constants.LABSHEET_FAILED_TEMPLATE_NAME):
    fname = 'failed documents/!' + str(idInfo[0]) + ' QC Lab Worksheet - Failed QC' + '.docx'
  else:
    raise Exception("template name incorrect")

  # write new file
  document.write(fname)