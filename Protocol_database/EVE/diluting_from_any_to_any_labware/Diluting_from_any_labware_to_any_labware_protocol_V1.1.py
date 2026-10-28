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
            'protocolName': 'Diluting samples in different tube types V1.1',
            'description': 'Diluting anything you want from different tube '
            'types to any tube type you want. If you put the dilution rate to '
            '1, it will transfer the final volume to the tube type of your '
            'choice.'
            }
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Samples
    parameters.add_int(variable_name="number_of_dilutions",
                       display_name="How many samples do you have?",
                       description="Number of samples you want to dilute. Max is 96 samples.",
                       default=96,
                       minimum=0,
                       maximum=96,
                       unit="samples")
    
    #### Tube types
    parameters.add_str(variable_name="sample_tube_type",    
                       display_name="sample tube type",
                       choices=[
                           {"display_name": "PCR-strips", "value": "PCR_strips"},
                           {"display_name": "PCR-plate", "value": "PCR_plate"},
                           {"display_name": "1.5mL tubes", "value": "1.5mL_tubes"},
                           ],
                       default="PCR_strips")
    parameters.add_str(variable_name="final_tube_type",    
                       display_name="final tube type",
                       choices=[
                           {"display_name": "PCR-strips", "value": "PCR_strips"},
                           {"display_name": "PCR-plate", "value": "PCR_plate"},
                           {"display_name": "1.5mL tubes", "value": "1.5mL_tubes"},
                           ],
                       default="PCR_strips")
    
    #### Dilution
    parameters.add_float(variable_name="final_volume",
                         display_name="final volume",
                         description="wat would you like to be your final volume after diluting?",
                         default=30.0,
                         minimum=10.0,
                         maximum=1400.0,
                         unit="ul")
    parameters.add_int(variable_name="dilution_rate",
                       display_name="dilution rate",
                       description="How many times you want to dilute your samples?",
                       default=10,
                       minimum=0,
                       maximum=100000,
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
    parameters.add_bool(variable_name="pause",
                        display_name="pause",
                        description="Do you want to have a pause between alliqouting and transfering your samples?",
                        default= False)

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
    #### Pipetting variables
    # Calculates all the volumes that needs to be pipetted
    stock_volume = plankton.final_volume / plankton.dilution_rate
    reagent_volume = plankton.final_volume - stock_volume
    total_reagent_volume = reagent_volume * plankton.number_of_dilutions
    
    # Defines reagent tube
    water_tube_type, number_of_water_tubes, max_volume_water = LW.which_tube_type(total_reagent_volume,
                                                                                  False)
    
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
        "PCR_strips" : (possible_strip_locations[math.ceil(plankton.number_of_dilutions/8/3)], len(possible_strip_locations[math.ceil(plankton.number_of_dilutions/8/3)])*8),
        "PCR_plate" : (False, 96),
        "1.5mL_tubes" : (False, 24),
        } 
    
    # Calculates number of stock racks
    stock_strip_columns = tube_type_dict[plankton.sample_tube_type][0]
    samples_per_rack = tube_type_dict[plankton.sample_tube_type][1]
    number_of_sample_racks = int(math.ceil((plankton.number_of_dilutions / samples_per_rack)))
                                 
    # Calculates number of final racks
    final_strip_columns = tube_type_dict[plankton.final_tube_type][0]
    destinations_per_rack = tube_type_dict[plankton.final_tube_type][1]
    number_of_final_racks = int(math.ceil((plankton.number_of_dilutions / destinations_per_rack)))


    #### Calculates the amount of tip racks needed and set pipette True or False
    tip_racks_p20, tip_racks_p300, P20, P300 = LW.number_of_tip_racks_2_0(volumes_aliquoting = reagent_volume,
                                                                          number_of_aliquotes = plankton.number_of_dilutions,
                                                                          volumes_transfering = stock_volume,
                                                                          number_of_transfers = plankton.number_of_dilutions,
                                                                          starting_tip_p20 = starting_tip_p20,
                                                                          starting_tip_p300 = starting_tip_p300)
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    if plankton.final_volume > 180 and plankton.final_tube_type != '1.5mL_tubes':
        check = False
    else:
        check = True
        
    if stock_volume < 1:
        raise Exception(f"You would like to dilute {stock_volume} ul. Pipetting"
                        " this amount is not accurate and therefore not advised."
                        " Please enter a bigger final volume or a smaller "
                        "dilution rate to continue!")
    elif 1 <= stock_volume < 2.0:
        protocol.comment(f"You want to pipette {stock_volume} ul of sample. "
                         "This is possible but we advise you to increase the "
                         "final volume or lower the dilution rate a little bit.")
    elif stock_volume >= 2.0 and check == False:
        protocol.comment(f"It is not possible to pipette {plankton.final_volume}"
                         " in {plankton.final_tube_type}. Please select the "
                         "1.5mL tubes or choose a smaller final volume to "
                         "perform this protocol")
    else:    
        protocol.comment(f"I need {number_of_water_tubes} of {water_tube_type}"
                         f"s filled to {max_volume_water} ul.")
    
    if plankton.final_tube_type == '1.5mL_tubes' and plankton.number_of_dilutions > 72:
        raise Exception("Unfortunately, it is not possible to dilute more then "
                        "72 samples with the final tube type 1.5 mL tubes. "
                        "Please, change the final tube type or do less dilutions.")        
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
    #### Water rack
    # Loading water rack
    tube_rack = LW.loading_tube_racks(simulate = simulate, 
                                      tube_type = water_tube_type,  
                                      reagent_type = 'Water', 
                                      amount = 1, 
                                      deck_positions = [11], 
                                      protocol = protocol)
    # Loading water tube
    water_tube = LW.tube_locations(source_racks = tube_rack,
                                   specific_columns = False,
                                   skip_wells = False,
                                   number_of_tubes = number_of_water_tubes,
                                   reagent_type = 'water',
                                   volume = max_volume_water/number_of_water_tubes/number_of_water_tubes,
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
                                    number_of_tubes = plankton.number_of_dilutions,
                                    reagent_type = 'samples',
                                    volume = stock_volume/plankton.number_of_dilutions,
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
    # Loading stock tubes
    destination_tubes = LW.tube_locations(source_racks = destination_racks,
                                    specific_columns = final_strip_columns,
                                    skip_wells = False,
                                    number_of_tubes = plankton.number_of_dilutions,
                                    reagent_type = 'destination',
                                    volume = (reagent_volume + stock_volume)/plankton.number_of_dilutions,
                                    protocol = protocol)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Aliquoting water
    PM.aliquoting_reagent(reagent_source = water_tube,
                          reagent_tube_type = water_tube_type,
                          reagent_startvolume = max_volume_water,
                          aliquot_volume = reagent_volume,
                          destination_wells = destination_tubes,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'next_tube',
                          pause = plankton.pause,
                          protocol = protocol)
    ## ========================================================================
    # Transfering stocks
    PM.transferring_reagents(source_wells = stock_tubes,
                             destination_wells = destination_tubes,
                             transfer_volume = stock_volume,
                             airgap = True,
                             mix = True,
                             p20 = p20,
                             p300 = p300,
                             protocol = protocol)
## ============================================================================
 
## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================