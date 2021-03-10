# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:41:44 2021

@author: svreugdenhil
"""
import math

reaction_vol = 25
DNA_vol = 1
disp_vol = reaction_vol - DNA_vol
print(disp_vol)
asp_vol = 200
max_dispenses = range(math.floor(asp_vol/disp_vol))
print(max_dispenses)

destination_row = "A"
destination_column = 1
destination_well = destination_row + str(destination_column)
print(destination_well)

