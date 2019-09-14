# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 17:53:47 2019

@author: Nagasudhir
Location MWH data = ( Raw WH * CT ratio * PT ratio ) / 10^6
"""

import psycopg2
from warehouse_db_config import getWarehouseDbConfigDict
from fict_meter_classes import FictMasterData
import datetime as dt
from raw_meter_data_adapter import RawMeterDataAdapter
from  freq_code_convert import freqCodeToFreq
from app_utils import intersection

class FictLocationEnergy:
    conn = None
    masterData = None
    processWindow = dt.timedelta(days=1)
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
            if c=='(':
                opStarted = True
            elif c==')':    
                if operand!='':
                    operands.append(operand)
                    operand=''
                    opStarted = False
            elif opStarted == True:
                operand = operand+c
        return operands
    
    def createFictLocationEnergyForDates(self, fromTime, toTime, locIds=None):
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
                fictLocMaster = self.masterData.getLocMasterInfo(winStart, fictLocId)
                # get the formula for location Id
                loc_formula = fictLocMaster.loc_formula
                # get the primary locationIds in the formula
                primLocIds = FictLocationEnergy.extractLocIdsFromFictFormula(loc_formula)
                # todo complete this
                print('Fict Location data update done')
            winStart = winEnd