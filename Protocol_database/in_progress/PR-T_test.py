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
            'protocolName': 'PR-T test protocol single',
            'description': ''
            }
requirements = {'apiLevel': '2.20', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):    
    #### PIPETTE TIPS
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
    
    
    #### PIPETTES       
    p300 = protocol.load_instrument('p300_multi_gen2',
                                    'left',
                                    tip_racks=tipone_tips_300)
    
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
    reagent_reservoir = LW.loading_tube_racks(simulate = False,
                                              tube_type = 'tipone_box_250ml_reservoir',
                                              reagent_type = 'water',
                                              amount = 1,
                                              deck_positions = [2],
                                              protocol = protocol)
    
# =============================================================================

# LIGHTS ON====================================================================
# =============================================================================
    protocol.set_rail_lights(True)
# =============================================================================

# THE ACTUAL PIPETTING=========================================================
# =============================================================================
    #### Multichannel filling plate
    # p300.pick_up_tip()
    # for column in magnetic_plate.columns_by_name():
    #     p300.aspirate(volume=100, location=reagent_reservoir[0].wells()[0])
    #     p300.dispense(volume=100, location=magnetic_plate.columns_by_name()[column][0])
    # p300.return_tip()
    
    # p300.pick_up_tip()
    # p300.aspirate(volume=100, location=reagent_reservoir[0].wells()[0])
    # p300.dispense(volume=100, location=magnetic_plate.wells()[0])
    # p300.return_tip()
    
    #### Singlechannel filling a column
    p300.configure_nozzle_layout(style=SINGLE, start="A1", tip_racks=opentrons_tips_300)

    
    for well in temperature_plate.columns_by_name()['1']:
        p300.pick_up_tip()
        p300.aspirate(volume=100, location=reagent_reservoir[0].wells()[0])
        p300.dispense(volume=100, location=well)
        p300.drop_tip()
    
    
# =============================================================================    





# LIGHTS OFF===================================================================
# =============================================================================
    protocol.set_rail_lights(False)
# =============================================================================   