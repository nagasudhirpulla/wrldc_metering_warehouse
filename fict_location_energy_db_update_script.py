# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 10:50:06 2019

@author: Nagasudhir
"""

from fict_location_energy_adapter import FictLocationEnergyAdapter
import datetime as dt
fromTime = dt.datetime(2019, 9, 7)
toTime = dt.datetime(2019, 9, 8)
locEn = FictLocationEnergyAdapter()
locEn.connectToDb()
# locEn.deriveFictLocationEnergyForDates(fromTime, toTime, [])
locEn.pushFolderDataToDb(folderpath='\\\\10.2.100.80\\d\\SEMBASE')
locEn.disconnectDb()
