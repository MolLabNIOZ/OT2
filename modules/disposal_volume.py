# SV 210315 a module for calculating the volume that the pipette should 
# aspirate = dispense volume + dispense, keeping the maximum volumes of
# each pipette in mind. 

# import opentrons
# protocol = opentrons.execute.get_protocol_api('2.9')



def disposal_volume_p300_200(dispension_vol):
    """A function to calculate the volume to aspirate for the p300. 
    Aspiration volume = dispense volume + 2%, this volume should not 
    exceed the maximum aspiration volume of the pipette.""" 
    
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
    
    return aspiration_vol
    

def disposal_volume_p20(dispension_vol):
    """A function to calculate the volume to aspirate for the p20. 
    Aspiration volume = dispense volume + 2%, this volume should not 
    exceed the maximum aspiration volume of the pipette."""
    
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
    
    return aspiration_vol
