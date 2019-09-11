# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 12:04:28 2019

@author: Nagasudhir
"""

import pandas as pd


class MeterMasterData:
    '''
    returns meter master data dataframe with columns
    'from_date', 'location_id', 'meter_id', 'ct_ratio', 'pt_ratio', 'description'
    return None in case of problem
    '''
    masterDataDf = None
    def parse(self, filename = 'meter_master_data.xlsx', sheetName=0):
        # read master data excel
        df = pd.read_excel(filename, sheet_name = sheetName)        

        # todo check if the column types are ok
        
        # check if the column names are ok
        reqColNames = ['from_date', 'location_id', 'meter_id', 'ct_ratio', 'pt_ratio', 'description']
        if(df.columns.tolist()[0:6] == reqColNames):
            return None
        
        self.masterDataDf = df
    
    '''
    push data to database table
    '''
    def pushToDb():
        
        
    
    '''
    Returns master data for a given date and meterId
    result is series like below
    from_date                  2019-09-04 00:00:00
    location_id                              KO-01
    meter_id                               hgjhgjh
    ct_ratio                                   500
    pt_ratio                               3636.36
    description    400kV SIDE OF GT1 AT KORBA STPS
    Name: 0, dtype: object
    '''
    def getLocMasterInfo(self, dateObj, locationId):
        df = self.masterDataDf
        filteredDf = df[(df['location_id']==locationId) & (df['from_date']<=dateObj)]
        locMasterInfo = filteredDf.loc[filteredDf['from_date'].idxmax()]
        return locMasterInfo