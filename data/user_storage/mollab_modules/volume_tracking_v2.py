"""
Module for volume tracking in different liquid containers
Treats the entire tube as a cylindrical shape. Works good for
volume tracking in 1.5mL, 5mL, 5mL screwcap, 15mL and 50mL tubes.
update: Now also for filling up a tube
Needs direction (filling or emptying) as input
"""

##### Import statements
import math
  ## Import math module to allow using π in calculations                    ##

def cal_start_height(container, start_vol):
    """Module to calculate the liquid height in a tube at the start"""
    ##### Defining container dimensions
    ## Depending on the type of container, these are the dimensions         ##
    if container == 'tube_1.5mL':
        diameter_top = 8.7          #diameter of the top of the tube in mm
        diameter_tip = 3.6          #diameter of the tip of the tube in mm
        height_conical_tip = 17.8   #tube - straight part
    elif container == 'tube_2mL':
        diameter_top = 9.85         #diameter of the top of the tube in mm
        diameter_tip = 2.4          #diameter of the tip of the tube in mm
        height_conical_tip = 6.8    #tube - straight part
    elif container == 'tube_5mL':
        diameter_top = 13           #diameter of the top of the tube in mm
        diameter_tip = 3.3          #diameter of the tip of the tube in mm
        height_conical_tip = 66.1 - 43.6 - 1.3 #tube - straight part - bottom wall
    elif container == 'tube_5mL_snap':
        diameter_top = 13.3         #diameter of the top of the tube in mm
        diameter_tip = 3.3          #diameter of the tip of the tube in mm
        height_conical_tip = 55.4 - 2.2 - 34.12 #tube - straight part - rim
    elif container == 'tube_15mL':
        diameter_top = 15.16        #diameter of the top of the tube in mm
        diameter_tip = 2.16         #diameter of the tip of the tube in mm
        height_conical_tip = 22.1   #tube - straight part
    elif container == 'tube_50mL':
        diameter_top = 27.48        #diameter of the top of the tube in mm
        diameter_tip = 4.7          #diameter of the tip of the tube in mm
        height_conical_tip = 15.3   #tube - straight part
        
    
    radius_top = diameter_top / 2         #radius of the top of the tube in mm
    radius_tip = diameter_tip / 2         #radius of the tip of the tube in mm
    vol_conical_tip = ((1/3) * math.pi * height_conical_tip *
                    ((radius_tip**2) + (radius_tip*radius_top) +
                     (radius_top**2)))
    ## How much volume fills up the conical tip: v = (1/3)*π*h*(r²+r*R+R²)  ##
    
    ##### Calculating start height
    cylinder_vol = start_vol - vol_conical_tip    # vol in straight part
    start_height = (
            height_conical_tip +        # current_height = height conical part 
            (cylinder_vol /             # + height cylindrical part
            (math.pi*((radius_top)**2)))
            )
    ## Initially start higher in a 15mL tube. Due to the shape of the tube, ##
    ## volume tracking doesn't work perfect when assuming that the entire   ##
    ## tube is cylindrical. This is partly solved by adding 7 mm to the     ##
    ## start_height.                                                        ##
    ## For 5mL screwcap tubes we substract 5 mm to solve a similar problem. ##
    if container == 'tube_15mL':
        start_height = start_height + 7
    if container == 'tube_5mL':
        start_height = start_height - 5
    
    return start_height


def volume_tracking(container, dispension_vol, current_height, direction):
    """
    At this moment the OT-2 doesn't have a volume tracking function.
    By default, aspiration occurs from the bottom of a container. When a
    container is filled with liquid, this can cause the pipette to be 
    submurged beyond the pipette tip, possibly damaging the pipette. 
    Furthermore, when a container is already full, it will overflow when the 
    pipette is reaching for the bottom. Also, when the pipette goes far into 
    the liquid, a lot of liquid will stick to the outside of the pipette tip.
    This will make pipetting less acurate and increases the risk of cross-
    contamination.
    
    This module introduces calculations for liquid levels in tubes
    and allows for tracking the height of the liquid in a container 
    during a protocol.
    
    Input for this function is:
        container = type of container. Several options are available:
            'tube_1.5mL'
            'tube_2mL'
            'tube_5mL'
            'tube_5mL_snap'
            'tube_15mL'
            'tube_50mL'
        current_vol = current volume during the run. At the start of the
        protocol this should be set at the start_vol of the protocol.
        aspiration_vol = the volume that will be aspirated in the tracked steps
        direction = 'emptying' or 'filling'
    
    Output of this function is:
        current_height = the height of the current liquid level in mm from the 
        bottom of the container.
        delta_height = The height difference in mm of the liquid inside the 
        container between before and after aspiration. Delta_height is returned 
        so that in the main protocol a safety-step can be implemented:
        (if current_height - delta_height <= 1: some kind of error handling)
        """

    ##### Defining container dimensions
    ## Depending on the type of container, these are the dimensions         ##
    if container == 'tube_1.5mL':
        diameter = 8.7          #diameter of the top of the tube in mm
    elif container == 'tube_2mL':
        diameter = 9.85         #diameter of the top of the tube in mm
    elif container == 'tube_5mL':
        diameter = 13           #diameter of the top of the tube in mm
    elif container == 'tube_5mL_snap':
        diameter = 13.3         #diameter of the top of the tube in mm
    elif container == 'tube_15mL':
        diameter = 15.16        #diameter of the top of the tube in mm
        height_conical_tip = 22.1   #tube - straight part
        offset_height = height_conical_tip + 18 
        ## offset_height = height from where to start using                 ##
        ## current_height - 1 so that the pipette tip stays submerged.      ##
    elif container == 'tube_50mL':
        diameter = 27.48        #diameter of the top of the tube in mm
    
    ## volume of a cylinder is calculated as follows:                       ##
    ## v = π*r²*h  -->  h = v/(π*r²)                                        ##
    
    radius = diameter / 2         #radius of the top of the tube in mm
    
    ##### Calculate delta height per dispensed volume
    delta_height =  (dispension_vol/(math.pi*((radius)**2)))

    ##### Update current_height 
    if direction == 'emptying': 
        current_height = current_height - delta_height
    elif direction == 'filling': 
        current_height = current_height + delta_height
    ## The current_height (after aspiration) must be updated before the     ##
    ## actual aspiration, because during aspiration the liquid will reach   ## 
    ## that level.

    ##### Tweaks                                                            ##
    if container == 'tube_15mL' and current_height < offset_height:
        current_height = current_height - 1
    ## Volume tracking when assuming the entire tube is cylindrical doesn't ##
    ## work very well with a 15 mL tube. Therefore, we need to adjust some  ##
    ## values so that we do the volume tracking as good as possible.        ##
    ## start_height is already adjusted so that we start a little heigher,  ##
    ## however at the offset_height the pipette didn't reach the liquid     ##
    ## anymore. So we lower the current_height with 1 so that the pipette   ##
    ## tip is always submerged and the entire tube is emptied.              ##
    pip_height = current_height - 2
    ## Make sure that the pipette tip is always submerged by                ##
    ## setting the current height 2 mm below its actual height              ##
    if container == 'tube_5mL':
        bottom_reached = (current_height - delta_height <= 6)
    else:
        bottom_reached = (current_height - delta_height <= 2)
    # not thoroughly tested for other tubes yet!!!
    
    return current_height, pip_height, bottom_reached

