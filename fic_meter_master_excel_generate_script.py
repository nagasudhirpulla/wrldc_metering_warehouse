# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:43:30 2019

@author: Nagasudhir

if cfg line starts with a number, then it is the location definition line.
for location formula, strip the lines below the definition line till the next locaion definition
"""
import sys
import pandas as pd

outFilePath = 'secret/fict_meter_excel.xlsx'
outSheetName = 'Sheet1'
# read the cfg file and dat file in the folder
inputCfgPath = 'secret/FICTMTRS.CFG'
inputDatPath = 'secret/FICTMTRS.DAT'

# parse the cfg file
txtFile = open(inputCfgPath, "r")
txt = txtFile.read()
txtFile.close()
txtLines = txt.splitlines()
# find the line which starts with START
pageStartLineInd = -1
for lineIter in range(len(txtLines)):
    if txtLines[lineIter].startswith("START"):
        pageStartLineInd = lineIter + 1
        break

if pageStartLineInd == -1:
    sys.exit('page start not found')
# find the line which starts with END
pageEndLineInd = pageStartLineInd
for lineIter in range(pageStartLineInd, len(txtLines)):
    if txtLines[lineIter].startswith("END"):
        pageEndLineInd = lineIter -1
        break

if pageEndLineInd == -1:
    sys.exit('page end not found')

# find the word segements till before description
cfgCols = ['location_id', 'formula']
cfgRows = []
lineIter = pageStartLineInd
while lineIter <= pageEndLineInd:
    # for name of meter strip the text between ()
    locLineText = txtLines[lineIter]
    loc_name = locLineText[locLineText.find("(")+1:locLineText.find(")")]
    locLineFound = False
    lineIter = lineIter + 1
    formulaText = ""
    # iterate through next lines till we dont start with number
    while (locLineFound != True and lineIter <= pageEndLineInd):
        lineText = txtLines[lineIter]
        if lineText[0].isdigit():
            locLineFound = True
        else:
            formulaText = formulaText + lineText
            lineIter = lineIter+1
    formulaText = formulaText.replace(' ', '').replace('\t', '')
    cfgRows.append([loc_name, formulaText])
cfgDf = pd.DataFrame(data=cfgRows, columns=cfgCols)

# parse the dat file
txtFile = open(inputDatPath, "r")
txt = txtFile.read()
txtFile.close()
txtLines = txt.splitlines()
# find the line which starts with ---
pageStartLineInd = -1
for lineIter in range(len(txtLines)):
    if txtLines[lineIter].startswith("---"):
        pageStartLineInd = lineIter + 1
        break

if pageStartLineInd == -1:
    sys.exit('page start not found')
# find the line which starts with ---
pageEndLineInd = pageStartLineInd
for lineIter in range(pageStartLineInd, len(txtLines)):
    if txtLines[lineIter].startswith("---"):
        pageEndLineInd = lineIter -1
        break

if pageEndLineInd == -1:
    sys.exit('page end not found')

# find the word segements till before description
datCols = ['location_id', 'loc_name', 'description']
datRows = []
for lineIter in range(pageStartLineInd, pageEndLineInd):
    # for name of meter strip the text between ()
    lineText = txtLines[lineIter]
    lineWords = lineText.split(None, 2)
    datRows.append(lineWords)    
datDf = pd.DataFrame(data=datRows, columns=datCols)

# join dat and cfg dataframes on the column location_id
fictDf = pd.merge(cfgDf, datDf, on='location_id', how='left')
fictDf.to_excel(outFilePath, sheet_name=outSheetName, index=False)