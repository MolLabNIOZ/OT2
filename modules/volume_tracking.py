# SV & MB 210315
# Module for tracking volume in different liquid containers
import math

def volume_tracking(container, current_vol, aspiration_vol):
    """A function to make volume tracking possible for of conical tubes"""
    
    # Depending on kind of tube, define the dimensions
    if container == 'tube_5mL':
        diameter_top = 13.3         #diameter of the top of the tube in mm
        diameter_tip = 3.3          #diamerer of the tip of the tube in mm
        height_conical_tip = 55.4 - 2.2 - 34.12 #tube - straight part - rim
    elif container == 'tube_1.5mL':
        diameter_top = 8.7       #diameter of the top of the tube in mm
        diameter_tip = 3.6   #diamerer of the tip of the tube in mm
        height_conical_tip = 37.8 - 20 #tube - straight part
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

    ## set parameters based on tube dimensions
    radius_top = diameter_top / 2
    radius_tip = diameter_tip / 2
    vol_conical_tip = ((1/3) * math.pi * height_conical_tip *
                   (radius_tip**2 + radius_tip*radius_top + radius_top**2))
    
    # if liquid level is in the conical part of tube
    # use calculations for conical shapes (h = v / (1/3*pi*(r_tip**2)+(r_tip+r_top)+(r_top**2)))
    if current_vol <= vol_conical_tip: 
        current_height = (
            current_vol / 
            ((1/3) * math.pi * 
            (radius_tip**2 + radius_tip*radius_top + radius_top**2))
            )       
        delta_height = (
            aspiration_vol /
            ((1/3) * math.pi * 
            (radius_tip**2 + radius_tip*radius_top + radius_top**2))
            )
    # if liquid level is in straight part of tube
    # use calculations for cylinder (h = total_vol - vol_in_con_part / (pi*r**2))
    else:
        cylinder_vol = current_vol - vol_conical_tip
        current_height = (
            height_conical_tip + 
            (cylinder_vol / 
            (math.pi*((radius_top)**2)))
            ) 
        delta_height =  (
            aspiration_vol /
            (math.pi*((radius_top)**2))
            )
    # after aspiration, update the current height and volume
    current_height = current_height - delta_height #calculate new hight after pipetting step
    current_vol = current_vol - aspiration_vol
    return current_height, current_vol, delta_height
    
# current_height, current_vol = volume_tracking('tube_5mL', 2500, 24)

# print (current_height)
# print (current_vol)




