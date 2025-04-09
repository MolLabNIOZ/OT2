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
sys.path.append("/mnt/c/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules_V1_2 as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# TEMPLATE DATA================================================================
# This region contains template data that will be replaced by the TapeStation 
# calculating protocol
# =============================================================================
DNA_µL_list = <DNA_volumes>
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {
            'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Equimolar pooling protocol for <NIOZ_NUMBER> V1.0',
            'description': 'Pools your sample equimolar after running the tapestation calculation protocol and sample diluting protocol.'
            }
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    #### Bullsh*t
    parameters.add_str(variable_name="Who_is_your_favourite_robot",    
                       display_name="Who is your favourite robot",
                       choices=[
                           {"display_name": "WALL-E", "value": "WALL-E"},
                           {"display_name": "EVE", "value": "EVE"},
                           {"display_name": "MO", "value": "MO"},
                           ],
                       default="MO")
    
    #### Starting tips
    # P20
    parameters.add_str(variable_name="starting_tip_p20_row",    
                       display_name="starting tip p20 row",
                       choices=[
                           {"display_name": "A", "value": "A"},
                           {"display_name": "B", "value": "B"},
                           {"display_name": "C", "value": "C"},
                           {"display_name": "D", "value": "D"},
                           {"display_name": "E", "value": "E"},
                           {"display_name": "F", "value": "this_is_not_false"},
                           {"display_name": "G", "value": "G"},
                           {"display_name": "H", "value": "H"}
                           ],
                       default="H")
    parameters.add_int(variable_name="starting_tip_p20_column",    
                       display_name="starting tip p20 column",
                       choices=[
                           {"display_name": "1", "value": 1},
                           {"display_name": "2", "value": 2},
                           {"display_name": "3", "value": 3},
                           {"display_name": "4", "value": 4},
                           {"display_name": "5", "value": 5},
                           {"display_name": "6", "value": 6},
                           {"display_name": "7", "value": 7},
                           {"display_name": "8", "value": 8},
                           {"display_name": "9", "value": 9},
                           {"display_name": "10", "value": 10},
                           {"display_name": "11", "value": 11},
                           {"display_name": "12", "value": 12}
                           ],
                       default=12)
    
    #### Starting tips
    # P300
    parameters.add_str(variable_name="starting_tip_p300_row",    
                       display_name="starting tip p300 row",
                       choices=[
                           {"display_name": "A", "value": "A"},
                           {"display_name": "B", "value": "B"},
                           {"display_name": "C", "value": "C"},
                           {"display_name": "D", "value": "D"},
                           {"display_name": "E", "value": "E"},
                           {"display_name": "F", "value": "this_is_not_false"},
                           {"display_name": "G", "value": "G"},
                           {"display_name": "H", "value": "H"}
                           ],
                       default="A")
    parameters.add_int(variable_name="starting_tip_p300_column",    
                       display_name="starting tip p300 column",
                       choices=[
                           {"display_name": "1", "value": 1},
                           {"display_name": "2", "value": 2},
                           {"display_name": "3", "value": 3},
                           {"display_name": "4", "value": 4},
                           {"display_name": "5", "value": 5},
                           {"display_name": "6", "value": 6},
                           {"display_name": "7", "value": 7},
                           {"display_name": "8", "value": 8},
                           {"display_name": "9", "value": 9},
                           {"display_name": "10", "value": 10},
                           {"display_name": "11", "value": 11},
                           {"display_name": "12", "value": 12}
                           ],
                       default=1)
    
    #### Lights/Pause
    parameters.add_bool(variable_name="lights_on",
                        display_name="lights on",
                        description="Do you want the lights turned ON?",
                        default=True)

def run(protocol: protocol_api.ProtocolContext):
    # Sets p as variable for protocol.params, this will make it all shorter
    plankton = protocol.params 
# =============================================================================

# PARAMETER VARIABLES==========================================================
# =============================================================================
    #### Starting tips
    if plankton.starting_tip_p20_row == 'this_is_not_false':
        starting_tip_p20_row = 'F'
    else:
        starting_tip_p20_row = plankton.starting_tip_p20_row
    if plankton.starting_tip_p300_row == 'this_is_not_false':
        starting_tip_p300_row = 'F'
    else:
        starting_tip_p300_row = plankton.starting_tip_p300_row
    
    # Combining the row-variable with the column-variable to create starting tip
    starting_tip_p20 = starting_tip_p20_row + str(plankton.starting_tip_p20_column)
    starting_tip_p300 = starting_tip_p300_row + str(plankton.starting_tip_p300_column)
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
    #### Calculate the total pool volume
    total_pool_volume = sum(DNA_µL_list)
    
    #### calculate total_pool_volume + buffer to add for clean-up 
    bead_volume = total_pool_volume
    total_cleanup_volume = total_pool_volume + bead_volume
    
    # Determine what tube type you need to pool everything
    pool_tube_type, number_of_tubes, max_volume = LW.which_tube_type(total_volume = total_cleanup_volume,
                                                                     tube_type = False)
    
    # For very large quantities, determine volume to pool per tube
    pool_volume_per_tube = total_cleanup_volume / number_of_tubes / 2
    
    #### Calculates how many tips are needed for pipetting all the DNA volumes
    p20_tips_needed, p300_tips_needed = LW.amount_of_tips(volumes = DNA_µL_list,
                                                          number_of_transfers = False,
                                                          tip_change = 1,
                                                          max_p20_volume = 15)
    
    # Calculates how many pipette boxes you need by using the function 'number_of_tipracks'
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip = starting_tip_p20,
                                                tips_needed = p20_tips_needed)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip = starting_tip_p300,
                                                 tips_needed = p300_tips_needed)
