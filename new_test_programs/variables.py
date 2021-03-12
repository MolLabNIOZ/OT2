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

<<<<<<< Updated upstream
delta_height = (math.pi*((13.3/2)**2))/188
print(height)

#%%
start_vol = 3000 #starting volume at the beginning of the protocol in ul
diameter = 13.3 #diameter of the top of the tube in mm
start_height = start_vol/(math.pi*((diameter/2)**2))
transfer_vol = 24
delta_height =  transfer_vol/(math.pi*((diameter/2)**2))
current_height = start_height
print(delta_height)


    
=======
radius_tip = 3.3/2
radius_top = 13.3/2
height_conical = 55.4 - 2.2 - 34.12
volume_conical = (1/3) * math.pi * height_conical * (radius_tip**2 + radius_tip*radius_top + radius_top**2)
>>>>>>> Stashed changes
