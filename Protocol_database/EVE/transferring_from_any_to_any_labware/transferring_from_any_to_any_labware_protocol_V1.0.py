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
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Transferring from and to different tube types V1.0',
            'description': 'Transferring from any to any tube type.'
            }
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Samples
    parameters.add_int(variable_name="number_of_transfers",
                       display_name="How many samples do you have?",
                       description="Number of samples you want to transfer. Max is 96 samples.",
                       default=96,
                       minimum=0,
                       maximum=96,
                       unit="samples")
    
    #### Tube types
    parameters.add_str(variable_name="sample_tube_type",    
                       display_name="sample tube type",
                       choices=[
                           {"display_name": "PCR-strips", "value": "PCR_strips"},
                           {"display_name": "PCR-plate", "value": "skirted_plate_96"},
                           {"display_name": "1.5mL tubes", "value": "1.5mL_tubes"},
                           ],
                       default="1.5mL_tubes")
    parameters.add_str(variable_name="final_tube_type",    
                       display_name="final tube type",
                       choices=[
                           {"display_name": "PCR-strips", "value": "PCR_strips"},
                           {"display_name": "PCR-plate", "value": "skirted_plate_96"},
                           {"display_name": "1.5mL tubes", "value": "1.5mL_tubes"},
                           ],
                       default="skirted_plate_96")
    
    #### Transfer
    parameters.add_float(variable_name="transfer_volume",
                         display_name="transfer volume",
                         description="What volume would you like to transfer?",
                         default=25.0,
                         minimum=10.0,
                         maximum=1400.0,
                         unit="ul")
    
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
                       default="H")
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
                       default=12)
    
    #### Lights/Pause  
    parameters.add_bool(variable_name="lights_on",
                        display_name="lights on",
                        description="Do you want the lights turned ON?",
                        default=True)

def run(protocol: protocol_api.ProtocolContext):
    plankton = protocol.params
# =============================================================================

## CONVERTING VARIABLES========================================================
## ============================================================================
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

## CALCULATED VARIABLES========================================================
## ============================================================================
    #### Final and stock racks
    # Possible locations of strips in racks
    possible_strip_locations = {
        1:['6'],
        2:['3','9'],
        3:['2','7','11'],
        4:['2','5','8','11'],
        }     
    # Possible combinations for the different tube types
    tube_type_dict = {
        "PCR_strips" : (possible_strip_locations[math.ceil(plankton.number_of_transfers/8/3)], len(possible_strip_locations[math.ceil(plankton.number_of_transfers/8/3)])*8),
        "skirted_plate_96" : (False, 96),
        "1.5mL_tubes" : (False, 24),
        } 
    
    # Calculates number of stock racks
    stock_strip_columns = tube_type_dict[plankton.sample_tube_type][0]
    samples_per_rack = tube_type_dict[plankton.sample_tube_type][1]
    number_of_sample_racks = int(math.ceil((plankton.number_of_transfers / samples_per_rack)))
                                 
    # Calculates number of final racks
    final_strip_columns = tube_type_dict[plankton.final_tube_type][0]
    destinations_per_rack = tube_type_dict[plankton.final_tube_type][1]
    number_of_final_racks = int(math.ceil((plankton.number_of_transfers / destinations_per_rack)))


    #### Calculates the amount of tip racks needed and set pipette True or False
    tip_racks_p20, tip_racks_p300, P20, P300 = LW.number_of_tip_racks_2_0(volumes_aliquoting = 0,
                                                                          number_of_aliquotes = 0,
                                                                          volumes_transfering = plankton.transfer_volume,
                                                                          number_of_transfers = plankton.number_of_transfers,
                                                                          starting_tip_p20 = starting_tip_p20,
                                                                          starting_tip_p300 = starting_tip_p300)
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(plankton.lights_on)
## ============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_p20 = LW.loading_tips(simulate,
                               'tipone_20uL',
                               tip_racks_p20,
                               [3,6,9],
                               protocol)
    tips_p300 = LW.loading_tips(simulate,
                               'opentrons_200uL',
                               tip_racks_p300,
                               [9,6,3],
                               protocol)
    ## ========================================================================
    #### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20 = P20, 
                                    tips_20 = tips_p20,
                                    starting_tip_p20 = starting_tip_p20,
                                    P300 = P300, 
                                    tips_300 = tips_p300,
                                    starting_tip_p300 = starting_tip_p300,
                                    protocol = protocol)
    ## ========================================================================
    #### Stock racks
    # Loading stock racks
    stock_racks = LW.loading_tube_racks(simulate = simulate, 
                                        tube_type = plankton.sample_tube_type,  
                                        reagent_type = 'samples', 
                                        amount = number_of_sample_racks,
                                        deck_positions = [1,4,7,10], 
                                        protocol = protocol)
    # Loading stock tubes
    stock_tubes = LW.tube_locations(source_racks = stock_racks,
                                    specific_columns = stock_strip_columns,
                                    skip_wells = False,
                                    number_of_tubes = plankton.number_of_transfers,
                                    reagent_type = 'samples',
                                    volume = plankton.transfer_volume/plankton.number_of_transfers,
                                    protocol = protocol)
    ## ========================================================================
    #### Final tube racks
    # Loading final racks
    destination_racks = LW.loading_tube_racks(simulate = simulate, 
                                        tube_type = plankton.final_tube_type,  
                                        reagent_type = 'final', 
                                        amount = number_of_final_racks,
                                        deck_positions = [2,5,8], 
                                        protocol = protocol)
    # Loading stock tubesf
    destination_tubes = LW.tube_locations(source_racks = destination_racks,
                                    specific_columns = final_strip_columns,
                                    skip_wells = False,
                                    number_of_tubes = plankton.number_of_transfers,
                                    reagent_type = 'destination',
                                    volume = plankton.transfer_volume/plankton.number_of_transfers,
                                    protocol = protocol)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    #### Transfering stocks
    PM.transferring_reagents(source_wells = stock_tubes,
                             destination_wells = destination_tubes,
                             transfer_volume = plankton.transfer_volume,
                             airgap = False,
                             mix = False,
                             p20 = p20,
                             p300 = p300,
                             protocol = protocol)
## ============================================================================
 
## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================