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
from app_utils import intersection

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
        
    def createLocationEnergyForDates(self, fromTime, toTime, locIds=None):
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
            for locId in reqLocIds:
                # print(locId)
                # get the master data info of location for the date
                locMaster = self.masterData.getLocMasterInfo(winStart, locId)
                # get raw data dataframe for date and then convert to primary data
                primDataDf = RawMeterDataAdapter.getMeterRawBlksDataFromDb(locMaster.meter_id, winStart, winEnd)
                if primDataDf.shape[0] == 0:
                    continue
                # convert to primary data
                primDataDf = primDataDf[['act_en_wh','freq_code', 'data_time']]
                primDataDf.act_en_wh = primDataDf.act_en_wh*locMaster.ct_ratio*locMaster.pt_ratio*(10**-6)
                primDataDf.data_time = primDataDf.data_time
                primDataDf.freq_code = freqCodeToFreq(primDataDf.freq_code, locMaster.resolution)
                dataInsertionTuples = [(locId, r[0], r[1], r[2].strftime('%Y-%m-%d %H:%M:%S')) for r in primDataDf.values]
                cur = self.conn.cursor()
                dataText = ','.join(cur.mogrify('(%s,%s,%s,%s)', row).decode("utf-8") for row in dataInsertionTuples)
                sqlTxt = 'INSERT INTO public.location_energy_data(\
            	location_id, mwh, freq, data_time) VALUES {0} on conflict (data_time, location_id) \
                do update set mwh = excluded.mwh, freq = excluded.freq'.format(dataText)
                cur.execute(sqlTxt)
                self.conn.commit()
                cur.close()
                print('{0} Primary Location data update done'.format(locId))
            winStart = winEnd
