# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:18:25 2019

@author: Nagasudhir


Raw meter data has 26 lines (check 1)

first and last lines have the following data delimited by spaces
meter_number, cumm_active_energy (Watt Hour), cumm_reactive_high (Watt Hour), cumm_reactive_low (Watt Hour), date (MM-dd-yy)
CG-1006-A  66548.2   4776.2     28.2  01-02-15

Remaining line has the following data delimited by spaces
hour_of_day, blk1_freq_code, blk1_active energy(Watt Hour), … till block 4
03  51   +15.62  50   +15.41  50   +15.45  52   +15.41
"""

import datetime as dt

class RawMeterCumData:
    data_time = None
    meter_id = None
    cumm_active_energy_wh = None
    cumm_reactive_energy_high_wh = None
    cumm_reactive_energy_low_wh = None
    def __init__(self, data_time, meter_id, cumm_active_energy_wh, cumm_reactive_energy_high_wh, cumm_reactive_energy_low_wh):
        self.meter_id = meter_id
        self.cumm_active_energy_wh = cumm_active_energy_wh
        self.cumm_reactive_energy_high_wh = cumm_reactive_energy_high_wh
        self.cumm_reactive_energy_low_wh = cumm_reactive_energy_low_wh
        self.data_time = data_time
    
    @staticmethod
    def parse(txtLine):
        strs = txtLine.split()
        # check if we have 5 words
        if len(strs) != 5:
            return None
        meter_id = strs[0]
        cumm_active_energy_wh = float(strs[1])
        cumm_reactive_energy_high_wh = float(strs[2])
        cumm_reactive_energy_low_wh = float(strs[3])
        data_time = dt.datetime.strptime(strs[4], '%m-%d-%y').date()
        meterHeader = RawMeterCumData(data_time, meter_id, cumm_active_energy_wh, cumm_reactive_energy_high_wh, cumm_reactive_energy_low_wh)
        return meterHeader
    
    def dict(self):
        return self.__dict__

class RawMeterData:
    data_time = None
    meter_id = None
    freq_code = None
    act_en_wh = None
    def __init__(self, data_time, meter_id, freq_code, act_en_wh):
        self.data_time = data_time
        self.meter_id = meter_id
        self.freq_code = freq_code
        self.act_en_wh = act_en_wh
    
    @staticmethod
    def parse(date_obj, meter_id, txtLine):
        strs = txtLine.split()
        # check if we have 9 words
        if len(strs) != 9:
            return None
        hr = int(strs[0])
        blkFreqCodes = [int(strs[1]), int(strs[3]), int(strs[5]), int(strs[7])]
        blkActEns = [float(strs[2]), float(strs[4]), float(strs[6]), float(strs[8])]
        dataRes = []
        for blkNum in range(0, 4):
            data_time = dt.datetime(date_obj.year, date_obj.month, date_obj.day, hr, 0, 0) + dt.timedelta(minutes=15*blkNum)
            blkData = RawMeterData(data_time, meter_id, blkFreqCodes[blkNum], blkActEns[blkNum])
            dataRes.append(blkData)
        return dataRes
    
    def dict(self):
        return self.__dict__

class RawMeterDataParser:
    @staticmethod
    def ParseRawMeterData(txt):
        txtLines = txt.splitlines()
        # check if we have 26 lines
        if len(txtLines) != 26:
            return None
        # get the day info object
        dayInfo = RawMeterCumData.parse(txtLines[0])
        dateObj = dayInfo.data_time
        meterId = dayInfo.meter_id
        blksInfo = []
        for lineIter in range(1,25):
            blksInfo = blksInfo + RawMeterData.parse(dateObj, meterId, txtLines[lineIter])
        return dict(cumData=dayInfo, blksData=blksInfo)