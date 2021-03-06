# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 17:53:47 2019

@author: Nagasudhir
Location MWH data = ( Raw WH * CT ratio * PT ratio ) / 10^6
"""

import os
import psycopg2
from warehouse_db_config import getWarehouseDbConfigDict
from fict_master_data import FictMasterData
import datetime as dt
from raw_meter_data_adapter import RawMeterDataAdapter
from freq_code_convert import freqCodeToFreq
from app_utils import intersection
import pandas.io.sql as sqlio
import glob
from itertools import chain
from num_string_parser import NumericStringParser
from fict_location_data_classes import FictLocationDataParser
nsp = NumericStringParser()


class FictLocationEnergyAdapter:
    conn = None
    masterData = None
    processWindow = dt.timedelta(days=1)

    def pushFolderDataToDb(self, folderpath='', recursive=True):
        fileFormats = ['MWH']
        files = [[f for f in glob.glob(
            folderpath + "/**/*." + fileFormat, recursive=True)] for fileFormat in fileFormats]
        files = list(chain.from_iterable(files))
        for filepath in files:
            # remove this section after bulk push
            fName = os.path.basename(filepath)
            if len(fName) > 9:
                print('{0} MWH file push skipped!'.format(filepath))
                continue
            # remove this section after bulk push
            
            # if filepath.length
            isPushSuccess = self.pushFileDataToDb(filepath)
            if isPushSuccess == True:
                print('{0} MWH file push success!'.format(filepath))
            else:
                print('{0} MWH file push failed..,'.format(filepath))

    def pushFileDataToDb(self, filepath):
        txtFile = open(filepath, "r")
        txt = txtFile.read()
        txtFile.close()
        print('{0} MWH file push in progress'.format(filepath))
        isPushSuccess = self.pushFictMwhDataTextToDb(txt)
        return isPushSuccess

    def pushFictMwhDataTextToDb(self, txt):
        txtData = FictLocationDataParser.ParseFictLocationData(txt)
        if txtData == None:
            return False
        blksData = txtData['blksData']
        isPushSuccess = self.pushFictBlksData(blksData)
        return isPushSuccess

    def pushFictBlksData(self, blksData):
        cur = self.conn.cursor()
        # we will commit in multiples of 100 rows
        rowIter = 0
        insIncr = 100
        numRows = len(blksData)
        while rowIter < numRows:
            # set iteration values
            iteratorEndVal = rowIter+insIncr
            if iteratorEndVal >= numRows:
                iteratorEndVal = numRows

            # Create row tuples
            dataInsertionTuples = []
            for insRowIter in range(rowIter, iteratorEndVal):
                dataRow = blksData[insRowIter]

                dataInsertionTuple = (dataRow.data_time.strftime(
                    '%Y-%m-%d %H:%M:%S'), dataRow.location_id, float(dataRow.mwh))
                dataInsertionTuples.append(dataInsertionTuple)

            # prepare sql for insertion and execute
            dataText = ','.join(cur.mogrify('(%s,%s,%s)', row).decode(
                "utf-8") for row in dataInsertionTuples)
            sqlTxt = 'INSERT INTO public.fict_location_energy_data(\
        	data_time, location_id, mwh)\
        	VALUES {0} on conflict (data_time, location_id) \
            do update set mwh = excluded.mwh'.format(dataText)
            cur.execute(sqlTxt)
            self.conn.commit()

            rowIter = iteratorEndVal

        # close cursor and connection
        cur.close()
        return True

    def connectToDb(self):
        warehouseConfigDict = getWarehouseDbConfigDict()
        self.conn = psycopg2.connect(host=warehouseConfigDict['db_host'], dbname=warehouseConfigDict['db_name'],
                                     user=warehouseConfigDict['db_username'], password=warehouseConfigDict['db_password'])

    def disconnectDb(self):
        self.conn.close()

    def loadMasterData(self):
        self.masterData = FictMasterData()
        self.masterData.loadFromDb()

    # extract all operands
    @staticmethod
    def extractLocIdsFromFictFormula(fictForm):
        opStarted = False
        operands = []
        operand = ''
        for c in fictForm:
            if c == '(':
                opStarted = True
            elif c == ')':
                if operand != '':
                    operands.append(operand)
                    operand = ''
                    opStarted = False
            elif opStarted == True:
                operand = operand+c
        return operands

    @staticmethod
    def evalFictFormula(loc_formula, primLocIds, locValSeries):
        newStr = loc_formula
        for locId in primLocIds:
            newStr = newStr.replace(locId, str(locValSeries[locId]))
        return nsp.eval(newStr)

    def deriveFictLocationEnergyForDates(self, fromTime, toTime, locIds=None):
        if toTime < fromTime:
            return

        # make hour minute second components of fromtime and totime as 0
        fromTime = dt.datetime(fromTime.year, fromTime.month, fromTime.day)
        toTime = dt.datetime(toTime.year, toTime.month, toTime.day)

        # check if master data is present
        if self.masterData == None:
            self.loadMasterData()

        # derive the locations to process
        allLocIds = self.masterData.masterDataDf.location_id.tolist()
        reqLocIds = allLocIds
        if not((locIds == None) or (locIds == [])):
            reqLocIds = intersection(locIds, allLocIds)

        if (reqLocIds == None) or (reqLocIds == []):
            return

        # process as per date window
        winStart = fromTime
        while winStart < toTime:
            print(winStart)
            print(dt.datetime.now())
            winEnd = winStart + self.processWindow
            if winEnd > toTime:
                winEnd = toTime
            # process for each location
            for fictLocId in reqLocIds:
                print(fictLocId)
                # get the master data info of fict location for the date
                fictLocMaster = self.masterData.getLocMasterInfo(
                    winStart, fictLocId)

                # get the formula for location Id
                loc_formula = fictLocMaster.loc_formula

                # get the primary locationIds in the formula
                primLocIds = FictLocationEnergyAdapter.extractLocIdsFromFictFormula(
                    loc_formula)

                # get data of primary locations
                cur = self.conn.cursor()
                dataText = ','.join(["'{0}'".format(primLoc)
                                     for primLoc in primLocIds])
                sqlTxt = 'select id, location_id, mwh, data_time \
                    from public.location_energy_data\
                    where location_id in ({0})'.format(dataText)
                primLocDataDf = sqlio.read_sql_query(
                    sqlTxt, self.conn, index_col='id')

                # evaluate fict location energy by formula for each timestamp
                fictLocDataDf = primLocDataDf.pivot(
                    index='data_time', columns='location_id', values='mwh')
                fictLocDataDf['energy'] = fictLocDataDf.apply(
                    lambda f: FictLocationEnergyAdapter.evalFictFormula(loc_formula, primLocIds, f), axis=1)
                # todo data integrity check
                dataInsertionTuples = fictLocDataDf.apply(lambda r: (
                    fictLocId, r.name.strftime('%Y-%m-%d %H:%M:%S'), r.energy), axis=1)
                cur = self.conn.cursor()
                dataText = ','.join(cur.mogrify('(%s,%s,%s)', row).decode(
                    "utf-8") for row in dataInsertionTuples)
                sqlTxt = 'INSERT INTO public.fict_location_energy_data(\
            	location_id, data_time, mwh) VALUES {0} on conflict (data_time, location_id) \
                do update set mwh = excluded.mwh'.format(dataText)
                cur.execute(sqlTxt)
                self.conn.commit()
                cur.close()
                print('{0} Fict Location data update done'.format(fictLocId))
            winStart = winEnd
            print('Completed Fict locations data update at {0}'.format(
                dt.datetime.now()))
