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

import subprocess

# def run_quiet_process(command): 
#     subprocess.check_output('{} &> /dev/null'.format(command), shell=True) 
# def test_speaker(AUDIO_FILE_PATH): 
#     print('Speaker') 
#     print('Next\t--> CTRL-C')
#     try:
#         run_quiet_process('mpg123 {}'.format(AUDIO_FILE_PATH))
#     except KeyboardInterrupt:
#         pass
#         print()
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
                       minimum=50.0,
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
# =============================================================================  

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### PIPETTE TIPS
    tip_racks_p300, P300 = LW.number_of_tipracks('A1', 8 + (plankton.number_of_samples * 5))
    
    tips_300 = LW.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               amount = tip_racks_p300,
                               deck_positions = [11,8,9,5,6],
                               protocol = protocol)   
    #### PIPETTES       
    p300_right = protocol.load_instrument('p300_multi_gen2',
                                          'right',
                                          tip_racks=tips_300)
    p300_left = protocol.load_instrument('p300_multi_gen2',
                                         'left',
                                         tip_racks=tips_300)
    

    #### HARDWARE MODULES
    mag_mod = protocol.load_module(module_name="magnetic module gen2", 
                                   location="7")
    temp_mod = protocol.load_module(module_name="temperature module gen2", 
                                   location="10")
    ### Loading adapter on temparature module
    temp_adapter = temp_mod.load_adapter("opentrons_96_well_aluminum_block")
    ## Loading plate on hardware modules
    magnetic_plate = mag_mod.load_labware("biorad_96_wellplate_200ul_pcr")
    temperature_plate = temp_adapter.load_labware("biorad_96_wellplate_200ul_pcr")
    
    #### LABWARE
    ## RESERVOIR
    ethanol_reservoir = LW.loading_tube_racks(simulate = False,
                                              tube_type = 'tipone_box_250ml_reservoir',
                                              reagent_type = 'water',
                                              amount = 1,
                                              deck_positions = [1],
                                              protocol = protocol)
    water_reservoir = LW.loading_tube_racks(simulate = False,
                                              tube_type = 'tipone_box_250ml_reservoir',
                                              reagent_type = 'water',
                                              amount = 1,
                                              deck_positions = [2],
                                              protocol = protocol)    
    liquid_waste = LW.loading_tube_racks(simulate = False,
                                         tube_type = 'tipone_box_250ml_reservoir',
                                         reagent_type = 'water',
                                         amount = 1,
                                         deck_positions = [4],
                                         protocol = protocol)
    
# =============================================================================

# LIGHTS ON====================================================================
# =============================================================================
    protocol.set_rail_lights(True)
# =============================================================================

# THE ACTUAL PIPETTING=========================================================
# =============================================================================
    if not protocol.is_simulating():
        subprocess.call('mpg123 /data/user_storage/audio/meme-okay-lets-go.mp3', shell=True)
    p300_left.pick_up_tip()
    p300_left.return_tip()
    
    

    

    # heat block at 37°C    
    # temp_mod.set_temperature(celsius=37)
    # protocol.delay(minutes = 20, msg = "20min incibation of sample with beads")
    
# =============================================================================

# LIGHTS OFF===================================================================
# =============================================================================
    protocol.set_rail_lights(False)
# =============================================================================
    