# =============================================================================
## LIGHTS & COMMENT------------------------------------------------------------
    protocol.set_rail_lights(plankton.lights_on)
    protocol.comment(f"You need {math.ceil(bead_volume/number_of_tubes)} μL of bead solution in {number_of_tubes} {pool_tube_type}")
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    # Loading p20 tips
    tips_20 = LW.loading_tips(simulate = simulate, 
                              tip_type = 'tipone_20uL', 
                              amount = tip_racks_p20, 
                              deck_positions = [7,10,11,8], 
                              protocol = protocol)
    
    # Loading p300 tips
    tips_300 = LW.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               amount = tip_racks_p300,
                               deck_positions = [8,11,10,7],
                               protocol = protocol)
    
    #### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20 = P20, 
                                    tips_20 = tips_20,
                                    starting_tip_p20 = starting_tip_p20,
                                    P300 = P300, 
                                    tips_300 = tips_300,
                                    starting_tip_p300 = starting_tip_p300,
                                    protocol = protocol)
    
    #### Loading labware
    # Loading source plate
    source_plate = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = 'plate_96_NIOZholder',
                                         reagent_type = 'source_plate',
                                         amount = 1,
                                         deck_positions = [1],
                                         protocol = protocol)
    
    # Spefifying location of the samples
    source_wells = LW.tube_locations(source_plate,
                                     False,
                                     False,
                                     len(DNA_µL_list),
                                     'samples',
                                     10,
                                     protocol)
    
    # Loading destination tube rack
    destination_rack = LW.loading_tube_racks (simulate = simulate, 
                                              tube_type = pool_tube_type, 
                                              reagent_type = 'pool_tube', 
                                              amount = 1, 
                                              deck_positions = [2], 
                                              protocol = protocol)
    
    # Spefifying location of the destination tube
    destination_tube = LW.tube_locations(source_racks = destination_rack,
                                         specific_columns = False,
                                         skip_wells = False,
                                         number_of_tubes = number_of_tubes,
                                         reagent_type = 'PB-buffer',
                                         volume = bead_volume/number_of_tubes/number_of_tubes,
                                         protocol = protocol)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Settings for transfering the sample volumes in the destination plate
    PM.pooling_varying_volumes(source_wells = source_wells,
                               pool_volumes = DNA_µL_list,
                               pool_tube = destination_tube,
                               pool_tube_type = pool_tube_type,
                               start_volume = bead_volume,
                               pool_volume_per_tube = pool_volume_per_tube,
                               airgap = True,
                               mix = True,
                               p20 = p20,
                               p300 = p300,
                               protocol = protocol)
## ============================================================================    
    
# TURN RAIL LIGHT OFF==========================================================
# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================
                        