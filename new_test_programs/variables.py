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

delta_height = (math.pi*((13.3/2)**2))/188
print(delta_height)

#%%
start_vol = 3000 #starting volume at the beginning of the protocol in ul
diameter = 13.3 #diameter of the top of the tube in mm
start_height = start_vol/(math.pi*((diameter/2)**2))
transfer_vol = 24
delta_height =  transfer_vol/(math.pi*((diameter/2)**2))
current_height = start_height
current_volume = 2500
  
radius_tip = 3.3/2
radius_top = 13.3/2
height_conical_tip = 55.4 - 2.2 - 34.12
volume_conical_tip = (1/3) * math.pi * height_conical_tip * (radius_tip**2 + radius_tip*radius_top + radius_top**2)
height_conical = current_volume / ((1/3) * math.pi * (radius_tip**2 + radius_tip*radius_top + radius_top**2))

if current_volume > volume_conical_tip:
    extra_volume = current_volume - volume_conical_tip
    height = height_conical_tip + (extra_volume / (math.pi*((diameter/2)**2)))
    delta_height =  transfer_vol/(math.pi*((diameter/2)**2))
elif current_volume <= volume_conical_tip:
    height = current_volume / ((1/3) * math.pi * (radius_tip**2 + radius_tip*radius_top + radius_top**2))
    delta_height =  transfer_vol/((1/3) * math.pi * (radius_tip**2 + radius_tip*radius_top + radius_top**2))
    
#%%
container = 'tube_5mL'
start_volume = 3000
aspiration_volume = 24

# Depending on kind of tube, define the dimensions
if container == 'tube_5mL':
    diameter_top = 13.3         #diameter of the top of the tube in mm
    diameter_tip = 3.3          #diamerer of the tip of the tube in mm
    height_conical_tip = 55.4 - 2.2 - 34.12 #tube - straight part - rim
## other tube types
# elif container == 'tube_1.5mL':
#     diameter_top =       #diameter of the top of the tube in mm
#     diameter_tip =       #diamerer of the tip of the tube in mm
#     height_conical_tip = #tube - straight part - rim
# elif container == 'tube_2mL':
#     diameter_top =       #diameter of the top of the tube in mm
#     diameter_tip =       #diamerer of the tip of the tube in mm
#     height_conical_tip = #tube - straight part - rim    

# elif container == 'tube_15mL':
#     diameter_top =       #diameter of the top of the tube in mm
#     diameter_tip =       #diamerer of the tip of the tube in mm
#     height_conical_tip = #tube - straight part - rim
# elif container == 'tube_50mL':
#     diameter_top =       #diameter of the top of the tube in mm
#     diameter_tip =       #diamerer of the tip of the tube in mm
#     height_conical_tip = #tube - straight part - rim

# set parameters based on tube dimensions
radius_top = diameter_top / 2
radius_tip = diameter_tip / 2
vol_conical_tip = ((1/3) * math.pi * height_conical_tip *
               (radius_tip**2 + radius_tip*radius_top + radius_top**2))

# set variables that change during the run
current_volume = start_volume
    
if current_volume - aspiration_volume < 5: #make sure bottom is never reached
    protocol.home() 
    protocol.pause('Your mix is finished.')
    
else: 
    if current_volume <= vol_conical_tip: 
        current_height = (
            current_volume / 
            ((1/3) * math.pi * 
            (radius_tip**2 + radius_tip*radius_top + radius_top**2))
            )
        delta_height = (
            aspiration_volume /
            ((1/3) * math.pi * 
            (radius_tip**2 + radius_tip*radius_top + radius_top**2))
            )
       
    else:
        cylinder_volume = current_volume - vol_conical_tip
        current_height = (
            height_conical_tip + 
            (cylinder_volume / 
            (math.pi*((radius_top)**2))
            )
                          ) 
        delta_height =  (
            aspiration_volume /
            (math.pi*((radius_top)**2))
            )
    
    current_height = current_height - delta_height #calculate new hight after pipetting step
     
print (current_height)
print (delta_height)

#%%
current_height = 5
height_conical_tip = 20
radius_top = 10
radius_tip = 2

radius_top = radius_top = (
            (radius_tip*(height_conical_tip - current_height))+
            (radius_top*(current_height-0)))/height_conical_tip
<<<<<<< HEAD

#%%

Rtop = 10      #Radius of the top of the tube
r = 2          #Radius of the bottom of the tube
t_h = 20       #Height of the tube
c_h = 20       #Current height

# calcultating the radius top at a certain height:
R = ((r*(t_h - c_h))+(Rtop*c_h))/t_h
=======
>>>>>>> parent of b21e09a (Restored old volume tracking module)

for c_h in range(21):
    R = ((r*(t_h - c_h))+(Rtop*c_h))/t_h
    print(str(c_h) + "\t" + str(R))