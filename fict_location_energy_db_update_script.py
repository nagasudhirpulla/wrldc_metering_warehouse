# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 10:50:06 2019

@author: Nagasudhir
"""

from fict_location_energy_adapter import FictLocationEnergyAdapter
import datetime as dt
fromTime = dt.datetime(2020, 4, 1)
toTime = dt.datetime(2020, 7, 1)
locEn = FictLocationEnergyAdapter()
locEn.connectToDb()
# locEn.deriveFictLocationEnergyForDates(fromTime, toTime, [])
for dayOffset in range((toTime-fromTime).days):
    dayStr = (fromTime+dt.timedelta(days=dayOffset)).strftime('%d%m%y')
    locEn.pushFolderDataToDb(folderpath='\\\\10.2.100.171\\c\\SEMBASE\\'+dayStr)
locEn.disconnectDb()
