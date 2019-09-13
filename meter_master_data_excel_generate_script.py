# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 12:29:12 2019

@author: Nagasudhir
"""
import sys
import pandas as pd
inputFilePath = 'secret/MASTER_T.DAT'
outputFilePath = 'secret/master_data.xlsx'
outSheetName = 'Sheet1'

txtFile = open(inputFilePath, "r")
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

pageEndLineInd = pageStartLineInd
for lineIter in range(pageStartLineInd, len(txtLines)):
    if txtLines[lineIter].startswith("---"):
        pageEndLineInd = lineIter -1
        break

if pageEndLineInd == -1:
    sys.exit('page end not found')

# find the word segements till before description
dataColumnNames = ['location_id', 'meter_id', 'ct_ratio', 'pt_ratio', 'status', 'description']
dataRows = []
for lineIter in range(pageStartLineInd, pageEndLineInd+1):
    dataRow = txtLines[lineIter].split(None, 5)
    try:
        dataRow[2] = int(dataRow[2])
        dataRow[3] = float(dataRow[3])
    except:
        dataRow[2] = 0
        dataRow[3] = 0
    dataRows.append(dataRow)
dataDf = pd.DataFrame(data=dataRows, columns=dataColumnNames)
dataDf.to_excel(outputFilePath, sheet_name=outSheetName, index = False)