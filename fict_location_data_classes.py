# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 10:18:31 2019

@author: Nagasudhir


Fict meter data has 25 lines (check 1)

first lines has the following data delimited by spaces
fict_location_id, fict_location_id, date (MM-dd-yy), ...
For Fict location energy file, the fisrt 2 segments are same (check 2)
AC-93 AC-93   08-09-19    11004.0518     2105.9      0.0

Remaining line has the following data delimited by spaces
hour_of_day00, blk1_active energy(Kilo Watt Hour), … till block 4
0200      122.771065        122.685020        120.562950        116.449539
"""
import datetime as dt


class FictLocationDayData:
    data_time = None
    location_id = None

    def __init__(self, data_time, location_id):
        self.location_id = location_id
        self.data_time = data_time

    @staticmethod
    def parse(txtLine):
        strs = txtLine.split()
        # check if we have at least 3 words
        if len(strs) <= 3:
            return None
        # check if 1st 2 segments are same
        if strs[0] != strs[1]:
            return None
        location_id = strs[0]
        data_time = dt.datetime.strptime(strs[2], '%d-%m-%y').date()
        meterHeader = FictLocationDayData(data_time, location_id)
        return meterHeader

    def dict(self):
        return self.__dict__


class FictLocationBlockData:
    data_time = None
    location_id = None
    mwh = None

    def __init__(self, data_time, location_id, mwh):
        self.data_time = data_time
        self.location_id = location_id
        self.mwh = mwh

    @staticmethod
    def parse(date_obj, location_id, txtLine):
        strs = txtLine.split()
        # check if we have 9 words
        if len(strs) != 5:
            return None

        hr = int(strs[0][:2])

        blkActEns = [strs[1], strs[2], strs[3], strs[4]]
        blkActEns = [float(f) for f in blkActEns]

        dataRes = []

        for blkNum in range(0, 4):
            data_time = dt.datetime(date_obj.year, date_obj.month,
                                    date_obj.day, hr, 0, 0) + dt.timedelta(minutes=15*blkNum)
            blkData = FictLocationBlockData(
                data_time, location_id, blkActEns[blkNum])
            dataRes.append(blkData)

        return dataRes

    def dict(self):
        return self.__dict__


class FictLocationDataParser:
    @staticmethod
    def ParseFictLocationData(txt):
        # print(txt)
        txtLines = txt.splitlines()
        # check if we have 25 lines
        if len(txtLines) < 25:
            return None
        # get the day info object
        dayInfo = FictLocationDayData.parse(txtLines[0])
        if dayInfo == None:
            return None
        dateObj = dayInfo.data_time
        locationId = dayInfo.location_id
        blksInfo = []
        for lineIter in range(1, 25):
            blksInfo = blksInfo + \
                FictLocationBlockData.parse(dateObj, locationId, txtLines[lineIter].replace(
                    'aa', '').replace('rr', '').replace('*', ''))
        return dict(cumData=dayInfo, blksData=blksInfo)
