# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 18:07:45 2019

@author: Nagasudhir

desired database start date - 01-Jan-2016
"""

from raw_meter_data_adapter import RawMeterDataAdapter
import datetime as dt

fromTime = dt.datetime(2019, 9, 2)
toTime = dt.datetime(2020, 4, 30)
adapter = RawMeterDataAdapter()
adapter.connectToDb()

for dayOffset in range((toTime-fromTime).days):
    dayStr = (fromTime+dt.timedelta(days=dayOffset)).strftime('%d%m%y')
    adapter.pushFolderDataToDb(
        folderpath='\\\\10.2.100.171\\c\\SEMBASE\\'+dayStr)
adapter.disconnectDb()
