# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:06:04 2019

@author: Nagasudhir
"""


from raw_meter_data_classes import RawMeterDataParser

txtFile = open("raw_meter_data_sample.txt", "r")
txt = txtFile.read()
txtFile.close()
data = RawMeterDataParser.ParseRawMeterData(txt)
print(data['cumData'].dict())
print(data['blksData'][0].dict())
print('Number of blocks = {0}'.format(len(data['blksData'])))