# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 17:53:47 2019

@author: Nagasudhir
Location MWH data = ( Raw WH * CT ratio * PT ratio ) / 10^6
"""

import psycopg2
from warehouse_db_config import getWarehouseDbConfigDict
from meter_master_data_classes import MeterMasterData
import datetime as dt
from raw_meter_data_adapter import RawMeterDataAdapter
from  freq_code_convert import freqCodeToFreq

# derive intersection of 2 lists
def intersection(lst1, lst2): 
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3 

class LocationEnergy:
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
        self.masterData = MeterMasterData()
        self.masterData.loadFromDb()
        
    def createLocationEnergyForDates(self, fromTime, toTime, locIds):
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
            winEnd = winStart + self.processWindow
            if winEnd > toTime:
                winEnd = toTime
            # process for each location
            for locId in reqLocIds:
                # get the master data info of location for the date
                locMaster = self.masterData.getLocMasterInfo(winStart, locId)
                # get raw data dataframe for date and then convert to primary data
                primDataDf = RawMeterDataAdapter.getMeterRawBlksDataFromDb(locMaster.meter_id, winStart, winEnd)
                # convert to primary data
                primDataDf = primDataDf[['act_en_wh','freq_code', 'data_time']]
                primDataDf.act_en_wh = primDataDf.act_en_wh*locMaster.ct_ratio*locMaster.pt_ratio*(10**-6)
                primDataDf.data_time = primDataDf.data_time
                primDataDf.freq_code = freqCodeToFreq(primDataDf.freq_code, locMaster.resolution)
                primDataDf.location_id = locMaster.location_id
                primDataDf.rename(columns={"freq_code": "freq", "act_en_wh": "mwh"})
                # todo push each row to db
            winStart = winEnd
