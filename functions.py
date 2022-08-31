"""
#Main Functions
"""
import lxml
from mailmerge import MailMerge

from utils import *
from constants import *
from gui import testerName

"""##getData(f)"""
# gets data from f, disruptive
# returns dataset of 6 tests, and id info
def getData(f):
  # returning 2d array
  allData = []
  # telling getRaw if it's first or not
  isFirst = True

  # GET ID  INFO
  # line 0 - serial number
  currentLine = f.pop(0)
  serialNum = currentLine[40:53]

  # line 1 - no info
  f.pop(0)

  # line 2 - date and time
  currentLine = f.pop(0)
  date = currentLine[15:25]
  # get yyyy/mm/dd format and add '-' in between
  date = date[6:10] + '-' + date[0:2] + '-' + date[3:5]
  time = currentLine[26:31]

  # for new update
  # date = currentLine[22:30]
  # date = date[0:4] + "-" + date[4:6] + "-" + date[6:8]
  # time = currentLine[30:34]
  # time = time[0:2] + ":" + time[2:4]

  # collect ID info
  idInfo = [serialNum, date, time]

  # GET DATA
  # first test
  # DEBUG: print("test 1")
  allData.append(getTest(f, isFirst))

  # other five tests
  for i in range(5):
    # DEBUG: print("test %s" % (i+2))
    allData.append(getTest(f, not isFirst))

  # print("\n")

  return [allData, idInfo]


"""##processData(rawData)"""
def processData(rawData):
  # list for organized data
  data = []

  # TRANSLATION (size, +/-, and trace)
  # for each test in rawData
  for test in rawData:
    # for each item in test
    # reset tempList
    tempList = []
    for item in test:
      # DEBUG: print("item: " + item, end=" ")
      for word, symbol in dictSymbol.items():
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

  # CATCH MACHINE ERRORS
  # run testParameters for each control
  # then update data for any 'BAD' inserts
  data = testParameters(data, 0, allowedRangesI) # KOVA I
  data = testParameters(data, 2, allowedRangesII) # KOVA II
  data = testParameters(data, 4, allowedRangesIII) # KOVA III

  # combine the two tests and return it
  return [combineTestInfo(data[0], data[1]), 
          combineTestInfo(data[2], data[3]),
          combineTestInfo(data[4], data[5])]


"""##writeData(idInfo, cleanData)"""
# writes data to new word doc using template
def writeData(idInfo, cleanData, tester):
  COA_Template = 'COA Template.docx'
  COA = MailMerge(COA_Template)
  # DEBUG: print(COA_Template.get_merge_fields())

  # merge id info & tester
  COA.merge(
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
      COA.merge(**{mergeField:cleanData[i][j]})
    kovaNumber = kovaNumber + 'I'

  # write new file - serialNum + .docx
  COA_filename = 'COAs/' + str(idInfo[0]) + '.docx'
  COA.write(COA_filename)

"""Generates documents and pulls all functions together (driver function?)"""
def generateDocuments(): 
  # gets list of string from openning the inner text file
  f = openTextFile()

  # keeping count for number of machines
  counter = 1

  # keep running until file runs out
  while f[0] != ['']:
    print("\nMachine %s --------------------------------------------------------------------" % counter)

    # get data
    rawData, idInfo = getData(f)
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
    writeData(idInfo, cleanData, testerName.get())
    counter += 1

    # DEBUG: print remaining data
    # print("remaining file: ", end=" ")
    # print(f)
    # print()