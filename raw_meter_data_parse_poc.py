# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:06:04 2019

@author: Nagasudhir
"""


from raw_meter_data_adapter import RawMeterDataAdapter

adapter = RawMeterDataAdapter()
adapter.connectToDb()
adapter.pushFolderDataToDb()
adapter.disconnectDb()