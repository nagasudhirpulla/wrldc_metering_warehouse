# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 09:51:56 2019

@author: Nagasudhir
"""

from num_string_parser import NumericStringParser
nsp = NumericStringParser()
s = '+(KO-11)     +(KO-12)   +(KO-13)   '
newStr = s.replace('KO-11', '45').replace('KO-12', '84').replace('KO-13', '34')
nsp.eval(newStr)    