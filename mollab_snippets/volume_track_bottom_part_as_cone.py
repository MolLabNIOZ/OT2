# =============================================================================
# This is the volume tracking function that we tried to use at first.
# It keeps in mind that the tip of the tube is conically shaped and changes
# the height calculation when it reaches this part.
# However, when using this formula for SOME reason the pipette goes down
# faster than the liquid does, causing the pipette to dip to deep.
# When treating the entire tube as a cylinder, it works better...
# We might need to check the formula itself at some point, maybe the 
# calculations are wrong?
# =============================================================================

def volume_tracking(container, dispension_vol, current_height):
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
    ## How much volume fills up the conical tip: v = (1/3)*π*h*(r²+r*R+R²)  ##

    ## If liquid level is below vol_conical_tip the delta_height is based on##
    ## a truncated cone shape (h = v / ((1/3)*π*(r²+r*R+R²)))               ##
    if current_height <= height_conical_tip:
        current_radius_top = (
            (radius_tip*(height_conical_tip - current_height))+
            (radius_top*current_height))/height_conical_tip
          ## lineair interpolation formula derived from                     ##
          ## https://en.wikipedia.org/wiki/Linear_interpolation             ##
          ## r = radius (r is tip R is top)                                 ##
          ## h = height                                                     ##
          ## current_r = (r(conical_h - current_h)+ (R*current_h))/conical_h##
          ## The radius_top decreases with each pipetting step, so we       ##
          ## calculate a new radius_top for each step.                      ##
        delta_height = (
            dispension_vol /
            ((1/3) * math.pi * 
            ((radius_tip**2) + (radius_tip*current_radius_top) + 
              (current_radius_top**2)))
            )
    ## If liquid level is above vol_conical_tip the delta_height is based on##
    ## a cylindrical shape (h = v/(π*r²), v = (total_vol - vol_conical_tip) ##
    else:
        delta_height =  (dispension_vol/(math.pi*((radius_top)**2)))
    
    ##### Update current_height and current_volume
    current_height = current_height - delta_height
    ## The current_height (after aspiration) must be updated before the     ##
    ## actual aspiration, because during aspiration the liquid will reach   ## 
    ## that level.                                                          ##
    
    return current_height, delta_height
# =============================================================================