# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 16:41:28 2019

@author: Nagasudhir
"""

import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
from warehouse_db_config import getWarehouseDbConfigDict

class FictMasterData:
    '''
    returns meter master data dataframe with columns
    'from_date', 'location_id', 'formula', 'loc_name', 'description'
    return None in case of problem
    '''
    masterDataDf = None
    
    def PushExcelToDb(self, filename = 'secret/fict_meter_master.xlsx', sheetName=0):
        self.parse(filename, sheetName)
        self.pushToDb()
    
    def parse(self, filename = 'secret/fict_meter_master.xlsx', sheetName=0):
        # read master data excel
        df = pd.read_excel(filename, sheet_name = sheetName)        
        # check if the column names are ok
        reqColNames = ['from_time', 'location_id', 'formula', 'loc_name', 'description']
        if(df.columns.tolist()[0:5] != reqColNames):
            print('columns not as desired in master data excel file')
            return        
        self.masterDataDf = df
    
    '''
    push data to database table, ovewrites existing data
    '''
    def pushToDb(self):
        warehouseConfigDict = getWarehouseDbConfigDict()
        conn = psycopg2.connect(host=warehouseConfigDict['db_host'], dbname=warehouseConfigDict['db_name'],
                            user=warehouseConfigDict['db_username'], password=warehouseConfigDict['db_password'])
        cur = conn.cursor()
        # we will commit in multiples of 1 row
        rowIter = 0
        insIncr = 1
        numRows = self.masterDataDf.shape[0]
        while rowIter < numRows:
            # set iteration values
            iteratorEndVal = rowIter+insIncr
            if iteratorEndVal >= numRows:
                iteratorEndVal = numRows
    
            # Create row tuples
            dataInsertionTuples = []
            for insRowIter in range(rowIter, iteratorEndVal):
                dataRow = self.masterDataDf.iloc[insRowIter]
    
                dataInsertionTuple = (dataRow.from_time.strftime('%Y-%m-%d %H:%M:%S'), dataRow.location_id, dataRow.formula, dataRow.loc_name, dataRow.description)
                dataInsertionTuples.append(dataInsertionTuple)
    
            # prepare sql for insertion and execute
            dataText = ','.join(cur.mogrify('(%s,%s,%s,%s,%s)', row).decode("utf-8") for row in dataInsertionTuples)
            cur.execute('INSERT INTO public.fict_master_data(\
        	from_time, location_id, loc_formula, loc_name, description)\
        	VALUES {0} on conflict (from_time, location_id) \
            do update set loc_formula = excluded.loc_formula, loc_name = excluded.loc_name, description = excluded.description'.format(dataText))
            conn.commit()
    
            rowIter = iteratorEndVal
    
        # close cursor and connection
        cur.close()
        conn.close()
        print('Fict meter Master data overwrite done')
        
    '''
    Loads master data from db
    '''
    def loadFromDb(self):
        warehouseConfigDict = getWarehouseDbConfigDict()
        conn = psycopg2.connect(host=warehouseConfigDict['db_host'], dbname=warehouseConfigDict['db_name'],
                            user=warehouseConfigDict['db_username'], password=warehouseConfigDict['db_password'])
        sql = "select * from fict_master_data;"
        df = sqlio.read_sql_query(sql, conn, index_col='id')
        conn = None
        self.masterDataDf   = df
    
    '''
    Returns master data for a given date and meterId
    result is series like below
    from_date                  2019-09-04 00:00:00
    location_id                              KO-01
    meter_id                               hgjhgjh
    ct_ratio                                   500
    pt_ratio                               3636.36
    status                                       M
    description    400kV SIDE OF GT1 AT KORBA STPS
    Name: 0, dtype: object
    '''
    def getLocMasterInfo(self, dateObj, locationId):
        df = self.masterDataDf
        filteredDf = df[(df.location_id==locationId) & (df.from_time<=dateObj)]
        locMasterInfo = filteredDf.loc[filteredDf.from_time.idxmax()]
        return locMasterInfo