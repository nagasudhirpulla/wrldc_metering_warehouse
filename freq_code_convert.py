# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 20:43:50 2019

@author: Nagasudhir

Avg Block Frequency = k1 + freq_code/k2
where 
(k1, k2) = (49, 50) for 0.02 Hz Resolution
(k1, k2) = (49.5, 100) for 0.01 Hz Resolution

"""

def freqCodeToFreq(freq_code, resol=0.02):
    (k1, k2) = (49, 50) if resol == 0.02 else (49.5, 100)
    freq = k1 + (freq_code/k2)
    return freq