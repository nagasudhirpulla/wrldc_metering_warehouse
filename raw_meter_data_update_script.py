# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 18:07:45 2019

@author: Nagasudhir
"""

from raw_meter_data_adapter import RawMeterDataAdapter
import datetime as dt

fromTime = dt.datetime(2019, 9, 1)
toTime = dt.datetime(2019, 9, 7)
adapter = RawMeterDataAdapter()
adapter.connectToDb()

for dayOffset in range((toTime-fromTime).days):
    dayStr = (fromTime+dt.timedelta(days=dayOffset)).strftime('%d%m%y')
    adapter.pushFolderDataToDb(folderpath='\\\\10.2.100.80\\d\\SEMBASE\\'+dayStr)
adapter.disconnectDb()