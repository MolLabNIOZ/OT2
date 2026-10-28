#### Import opentrons protocol API v2
from opentrons import protocol_api
# For single tip pickup
from opentrons.protocol_api import SINGLE, ALL
#### For simulating in the app, set pathway to modules
import sys
sys.path.append("O:/")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'PR-T test protocol multi',
            'description': ''
            }
requirements = {'apiLevel': '2.20', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):    
    #### p300_left TIPS
    opentrons_tips_300 = LW.loading_tips(simulate = False,
                               tip_type = 'opentrons_200uL',
                               amount = 1,
                               deck_positions = [8],
                               protocol = protocol)
    tipone_tips_300 = LW.loading_tips(simulate = False,
                                      tip_type = 'tipone_300uL',
                                      amount = 1,
                                      deck_positions = [6],
                                      protocol = protocol)
    
    
    #### p300_leftS       
    p300_left = protocol.load_instrument('p300_multi_gen2',
                                         'left',
                                         tip_racks=tipone_tips_300)
    p300_right = protocol.load_instrument('p300_multi_gen2',
                                          'right',
                                          tip_racks=opentrons_tips_300)
    
    #### HARDWARE MODULES
    mag_mod = protocol.load_module(module_name="magnetic module gen2", 
                                   location="4")
    temp_mod = protocol.load_module(module_name="temperature module gen2", 
                                   location="7")
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
                                              deck_positions = [2],
                                              protocol = protocol)
    liquid_waste = LW.loading_tube_racks(simulate = False,
                                         tube_type = 'tipone_box_250ml_reservoir',
                                         reagent_type = 'water',
                                         amount = 1,
                                         deck_positions = [3],
                                         protocol = protocol)
    
# =============================================================================

# LIGHTS ON====================================================================
# =============================================================================
    protocol.set_rail_lights(True)
# =============================================================================

# THE ACTUAL PIPETTING=========================================================
# =============================================================================

    ### Multichannel filling plate
    p300_left.pick_up_tip()
    
    mag_mod.engage(height_from_base=8.6)
    protocol.delay(seconds = 0, minutes = 5, msg = "sample + beads")   
    for column in magnetic_plate.columns_by_name():
        p300_left.aspirate(volume=50, location=magnetic_plate.columns_by_name()[column][0])                                   
        p300_left.dispense(volume=50, location=liquid_waste[0].wells()[0])
        mag_mod.disengage()
    p300_left.return_tip()
    
   
    # #### Singlechannel filling a column
    # p300_right.configure_nozzle_layout(style=SINGLE, start="A1", tip_racks=opentrons_tips_300)    
    # for i, well in enumerate(temperature_plate.columns_by_name()['1']):
    #     temp = 22 + i
    #     p300_right.pick_up_tip()
    #     p300_right.aspirate(volume=20, location=reagent_reservoir[0].wells()[0])
    #     p300_right.dispense(volume=20, location=well)
    #     temp_mod.set_temperature(celsius=temp)
    #     p300_right.drop_tip()
    # temp_mod.deactivate()
        
# =============================================================================    

# LIGHTS OFF===================================================================
# =============================================================================
    protocol.set_rail_lights(False)
# =============================================================================   