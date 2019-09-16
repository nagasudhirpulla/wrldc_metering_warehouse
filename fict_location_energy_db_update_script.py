# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 10:50:06 2019

@author: Nagasudhir
"""

from fict_location_energy_classes import FictLocationEnergy
import datetime as dt
fromTime = dt.datetime(2019, 9, 7)
toTime = dt.datetime(2019, 9, 8)
locEn = FictLocationEnergy()
locEn.connectToDb()
locEn.createFictLocationEnergyForDates(fromTime, toTime, [])
locEn.disconnectDb()