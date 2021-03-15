# SV 210315 a module for calculating the volume that the pipette should 
# aspirate = dispense volume + dispense, keeping the maximum volumes of
# each pipette in mind.


def disposal_volume_p300(dispension_vol):
    """A function to calculate the volume to aspirate for the p300. 
    Aspiration volume = dispense volume + 2%, this volume should not 
    exceed the maximum aspiration volume of the pipette.""" 
    
    max_vol_pipette = 200 + (200/100*2)
    
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
    
    if aspiration_vol <= max_vol_pipette:
        return aspiration_vol
    else: 
        print("WARNING: aspiration volume exceeds max volume of the pipette")
    

def disposal_volume_p20(dispension_vol):
    """A function to calculate the volume to aspirate for the p20. 
    Aspiration volume = dispense volume + 2%, this volume should not 
    exceed the maximum aspiration volume of the pipette."""
    
    max_vol_pipette = 20 + (20/100*2)
    
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
    
    if aspiration_vol <= max_vol_pipette:
        return aspiration_vol
    else:
        print("WARNING: aspiration volume exceeds max volume of the pipette")
