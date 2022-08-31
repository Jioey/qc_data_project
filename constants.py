"""##Constants"""
# TODO: Maybe change to enums?
# name of all parameters tested, in correct order
PARAMETERS = ['LEU', 'NIT', 'URO', 'PRO', 'pH', 'BLO', 'SG', 'KET', 'BIL', 'GLU']

# list of acceptable parameters for each control (technically a list, NOT dict)

# in order of PARAMETERS
allowedRangesI = [['1+', '2+', '3+'], ['(+)'], ['4.0', '\u22658.0'], ['100', '\u2265300'], ['6.5', '7.0', '7.5', '8.0'], ['2+', '3+'], ['1.010', '1.015', '1.020', '1.025'], ['40', '\u226580'], ['2+', '3+'], ['500', '1000']]
allowedRangesII = [['1+', '2+', '3+'], ['(+)'], ['0.2', '1.0'], ['TRA', '30'], ['7.0', '7.5', '8.0', '8.5'], ['1+', '2+'], ['1.005', '1.010', '1.015'], ['TRA', '15', '40'], ['(-)', '1+'], ['100', '250']]
allowedRangesIII = [['(-)'], ['(-)'], ['0.2', '1.0'], ['(-)'], ['5.0', '5.5', '6.0', '6.5'], ['(-)'], ['1.005', '1.010', '1.015'], ['(-)'], ['(-)'], ['(-)']]

# dictionary for translation
dictSymbol = {'Small':'1+', 'Moderate':'2+', 'Large':'3+', 'Positive':'(+)', 'Negative':'(-)', 'Trace':'TRA', '>=':'\u2265'}

# row and column name for dataframe (technically not dict too)
ROW_NAME = ['Control', 'KOVA I', 'KOVA II', 'KOVA III']
COL_NAME = PARAMETERS

# inner file name
INNER_FILE_NAME = 'all results.txt'