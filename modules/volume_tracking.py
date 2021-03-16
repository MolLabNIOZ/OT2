# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 210312
# Description: Module for volume tracking in different liquid containers
# =============================================================================

##### Import statements
import math
  ## Import math module to allow using π in calculations                    ##

##### Define function
def volume_tracking(container, current_vol, aspiration_vol):
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
    
    This module introduces calculations for liquid levels in conically shaped
    tubes and allows for tracking the height of the liquid in a container 
    during a protocol.
    
    Input for this function is:
        container =type of container. For now the options are 'tube_1.5mL' and
        'tube_5mL'.
        current_vol = current volume during the run. At the start of the
        protocol this should be set at the start_vol of the protocol.
        aspiration_vol = the volume that will be aspirated in the tracked steps
    
    Output of this function is:
        current_height = the height of the current liquid level in mm from the 
        bottom of the container.
        current_vol = the volume of liquid left in the container. After calling
        the volume_tracking function, make sure to update the current_vol 
        variable in your main protocol with the outcome of this function.
        delta_height = The height difference in mm of the liquid inside the 
        container between before and after aspiration. Delta_height is returned 
        so that in the main protocol a safety-step can be implemented:
        (if current_height - delta_height <= 1: some kind of error handling)
    """

    ##### Defining container dimensions
    ## Depending on the type of container, these are the dimensions         ##
    if container == 'tube_5mL':
        diameter_top = 13.3         #diameter of the top of the tube in mm
        diameter_tip = 3.3          #diameter of the tip of the tube in mm
        height_conical_tip = 55.4 - 2.2 - 34.12 #tube - straight part - rim
    elif container == 'tube_1.5mL':
        diameter_top = 8.7       #diameter of the top of the tube in mm
        diameter_tip = 3.6   #diamerer of the tip of the tube in mm
        height_conical_tip = 37.8 - 20 #tube - straight part
    ## From the following labware we do not have the dimensions yet         ##
    # elif container == 'tube_2mL':
    #     diameter_top =       #diameter of the top of the tube in mm
    #     diameter_tip =       #diameter of the tip of the tube in mm
    #     height_conical_tip = #tube - straight part - rim    
    # elif container == 'tube_15mL':
    #     diameter_top =       #diameter of the top of the tube in mm
    #     diameter_tip =       #diameter of the tip of the tube in mm
    #     height_conical_tip = #tube - straight part - rim
    # elif container == 'tube_50mL':
    #     diameter_top =       #diameter of the top of the tube in mm
    #     diameter_tip =       #diameter of the tip of the tube in mm
    #     height_conical_tip = #tube - straight part - rim

    ##### basic volume calculations for cylinder and cone shape
    ## volume of a cylinder is calculated as follows:                       ##
    ## v = π*r²*h  -->  h = v/(π*r²)                                        ##
    ## volume of a truncated cone is calculated as follows:                 ##
    ## v = (1/3)*π*h*(r²+r*R+R²)  -->  h = v / ((1/3)*π*(r²+r*R+R²))        ##
    ## For these calculations we need the radius of the top and tip of the  ##
    ## container. Also we need to know how much volume fills up the conical ##
    ## tip of the container. Above this volume the delta_height is based on ##
    ## a cylindrical shape, below this volume the delta_height is based on  ##
    ## a truncated cone shape.                                              ##
    radius_top = diameter_top / 2         #radius of the top of the tube in mm
    radius_tip = diameter_tip / 2         #radius of the tip of the tube in mm
    vol_conical_tip = ((1/3) * math.pi * height_conical_tip *
                   (radius_tip**2 + radius_tip*radius_top + radius_top**2))
    ## How much volume fills up the conical tip: v = (1/3)*π*h*(r²+r*R+R²)  ##

    ## If liquid level is below vol_conical_tip the delta_height is based on##
    ## a truncated cone shape (h = v / ((1/3)*π*(r²+r*R+R²)))
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
    ## If liquid level is above vol_conical_tip the delta_height is based on##
    ## a cylindrical shape (h = v/(π*r²), v = (total_vol - vol_conical_tip) ##
    else:
        cylinder_vol = current_vol - vol_conical_tip    # vol in straight part
        current_height = (
            height_conical_tip +        # current_height = height conical part 
            (cylinder_vol /             # + height cylindrical part
            (math.pi*((radius_top)**2)))
            ) 
        delta_height =  (
            aspiration_vol /
            (math.pi*((radius_top)**2))
            )
    
    ##### Update current_height and current_volume
    current_height = current_height - delta_height
    current_vol = current_vol - aspiration_vol
    ## The current_height (after aspiration) must be updated before the     ##
    ## actual aspiration, because during aspiration the liquid will reach   ## 
    ## that level.                                                          ##
    
    return current_height, current_vol, delta_height