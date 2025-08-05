# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
simulate = False
#### Import opentrons protocol API v2
from opentrons import protocol_api
#### Import math 
import math ## To do some calculations
#### For simulating in the app, set pathway to modules
import sys
sys.path.append("O:/")
#### For playing sounds
import subprocess

#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Bead Clean Up V1.0',
            'description': 'Performing a Magnetic Bead Clean-Up'
            }
requirements = {'apiLevel': '2.20', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Samples
    parameters.add_int(variable_name="number_of_samples",
                       display_name="number of samples",
                       description="How many samples need to be cleaned up?",
                       default=8,
                       minimum=0,
                       maximum=96,
                       unit="samples")
    
    parameters.add_float(variable_name="sample_volume",
                       display_name="sample volume",
                       description="How much sample volume do you have?",
                       default=50.0,
                       minimum=0.0,
                       maximum=50.0,
                       unit="µL")
    #### Beads
    parameters.add_float(variable_name="sample_to_bead_ratio",
                       display_name="sample to bead ratio",
                       description="sample:beads (1:ratio)",
                       default=1.0,
                       minimum=0.0,
                       maximum=2.0,
                       unit="s:b")
    #### Elution
    parameters.add_float(variable_name="elution_volume",
                       display_name="elution volume",
                       description="How much volume do you want to elute in?",
                       default=50.0,
                       minimum=35.0,
                       maximum=100.0,
                       unit="µL")
      
def run(protocol: protocol_api.ProtocolContext):
    plankton = protocol.params
# =============================================================================    
    
## CONVERTING VARIABLES========================================================
## ============================================================================   
    #### Solutions
    bead_volume = plankton.sample_volume * plankton.sample_to_bead_ratio
    wash_volume = (plankton.sample_volume + bead_volume)*1.1
    number_of_sample_columns = math.ceil(plankton.number_of_samples / 8)
# =============================================================================  

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### PIPETTE TIPS
    tip_racks_p300, P300 = LW.number_of_tipracks('A1', 8 + (plankton.number_of_samples * 3))
    
    tips_300_sample = LW.loading_tips(simulate = simulate,
                                      tip_type = 'tipone_300uL',
                                      amount = 1,
                                      deck_positions = [9],
                                      protocol = protocol)
    tips_300_reagent = LW.loading_tips(simulate = simulate,
                                       tip_type = 'tipone_300uL',
                                       amount = 1,
                                       deck_positions = [6],
                                       protocol = protocol)
    #### PIPETTES       
    p300_right = protocol.load_instrument('p300_multi_gen2',
                                          'right',
                                          tip_racks=tips_300_sample)
    p300_left = protocol.load_instrument('p300_multi_gen2',
                                         'left',
                                         tip_racks=tips_300_reagent)
    

    #### HARDWARE MODULES
    mag_mod = protocol.load_module(module_name="magnetic module gen2", 
                                   location="7")
    temp_mod = protocol.load_module(module_name="temperature module gen2", 
                                   location="10")
    ### Loading adapter on temparature module
    temp_adapter = temp_mod.load_adapter("opentrons_96_well_aluminum_block")
    ## Loading plate on hardware modules
    mag_plate = mag_mod.load_labware("biorad_96_wellplate_200ul_pcr")
    temp_plate = temp_adapter.load_labware("biorad_96_wellplate_200ul_pcr")
    
    #### LABWARE
    ## RESERVOIR
    ethanol_reservoir = LW.loading_tube_racks(simulate = False,
                                              tube_type = 'tipone_box_250ml_reservoir',
                                              reagent_type = 'water',
                                              amount = 1,
                                              deck_positions = [1],
                                              protocol = protocol)   
    liquid_waste = LW.loading_tube_racks(simulate = False,
                                         tube_type = 'tipone_box_250ml_reservoir',
                                         reagent_type = 'water',
                                         amount = 1,
                                         deck_positions = [4],
                                         protocol = protocol)
    
    ## SAMPLES
    sample_plate = LW.loading_tube_racks(simulate = simulate,
                                      tube_type = 'plate_96_NIOZholder',
                                      reagent_type = 'samples',
                                      amount = 1,
                                      deck_positions = [11],
                                      protocol = protocol)
    
# =============================================================================

# LIGHTS ON====================================================================
# =============================================================================
    protocol.set_rail_lights(True)
# =============================================================================

# THE ACTUAL PIPETTING=========================================================
# ============================================================================= 
    protocol.pause(msg = f"Put a plate filled with {bead_volume}µL of magnetic beads per well on the temperature module.")
    
    # Heat up to 37°C    
    temp_mod.set_temperature(celsius=37)
    
    #### Add samples to beads
    # Loop through columns of plate/tip_rack
    for i in range(number_of_sample_columns): 
        column = "A" + str(i+1)    
        # Pick up row of tips
        p300_right.pick_up_tip(tips_300_sample[0][column])
        
        # Take sample from sample plate
        p300_right.aspirate(plankton.sample_volume, sample_plate[0][column])
        # Dispense in plate with beads on temperature module
        p300_right.dispense(plankton.sample_volume, temp_plate[column])
        
        # Mix by pipetting up and down
        p300_right.mix(repetitions=3, volume=100, rate=2.0) # 2x default flow rate
        # Mix by adding bubbles
        p300_right.blow_out(temp_plate[column].bottom())
        # Mix by pipetting up and down
        p300_right.mix(repetitions=3, volume=100, rate=2.0) # 2x default flow rate
        # Mix by adding bubbles
        p300_right.blow_out(temp_plate[column].bottom())
        # Mix by pipetting up and down
        p300_right.mix(repetitions=3, volume=100, rate=2.0) # 2x default flow rate
        
        # Return tips to tip rack for later use
        p300_right.return_tip()
        
        
    
    # Turn off heat block
    temp_mod.deactivate()    
        
        
    
    # protocol.delay(minutes = 20, msg = "20min incibation of sample with beads")
    
# =============================================================================

# LIGHTS OFF===================================================================
# =============================================================================
    protocol.set_rail_lights(False)
# =============================================================================
    