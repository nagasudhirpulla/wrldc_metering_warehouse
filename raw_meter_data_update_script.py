# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 18:07:45 2019

@author: Nagasudhir

desired database start date - 01-Jan-2016
"""

from raw_meter_data_adapter import RawMeterDataAdapter
import datetime as dt

fromTime = dt.datetime(2018, 8, 20)
toTime = dt.datetime(2019, 1, 1)
adapter = RawMeterDataAdapter()
adapter.connectToDb()

for dayOffset in range((toTime-fromTime).days):
    dayStr = (fromTime+dt.timedelta(days=dayOffset)).strftime('%d%m%y')
    adapter.pushFolderDataToDb(
        folderpath='\\\\10.2.100.80\\D\\SEMBASE\\'+dayStr)
adapter.disconnectDb()
