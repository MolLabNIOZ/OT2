volumes = [20.77, 24.42, 22.27, 40.57, 39.69, 49.28, 39.31, 25.17, 39.72, 46.91, 21.56, 26.27, 24.04, 54.0, 32.23, 47.34, 47.38, 17.28, 41.59, 24.7, 33.19, 30.36, 34.05, 34.24, 33.15, 39.92, 56.69, 35.73, 27.89, 80.1, 49.4, 67.16, 23.65, 23.48, 20.77, 27.36, 27.36, 23.09, 27.35, 119.63, 17.01, 37.2, 13.17, 47.74, 30.52, 53.74, 33.45, 74.03, 54.13, 21.17, 31.65, 21.11, 58.47, 19.82, 20.82, 45.33, 32.58, 154.56, 138.53, 14.51, 17.15, 44.22, 43.29, 179.74, 80.17, 127.75, 162.31, 71.78, 140.49, 161.14, 67.69, 16.87, 24.29, 15.02, 19.98, 16.79, 140.76, 121.18, 36.4, 50.56, 51.17, 23.72, 64.32, 79.54, 31.05, 57.77, 75.23, 57.94, 29.4, 59.77, 46.46, 26.11, 30.59, 30.59, 58.56, 52.92]
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
from data.user_storage.mollab_modules import Pipetting_Modules_v5 as PM
from data.user_storage.mollab_modules import LabWare_v3 as LW
from data.user_storage.mollab_modules import LabWare_v2 as LW2


# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Run 13 Lena_transferring to plate in duplicate',
            'description': 'Transferring from any tube type to 1 or more plates'}
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    #### Tube type
    parameters.add_str(variable_name="sample_tube_type",    
                       display_name="sample tube type",
                       choices=[
                           {"display_name": "PCR-strips", "value": "PCR_strips"},
                           {"display_name": "PCR-plate", "value": "skirted_plate_96"},
                           {"display_name": "PCR-plate_holder", "value": "plate_96_NIOZholder"},
                           {"display_name": "1.5mL tubes", "value": "1.5mL_tubes"},
                           ],
                       default="1.5mL_tubes")

    #### Transfers
    parameters.add_int(variable_name="number_of_duplicate_transfers",
                       display_name="How many duplicate transfers",
                       description="number of times transferred",
                       default=2,
                       minimum=0,
                       maximum=3,
                       unit="times")    

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
        "PCR_strips" : (possible_strip_locations[math.ceil(len(volumes)/8/3)], len(possible_strip_locations[math.ceil(len(volumes)/8/3)])*8),
        "skirted_plate_96" : (False, 96),
        "plate_96_NIOZholder" : (False, 96),
        "1.5mL_tubes" : (False, 24),
        } 
    
    # Calculates number of stock racks
    stock_strip_columns = tube_type_dict[plankton.sample_tube_type][0]
    samples_per_rack = tube_type_dict[plankton.sample_tube_type][1]
    number_of_sample_racks = int(math.ceil((len(volumes) / samples_per_rack)))
                                 

    #### Calculates the amount of tip racks needed and set pipette True or False
    amount_tips_20, amount_tips_300 = LW.amount_of_tips(volumes,
                                                        len(volumes),
                                                        1,
                                                        19)
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               amount_tips_20)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip_p300,
                                                 amount_tips_300)    
## ============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_p20 = LW.loading_tips(simulate,
                               'tipone_20uL',
                               tip_racks_p20,
                               [1,4,7,10],
                               protocol)
    tips_p300 = LW.loading_tips(simulate,
                               'opentrons_200uL',
                               tip_racks_p300,
                               [10,7,4,1],
                               protocol)
    ## ========================================================================
    #### Loading pipettes
    p20, p300 = LW.loading_pipettes(left = 'P20',
                                    right = 'P300',
                                    tips_20 = tips_p20,
                                    starting_tip_p20 = starting_tip_p20,
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
                                        deck_positions = [2,5,8,11], 
                                        protocol = protocol)
    # Loading stock tubes
    stock_tubes = LW.tube_locations(source_racks = stock_racks,
                                    specific_columns = stock_strip_columns,
                                    skip_wells = False,
                                    number_of_tubes = len(volumes),
                                    reagent_type = 'samples',
                                    volume = 150,
                                    protocol = protocol)
    ## ========================================================================
    #### Final tube racks
    # Loading final racks
    destination_racks = LW.loading_tube_racks(simulate = simulate, 
                                              tube_type = 'skirted_plate_96',  
                                              reagent_type = 'final', 
                                              amount = plankton.number_of_duplicate_transfers,
                                              deck_positions = [3,6,9], 
                                              protocol = protocol)
    # Loading stock tubes         
    destination_tubes = []
    for i in range(plankton.number_of_duplicate_transfers):
        current_destination_tubes = LW2.tube_locations_varying_liquid(source_racks = [destination_racks[i]],
                                                                     specific_columns = False,
                                                                     skip_wells = False,
                                                                     number_of_tubes = len(volumes),
                                                                     reagent_type = 'destination',
                                                                     volume_list = volumes,
                                                                     protocol = protocol)
        destination_tubes.append(current_destination_tubes)
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(True)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    #### Transfering stocks
    PM.transferring_varying_volumes_duplicate(source_wells = stock_tubes,
                                              destination_wells = destination_tubes,
                                              transfer_volumes = volumes,
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
