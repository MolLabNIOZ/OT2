volumes = [18.06, 18.51, 14.42, 22.83, 28.1, 24.98, 24.03, 15.64, 71.62, 22.76, 14.16, 30.72, 39.1, 20.09, 56.5, 41.22, 21.3, 16.12, 15.95, 14.14, 14.16, 15.49, 14.16, 14.91, 26.1, 15.02, 49.28, 30.96, 74.23, 44.68, 25.21, 20.96, 25.87, 25.83, 18.31, 18.37, 19.75, 19.14, 16.51, 18.86, 17.37, 17.51, 19.58, 43.25, 37.98, 17.36, 17.87, 30.17, 20.42, 17.12, 18.87, 27.36, 27.89, 22.76, 21.21, 24.39, 36.07, 23.46, 21.58, 17.04, 18.37, 17.66, 19.85, 19.15, 19.14, 18.18, 19.51, 19.8, 17.82, 19.59, 21.81, 33.02, 22.37, 19.63, 18.15, 21.02, 19.99, 17.7, 14.16, 14.14, 24.35, 41.95, 19.15, 23.89, 40.46, 46.16, 18.84, 23.05, 21.7, 15.19, 15.23, 15.21, 15.19, 75.0, 15.2, 15.19]
water_volumes = [56.94, 56.49, 60.58, 52.17, 46.9, 50.02, 50.97, 59.36, 3.38, 52.24, 60.84, 44.28, 35.9, 54.91, 18.5, 33.78, 53.7, 58.88, 59.05, 60.86, 60.84, 59.51, 60.84, 60.09, 48.9, 59.98, 25.72, 44.04, 0.77, 30.32, 49.79, 54.04, 49.13, 49.17, 56.69, 56.63, 55.25, 55.86, 58.49, 56.14, 57.63, 57.49, 55.42, 31.75, 37.02, 57.64, 57.13, 44.83, 54.58, 57.88, 56.13, 47.64, 47.11, 52.24, 53.79, 50.61, 38.93, 51.54, 53.42, 57.96, 56.63, 57.34, 55.15, 55.85, 55.86, 56.82, 55.49, 55.2, 57.18, 55.41, 53.19, 41.98, 52.63, 55.37, 56.85, 53.98, 55.01, 57.3, 60.84, 60.86, 50.65, 33.05, 55.85, 51.11, 34.54, 28.84, 56.16, 51.95, 53.3, 59.81, 59.77, 59.79, 59.81, 0.0, 59.8, 59.81]
# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
simulate = True
#### Import opentrons protocol API v2
from opentrons import protocol_api
#### Import math 
import math ## To do some calculations
#### For simulating in the app, set pathway to modules
import sys
sys.path.append("O:/")
sys.path.append("/mnt/c/Program files/Opentrons")
sys.path.append("C:/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules_v5 as PM
from data.user_storage.mollab_modules import LabWare_v3 as LW

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': '260122_Lena_transferring to plate in duplicate',
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
    parameters.add_bool(variable_name="add_water",
                        display_name="Do you want to add water",
                        description="Do you need all wells to contain the same volume?",
                        default=True)

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
                       default="A")
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
                       default=1)
    
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
    tips_samples = LW.amount_of_tips(volumes,
                                     len(volumes),
                                     1,
                                     15)
    tips_water = LW.amount_of_tips(water_volumes,
                                   len(water_volumes),
                                   16,
                                   19)
    amount_tips_20 = tips_samples[0] + tips_water[0]
    amount_tips_300 = tips_samples[1] + tips_water[1]
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
        current_destination_tubes = LW.tube_locations_varying_liquid(source_racks = [destination_racks[i]],
                                                                     specific_columns = False,
                                                                     skip_wells = False,
                                                                     number_of_tubes = len(volumes),
                                                                     reagent_type = 'destination',
                                                                     volume_list = volumes,
                                                                     protocol = protocol)
        destination_tubes.append(current_destination_tubes)

    # Loading tube(s) for water
    if plankton.add_water:
        water_tube_type, number_of_tubes, max_volume = LW.which_tube_type(
            total_volume = sum(water_volumes) * 1.2,
            tube_type = '5mL_screwcap_tubes')
        water_racks = LW.loading_tube_racks(simulate = simulate,
                                            tube_type = water_tube_type,
                                            reagent_type = 'Water',
                                            amount = 1,
                                            deck_positions = [9],
                                            protocol = protocol)
        water_tube = LW.tube_locations(source_racks = water_racks,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = number_of_tubes,
                                       reagent_type = 'water',
                                       volume = max_volume,
                                       protocol = protocol)

## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(True)
## ============================================================================

# COMMENTS=====================================================================
# =============================================================================
    if plankton.add_water:
        protocol.pause(f"Put {number_of_tubes} {water_tube_type} with {max_volume}µL of water "
                       "in Deck slot 9")
# =============================================================================
## PIPETTING===================================================================
## ============================================================================
    ### 
    if plankton.add_water:       
        PM.aliquoting_varying_volumes(reagent_source = water_tube, 
                                      reagent_tube_type = water_tube_type, 
                                      reagent_startvolume = max_volume, 
                                      aliquot_volumes = water_volumes, 
                                      destination_wells = destination_tubes[1], 
                                      p20 = p20, 
                                      p300 = p300, 
                                      tip_change = 16, 
                                      action_at_bottom = 'next_tube', 
                                      pause = False, 
                                      protocol = protocol)

    ### Transfering stocks
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
