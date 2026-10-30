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
sys.path.append("/home/maartje/GitHub/OT2/")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules_v5 as PM
from data.user_storage.mollab_modules import LabWare_v3 as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Diluting samples from strips to strips or plate with a multichannel V1',
            'description': 'Diluting samples from strips to strips or plate with a multichannel'
            'If you put the dilution rate to 1, it will transfer the final volume to the tube type of your choice.'
            }
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    #### Samples
    parameters.add_int(variable_name="number_of_samples",
                        display_name="How many samples do you have?",
                        description="Number of samples you want to dilute. Max is 96 samples.",
                        default=96,
                        minimum=0,
                        maximum=96,
                        unit="samples")
    
   #### Dilution
    parameters.add_str(variable_name="final_tube_type",
                        display_name="final tube type",
                        choices=[
                            {"display_name": "PCR-strips", "value": "PCR_strips"},
                            {"display_name": "PCR-plate", "value": "skirted_plate_96"}
                            ],
                        default="PCR_strips")
    parameters.add_float(variable_name="final_volume",
                         display_name="final volume",
                         description="what would you like to be your final volume after diluting?",
                         default=22.0,
                         minimum=22.0,
                         maximum=200.0,
                         unit="µl")
    parameters.add_int(variable_name="dilution_rate",
                       display_name="dilution rate",
                       description="How many times you want to dilute your samples?",
                       default=10,
                       minimum=10,
                       maximum=100,
                       unit="times")

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
    
def run(protocol: protocol_api.ProtocolContext):
    plankton = protocol.params
# =============================================================================

## CONVERTING VARIABLES========================================================
## ============================================================================
    #### Starting tips  
    # Combining the row-variable with the column-variable to create starting tip
    starting_tip_p20 = "A1"
    if plankton.starting_tip_p300_row == 'this_is_not_false':
        starting_tip_p300_row = 'F'
    else:
        starting_tip_p300_row = plankton.starting_tip_p300_row
    # Combining the row-variable with the column-variable to create starting tip
    starting_tip_p300 = starting_tip_p300_row + str(plankton.starting_tip_p300_column)
    #### Number of samples
    half_column_tubes = plankton.number_of_samples % 8
    extra_tubes = 0
    if half_column_tubes > 0:
        extra_tubes = 8 - half_column_tubes
        final_number_of_samples = plankton.number_of_samples + extra_tubes
        protocol.comment(f"{extra_tubes} extra negative controls are added to fill up to entire columns. "
                            "This is necesarry to accomodate the multichannel pipette")
    else:
        final_number_of_samples = plankton.number_of_samples 
# =============================================================================
## CALCULATED VARIABLES========================================================
## ============================================================================
    #### Pipetting variables
    # Calculates all the volumes that needs to be pipetted
    stock_volume = plankton.final_volume / plankton.dilution_rate
    reagent_volume = plankton.final_volume - stock_volume
    total_reagent_volume = reagent_volume * final_number_of_samples
    
    # Defines reagent tube
    if total_reagent_volume > 1500 and reagent_volume <= 19:
        tube_type = '1.5mL_tubes'
    else:
        tube_type = False
    water_tube_type, number_of_water_tubes, max_volume_water = LW.which_tube_type(total_reagent_volume,tube_type)

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
        "PCR_strips" : (possible_strip_locations[math.ceil(final_number_of_samples/8/3)], len(possible_strip_locations[math.ceil(final_number_of_samples/8/3)])*8),
        "skirted_plate_96" : (False, 96)
        } 
    
    # Calculates number of stock racks
    stock_strip_columns = tube_type_dict['PCR_strips'][0]
    samples_per_rack = tube_type_dict['PCR_strips'][1]
    number_of_sample_racks = int(math.ceil((final_number_of_samples / samples_per_rack)))
                                 
    # Calculates number of final racks
    final_strip_columns = tube_type_dict[plankton.final_tube_type][0]
    destinations_per_rack = tube_type_dict[plankton.final_tube_type][1]
    number_of_final_racks = int(math.ceil((final_number_of_samples / destinations_per_rack)))

        #### Calculates the amount of tip racks needed and set pipette True or False
    tip_racks_p20, tip_racks_p300, P20, P300 = LW.number_of_tip_racks_2_0(volumes_aliquoting = reagent_volume,
                                                                          number_of_aliquotes = final_number_of_samples,
                                                                          volumes_transfering = stock_volume,
                                                                          number_of_transfers = final_number_of_samples,
                                                                          starting_tip_p20 = starting_tip_p20,
                                                                          starting_tip_p300 = starting_tip_p300)
