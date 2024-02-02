"""
version: Jan_2024
"""

def cal_start_height(tube_type, start_volume):
    """
    Module to calculate the liquid height in a tube at the start of the run
    Parameters
    ----------
    tube_type : brand / size
        '1.5mL_tubes' / '5mL_screwcap_tubes' / '5mL_snapcap_tubes' / '15mL_tubes' / '50mL_tubes'
    start_vol : int
        exact volume in µL that is present in the reagent tube(s) at the start

    Returns
    -------
    start_height : float
        height in mm from the bottom of the tube

    """
    #### Import math module to allow using π in calculations
    import math 
    
    #### Defining tube_type dimensions, based on labware blueprints
    tube_dimensions = {
    '1.5mL_tubes': {
        'diameter_top': 8.7,
        'diameter_tip': 3.6,
        'height_conical_tip': 17.8},
    '5mL_screwcap_tubes': {
        'diameter_top': 13,
        'diameter_tip': 3.3,
        'height_conical_tip': 66.1 - 43.6 - 1.3},
    '5mL_snapcap_tubes': {
        'diameter_top': 13.3,
        'diameter_tip': 3.3,
        'height_conical_tip': 55.4 - 2.2 - 34.12},
    '15mL_tubes': {
        'diameter_top': 15.16,
        'diameter_tip': 2.16,
        'height_conical_tip': 22.1},
    '50mL_tubes': {
        'diameter_top': 27.48,
        'diameter_tip': 4.7,
        'height_conical_tip': 15.3}} 
    
    #### Calculate radiuses (diameter / 2)
    radius_top = tube_dimensions[tube_type]['diameter_top']/ 2
    radius_tip = tube_dimensions[tube_type]['diameter_tip']/ 2
    
    #### Calculate the volume of the conical tip v = (1/3)*π*h*(r²+r*R+R²)
    vol_conical_tip = ((1/3)*math.pi*tube_dimensions[tube_type]['diameter_tip']*
                       ((radius_tip**2) + (radius_tip*radius_top) +
                        (radius_top**2)))

    #### Calculating start height
    cylinder_vol = start_volume - vol_conical_tip
    start_height = (tube_dimensions[tube_type]['diameter_tip'] +
                    (cylinder_vol / (math.pi*((radius_top)**2))))
        # start_height = height_conical_tip + height_cylindrical_part
    
    #### Some tweaks
    if tube_type == '15mL_tubes':
        start_height = start_height + 7
    if tube_type == '5mL_screwcap_tubes':
        start_height = start_height - 5
        ## Initially start higher in a 15mL tube. Due to the shape of the tube,
        ## volume tracking doesn't work perfect when assuming that the entire
        ## tube is cylindrical. This is partly solved by adding 7 mm to the
        ## start_height.
        ## For 5mL screwcap tubes we substract 5 mm to solve a similar problem.    
    
    return start_height  

def volume_tracking(tube_type, dispension_vol, current_height, direction):  
    """
    By default, aspiration occurs from the bottom of a tube.    
    This module introduces calculations for liquid levels in tubes
    and allows for tracking the height of the liquid in a tube 
    during a protocol.
    
    Parameters
    ----------
    tube_type : brand / size
        'tube_1.5mL' / 'tube_5mL' / 'tube_15mL' / 'tube_50mL'
    dispension_vol : int
        volume in µL that you want to dispense
    current_height : float
        height in the tube (in mm) of the reagent at this moment in the run
    direction : string
        is the tube being emptied or filled? 'emptying' / 'filling'

    Returns
    -------
    current_height : float
        height in mm of the current volume from the bottom of the tube
    pip_height : float
        current_height - 5, to make sure the tip is submerged
    bottom_reached : boolean True or False
        Safety measure, indicates that the bottom of the tube is reached
    """
    #### Import math module to allow using π in calculations
    import math
    
    #### Defining tube_type dimensions, based on labware blueprints
    tube_diameters = {
    '1.5mL_tubes': 8.7,
    '5mL_screwcap_tubes': 13,
    '5mL_snapcap_tubes': 13.3,
    '15mL_tubes': 15.16,
    '50mL_tubes': 27.48}
 
    #### Calculate delta_height of the specified volume      
    radius = tube_diameters[tube_type] / 2
    delta_height =  (dispension_vol/(math.pi*((radius)**2))) #h = v/(π*r²)

    #### Update current_height 
    if direction == 'emptying': 
        current_height = current_height - delta_height
    elif direction == 'filling': 
        current_height = current_height + delta_height
        ## The current_height (after aspiration) must be updated before the
        ## actual aspiration, because during aspiration the liquid will reach 
        ## that level.

    #### Tweaks
    if tube_type == '15mL_tubes':
        height_conical_tip = 22.1   #tube - straight part
        offset_height = height_conical_tip + 18 
        ## offset_height = height from where to start using
        ## current_height - 1 so that the pipette tip stays submerged.                                                            ##
        if current_height < offset_height:
            current_height = current_height - 1
    ## Volume tracking when assuming the entire tube is cylindrical doesn't
    ## work very well with a 15 mL tube. Therefore, we need to adjust some
    ## values so that we do the volume tracking as good as possible.       
    ## start_height is already adjusted so that we start a little heigher,
    ## however at the offset_height the pipette didn't reach the liquid     
    ## anymore. So we lower the current_height with 1 so that the pipette   
    ## tip is always submerged and the entire tube is emptied.              

    #### Determine the height at which to pipette
    pip_height = current_height - 5
    ## Make sure that the pipette tip is always submerged by       
    ## setting the current height 5 mm below the reagent surface   

    #### Determine whether the pipette is reaching the bottom of the tube
    bottom_reached = False
    if pip_height - delta_height <= 2:
            bottom_reached = True
    # not thoroughly tested yet for other tubes then tubes_5mL!!!
    
    return current_height, pip_height, bottom_reached