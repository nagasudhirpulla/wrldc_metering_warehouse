# -*- coding: utf-8 -*-
"""
https://www.mkyong.com/python/python-how-to-list-all-files-in-a-directory/
raw meter data files have extension NPD
"""

from raw_meter_data_classes import RawMeterDataParser
import psycopg2
from warehouse_db_config import getWarehouseDbConfigDict
import glob

class RawMeterDataAdapter:
    conn = None    
    def pushFolderDataToDb(self, folderpath='', recursive=True):
        fileFormat = 'NPD'
        files = [f for f in glob.glob(folderpath + "**/*." + fileFormat, recursive=recursive)]
        for filepath in files:
            self.pushFileDataToDb(filepath)
    
    def pushFileDataToDb(self, filepath):
        txtFile = open(filepath, "r")
        txt = txtFile.read()
        txtFile.close()
        self.pushRawMeterDataTextToDb(txt)
    
    def pushRawMeterDataTextToDb(self, txt):
        txtData = RawMeterDataParser.ParseRawMeterData(txt)
        cumData = txtData['cumData']
        blksData = txtData['blksData']
        self.pushRawCumData(cumData)
        self.pushRawBlksData(blksData)            
        
    def connectToDb(self):
        warehouseConfigDict = getWarehouseDbConfigDict()
        self.conn = psycopg2.connect(host=warehouseConfigDict['db_host'], dbname=warehouseConfigDict['db_name'],
                            user=warehouseConfigDict['db_username'], password=warehouseConfigDict['db_password'])
        
    def disconnectDb(self):
        self.conn.close()
        
    def pushRawCumData(self, cumData):
        cur = self.conn.cursor()
        dataInsertionTuple = (cumData.data_time.strftime('%Y-%m-%d %H:%M:%S'), cumData.meter_id, float(cumData.cumm_active_energy_wh), float(cumData.cumm_reactive_energy_high_wh), float(cumData.cumm_reactive_energy_low_wh))
        dataText = cur.mogrify('(%s,%s,%s,%s,%s)', dataInsertionTuple).decode("utf-8")
        sqlTxt = 'INSERT INTO public.raw_meter_cum_data(\
        	data_time, meter_id, cumm_active_energy_wh, cumm_reactive_energy_high_wh, cumm_reactive_energy_low_wh)\
        	VALUES {0} on conflict (data_time, meter_id) \
            do update set cumm_active_energy_wh = excluded.cumm_active_energy_wh, \
            cumm_reactive_energy_high_wh = excluded.cumm_reactive_energy_high_wh, \
            cumm_reactive_energy_low_wh = excluded.cumm_reactive_energy_low_wh'.format(dataText)
        cur.execute(sqlTxt)
        self.conn.commit()
        cur.close()
        print('Raw Cumulative Meter data push done')
    
    def pushRawBlksData(self, blksData):
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
    
                dataInsertionTuple = (dataRow.data_time.strftime('%Y-%m-%d %H:%M:%S'), dataRow.meter_id, dataRow.freq_code, float(dataRow.act_en_wh))
                dataInsertionTuples.append(dataInsertionTuple)
    
            # prepare sql for insertion and execute
            dataText = ','.join(cur.mogrify('(%s,%s,%s,%s)', row).decode("utf-8") for row in dataInsertionTuples)
            sqlTxt = 'INSERT INTO public.raw_meter_data(\
        	data_time, meter_id, freq_code, act_en_wh)\
        	VALUES {0} on conflict (meter_id, data_time) \
            do update set freq_code = excluded.freq_code, act_en_wh = excluded.act_en_wh'.format(dataText)
            cur.execute(sqlTxt)
            self.conn.commit()
    
            rowIter = iteratorEndVal
    
        # close cursor and connection
        cur.close()
        print('Raw Meter data push done')