# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 11:45:02 2019

@author: Nagasudhir
"""

# derive intersection of 2 lists
def intersection(lst1, lst2): 
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3 