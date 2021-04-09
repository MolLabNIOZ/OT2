# =============================================================================
# Separate formulas for volume tracking
# =============================================================================

radius_top = diameter_top / 2       #radius of the top of the tube in mm

radius_top_c = diameter_top_c / 2   #radius conical part of the tube in mm

radius_tip = diameter_tip / 2       #radius of the tip of the tube in mm

vol_conical_tip = ((1/3) * math.pi * height_conical_tip *
                   (radius_tip**2 + radius_tip*radius_top_c + radius_top_c**2))
## How much volume fills up the conical tip: v = (1/3)*π*h*(r²+r*R+R²)      ##

cylinder_vol = start_vol - vol_conical_tip    #vol in cylinder part

start_height = (
        height_conical_tip +      
        (cylinder_vol /            
        (math.pi*((radius_top)**2)))
        )
#current_height = height conical part + height cylindrical part