## COMMENTS====================================================================
## ============================================================================
    if stock_volume < 1:
        raise Exception(f"For your dilutions, {stock_volume} µl of your sample will be used. "
                        "Pipetting this amount is not accurate and therefore not advised. "
                        "Please enter a bigger final volume or a smaller dilution rate to continue!")
    elif 1 <= stock_volume < 2.0:
        protocol.comment(f"For your dilutions, {stock_volume} µl of your sample will be used. "
                         "This is possible but we advise you to increase the final volume or lower the dilution rate a little bit.")
        protocol.comment(f"I need {number_of_water_tubes} of {water_tube_type}"
                                 f" filled to {max_volume_water} µl with water.")  
    else:    
        protocol.comment(f"I need {number_of_water_tubes} of {water_tube_type}"
                         f" filled to {max_volume_water} µl with water.")     
## ============================================================================

# =============================================================================
# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_p20 = LW.loading_tips(simulate,
                               'tipone_20uL',
                               1,
                               [1],
                               protocol)
    tips_p300 = LW.loading_tips(simulate,
                               'opentrons_200uL',
                               tip_racks_p300,
                               [7,10],
                               protocol)
    ## ========================================================================
    #### PIPETTES
    left_pipette, right_pipette = LW.loading_pipettes('P20multi',
                                                      'P300',
                                                      tips_p20,
                                                      starting_tip_p20, 
                                                      tips_p300,
                                                      starting_tip_p300,
                                                      protocol)
    ## ========================================================================
    #### Water rack

    # Loading water tube
    if number_of_water_tubes > 0:
        # Loading water rack
        tube_rack = LW.loading_tube_racks(simulate = simulate,
                                          tube_type = water_tube_type,
                                          reagent_type = 'Water',
                                          amount = 1,
                                          deck_positions = [11],
                                          protocol = protocol)
        # Loading water tubes
        water_volume = max_volume_water/number_of_water_tubes/number_of_water_tubes

        water_tube = LW.tube_locations(source_racks = tube_rack,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = number_of_water_tubes,
                                       reagent_type = 'water',
                                       volume = water_volume,
                                       protocol = protocol)
    ## ========================================================================
    #### Stock racks
        # Loading stock racks
    stock_racks = LW.loading_tube_racks(simulate = simulate, 
                                        tube_type = 'PCR_strips',  
                                        reagent_type = 'samples', 
                                        amount = number_of_sample_racks,
                                        deck_positions = [2,5,8], 
                                        protocol = protocol)
    # Loading stock tubes
    stock_tubes, empty_tubes = LW.multiple_reagent_tube_locations(source_racks = stock_racks,
                                                     specific_columns = stock_strip_columns,
                                                     skip_wells = False,
                                                     reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'NTC': extra_tubes},
                                                     volume = stock_volume,
                                                     protocol = protocol)

    ## ========================================================================
    #### Final tube racks
    # Loading final racks
    destination_racks = LW.loading_tube_racks(simulate = simulate, 
                                        tube_type = plankton.final_tube_type,  
                                        reagent_type = 'final', 
                                        amount = number_of_final_racks,
                                        deck_positions = [3,6,9], 
                                        protocol = protocol)
    # Loading stock tubes
    sample_destination, empty_destination = LW.multiple_reagent_tube_locations(source_racks = destination_racks,
                                                     specific_columns = final_strip_columns,
                                                     skip_wells = False,
                                                     reagent_and_numbers_dict = {'destination': plankton.number_of_samples, 'NTC': extra_tubes},
                                                     volume = (reagent_volume + stock_volume)/final_number_of_samples,
                                                     protocol = protocol)
## ============================================================================
## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(True)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Aliquoting water
    if number_of_water_tubes == 1:
        action_at_bottom = 'next_tube'
    else:
        action_at_bottom = 'continue_at_bottom'
    if number_of_water_tubes > 0:
        PM.aliquoting_reagent(reagent_source = water_tube,
                              reagent_tube_type = water_tube_type,
                              reagent_startvolume = max_volume_water,
                              aliquot_volume = reagent_volume,
                              destination_wells = sample_destination + empty_destination,
                              p20 = left_pipette,
                              p300 = right_pipette,
                              action_at_bottom = action_at_bottom,
                              pause = False,
                              protocol = protocol)
    ## ========================================================================
    # Transfering stocks
    PM.transferring_reagents_multichannel(source_wells = stock_tubes + empty_tubes,
                                          destination_wells = sample_destination + empty_destination,
                                          transfer_volume = stock_volume,
                                          airgap = True,
                                          mix = True,
                                          p20 = left_pipette,
                                          tips_20 = tips_p20,
                                          p300 = False,
                                          tips_300 = False,
                                          protocol = protocol)
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================