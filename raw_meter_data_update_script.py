# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 18:07:45 2019

@author: Nagasudhir
"""

from raw_meter_data_adapter import RawMeterDataAdapter

adapter = RawMeterDataAdapter()
adapter.connectToDb()
adapter.pushFolderDataToDb(folderpath='\\\\10.2.100.80\\d\\SEMBASE\\130919')
adapter.disconnectDb()