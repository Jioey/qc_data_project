"""
# Util functions
"""
import lxml
from mailmerge import MailMerge
# import PARAMETERS
from constants import PARAMETERS, COA_TEMPLATE_NAME, LABSHEET_TEMPLATE_NAME

"""openFile()"""
def openTextFile(filename):
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
## getTest(f)
Code to get raw data from file and turn into 2d list
Take data from normal tests (non first)
Returns data of 1 test, in correct order for COA
"""
def getTest(f, isFirst:bool):
  if not isFirst:
    # pop no info lines
    f.pop(0)
    f.pop(0)
    f.pop(0)

  # get the data
  data = []
  for i in range(10):
    # removes first line and stores in currentLine
    currentLine = f.pop(0)
    # parses line by the char '|'
    currentLine = list(filter(None, currentLine.split("|")))
    # DEBUG: print(currentLine)
    # store the wanted data/item
    s = currentLine[5]

    # CHOP UNNECESSARY STUFF OUT OF STRING
    # split into list of words
    s = s.split(' ')
    # get rid of empty items in list
    s = [i for i in s if i]
    # remove '*' if it's in list
    if '*' in s: s.remove('*')
    # remove '*' if it's in the word (index 0 would be the data we're interested in)
    s = s[0].replace('*', '')

    # add the data to the data list
    data.append(s)

  # reverse order for COA -- NOT NEEDED WITH NOT UPDATED SOFTWARE
  # data.reverse()

  # DEBUG:
  # print(data)
  # print("\n")

  # empty string considered False
  # if line is not empty (meaning it's CSR Warning), then pop another line
  # if not then if-statement pop takes away empty line 14  
  if f.pop(0)[0:3] == 'NTE':
    # DEBUG: print('CSR Line!')
    f.pop(0)
  
  return data


"""
##testParameters(data, startInd:int, allowedRanges)
Test parameters for two tests and prints & edits item if it's wrong
Returns modified data set
"""
def testParameters(data, startInd:int, allowedRanges, sn):
  # for two tests
  for i in range(startInd, startInd + 2):
    # for each parameter in each test (10 of them)
    for j in range(10):
      current = data[i][j]
      # if parameter is not in accepted ranges, then warns usr
      if current not in allowedRanges[j]:
        from gui import warn
        warn("Machine %s error in test %s, on element %s, value is %s, should be within %s" % (sn, i, PARAMETERS[j], current, allowedRanges[j]))

  return data


"""
##combineTestInfo(test1, test2)
Combine two tests into one list
Returns combined, clean list
"""
def combineTestInfo(test1, test2):
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

def mailmergeToTemplate(templateName, idInfo, cleanData, tester):
  # open the file using MailMerge
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
      mergeField = 'KOVA-' + kovaNumber + '_' + PARAMETERS[j]
      # merge added field to corresponding data of index
      document.merge(**{mergeField:cleanData[i][j]})
    kovaNumber = kovaNumber + 'I'

  # write new file - serialNum + .docx
  if (templateName == COA_TEMPLATE_NAME):
    fname = 'documents/' + str(idInfo[0]) + '.docx'
  elif (templateName == LABSHEET_TEMPLATE_NAME):
    fname = 'documents/' + str(idInfo[0]) + ' QC Lab Worksheet' + '.docx'
  else:
    raise Exception("template name incorrect")
  document.write(fname)