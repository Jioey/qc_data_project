"""
# Util functions
"""
# import PARAMETERS
from constants import PARAMETERS

"""openFile()"""
def openTextFile():
  # open file
  # TODO: figure out and discuss how to read local file in location?
  # TODO: Change txt filename
  # rawFile = open("demotextOld.txt", "r")
  rawFile = open("all results.txt", "r")

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
def testParameters(data, startInd:int, allowedRanges):
  # for two tests
  for i in range(startInd, startInd + 2):
    # for each parameter in each test (10 of them)
    for j in range(10):
      current = data[i][j]
      # if parameter is not in accepted ranges
      if current not in allowedRanges[j]:
        # print string w info of BAD parameter
        print("Machine error in test %s, on element %s, value is %s, should be within %s" % (i, PARAMETERS[j], current, allowedRanges[j]))
        # adds 'BAD' to parameter to be human spotted in resulting excel table - DON'T KNOW IF WORKS BUT NOT CODE-BREAKING
        current = 'BAD ' + current

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