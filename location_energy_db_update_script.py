# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 10:50:06 2019

@author: Nagasudhir
"""

from location_energy_classes import LocationEnergy
import datetime as dt
fromTime = dt.datetime(2020, 4, 1)
toTime = dt.datetime(2020, 4, 20)
locEn = LocationEnergy()
locEn.connectToDb()
locEn.createLocationEnergyForDates(fromTime, toTime, [])
locEn.disconnectDb()