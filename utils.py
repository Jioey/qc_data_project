import lxml
from mailmerge import MailMerge
from constants import constants

'''
Opens text file and returns a copy of it as a list of string

Args:
    filename (str): The name of the file to be opened

Returns:
    f (list[str]): The text file's content in list format
'''
def openTextFile(filename:str) -> list[str]:
  # open file
  rawFile = open(filename, "r")
  # DEBUG: rawFile = open("demotextOld.txt", "r")

  # turn into list of string and have a copy of original
  f = rawFile.readlines()

  # add lines for program to determine the end of the file
  f.append('')
  f.append('')

  # close file
  rawFile.close()

  # returns a copy of the list of string
  return f.copy()


'''
Gets data of one test from f and turns it into a list

Args:
    f (list[str]): The arg is used as reference to the full file

Returns:
    list[str]: Data/The list of results of one test
    int: kovaKey based on kovaId
'''
def getTest(f:list[str]) -> tuple[list[str], str]:
  # pop out info lines (top)
  f.pop(0)
  kovaID = list(filter(None, f.pop(0).split("|")))[2] # Includes patient id, used for identifying KOVA test
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
    data.append(currentLine[4])

  # reverse order for order on document
  data.reverse()

  # DEBUG: print(data)

  # removes an extra line if there is 
  checkLastLine(f)
  
  # replace w number representing kovaID and raise exception if none found
  kovaKey = {'QUICKTEST':0, 'KOVA I':1, 'KOVA II':2, 'KOVA III':3}.get(kovaID.upper())
  if kovaKey == None:
    raise Exception("Patient ID invalid")

  return data, kovaKey


'''
Checks the line after a test and determine if it should pop an extra line (a warning line),
pop only one line (the empty line between tests), or don't do anything (when there is no empty line between tests)

Args:
    f (list[str]): Used as reference to the full file

Returns:
    None
'''
def checkLastLine(f:list[str]) -> None:  
  # DEBUG: print("f[0] here is: %s" % f[0])
  # if next line starts w NTE, meaning it is a warning line -> pop
  if f[0][0:3] == 'NTE':
    # DEBUG: print('CSR Line found')
    f.pop(0)

  # if next line does not have MSH, meaning it is an empty line btwn tests -> pop
  if f[0][1:4] != 'MSH':
    # DEBUG: print("empty line poped")
    f.pop(0)
  # note: empty line has undeterminable hidden char, so I did it this way 
  # (had to add an extra line at end of file when imported to work w that)

  # do not pop another line if MSH is there, meaning start of next test

'''
'Translates' data - replaces words with symbols based on constants.dictSymbol
e.g. 'Positive' to '(+)'

Args:
    rawData (list[list[str]): The list of data, from results of one machine, to be translated

Returns:
    data (list[list[str]): The translated list of results
'''
def translateData(rawData:list[list[str]], dictSymbol:dict) -> list[list[str]]:
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

  return data


'''
Combines two lists of single test results into one list

Args:
    test1 (list[str]): First list to be combined
    test2 (list[str]): Second list to be combined

Returns:
    list[list[str]]: Combined (and clean-looking) list
'''
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


'''
Using mailMerge to create a COA or Lab Sheet using 
a Word template and the data extracted by the program

Args:
    templateName (str): The name of the Word template to use
    idInfo (list[str]): List of serial number, date, and time
    cleanData (list[list[str]): The processed list of data of one machine
    tester (str): Name of tester to be written on the document

Raises:
    Exception: Template name incorrect

Returns:
    None
'''
def mailmergeToTemplates(templateName:str, idInfo:list[str], cleanData:list[list[str]], tester:str, c:constants) -> None:
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
      mergeField = 'KOVA-' + kovaNumber + '_' + c.PARAMETERS[j]
      # merge added field to corresponding data of index
      document.merge(**{mergeField:cleanData[i][j]})
    kovaNumber = kovaNumber + 'I'

  # set filename based on if QC failed and which document it is (using template name)
  if (templateName == c.COA_TEMPLATE_NAME):
    fname = 'documents/' + str(idInfo[0]) + '.docx'
  elif (templateName == c.LABSHEET_TEMPLATE_NAME):
    fname = 'documents/' + str(idInfo[0]) + ' QC Lab Worksheet' + '.docx'
  elif (templateName == c.COA_FAILED_TEMPLATE_NAME):
    fname = 'failed documents/!' + str(idInfo[0]) + ' - Failed QC' + '.docx'
  elif (templateName == c.LABSHEET_FAILED_TEMPLATE_NAME):
    fname = 'failed documents/!' + str(idInfo[0]) + ' QC Lab Worksheet - Failed QC' + '.docx'
  else:
    raise Exception("Template name incorrect")

  # write new file
  document.write(fname)


# for debug use
if __name__ == '__main__':
  openTextFile('../(905)demotext.txt')