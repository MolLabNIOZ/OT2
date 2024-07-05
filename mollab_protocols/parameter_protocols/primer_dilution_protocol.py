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
sys.path.append("C:/Program files/Opentrons")
sys.path.append("/mnt/c/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Diluting barcoded primers in PCR-strips V1.0',
            'description': 'Dilute your barcoded primers 10 or 5 times from your primer strip stocks to primer strip working dilutions.'
            }
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Primers
    parameters.add_int(variable_name="number_of_primers",
                       display_name="number of unique primers",
                       description="Number of unique primers.",
                       default=96,
                       minimum=0,
                       maximum=96,
                       unit="primers")
    parameters.add_float(variable_name="final_volume",
                       display_name="final volume",
                       description="What do you want the final volume to be?",
                       default=30.0,
                       minimum=1.0,
                       maximum=50.0,
                       unit="µL")
    
    #### Dilution rate
    parameters.add_str(variable_name="dilution_rate",    
                       display_name="dilution rate",
                       choices=[
                           {"display_name": "10 times", "value": "10_times"},
                           {"display_name": "5 times", "value": "5_times"}
                           ],
                       default="10_times")
    
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
                           {"display_name": "F", "value": "F"},
                           {"display_name": "G", "value": "G"},
                           {"display_name": "H", "value": "H"}
                           ],
                       default="A")
    parameters.add_str(variable_name="starting_tip_p20_column",    
                       display_name="starting tip p20 column",
                       choices=[
                           {"display_name": "1", "value": "this_is_not_an_int1"},
                           {"display_name": "2", "value": "this_is_not_an_int2"},
                           {"display_name": "3", "value": "this_is_not_an_int3"},
                           {"display_name": "4", "value": "this_is_not_an_int4"},
                           {"display_name": "5", "value": "this_is_not_an_int5"},
                           {"display_name": "6", "value": "this_is_not_an_int6"},
                           {"display_name": "7", "value": "this_is_not_an_int7"},
                           {"display_name": "8", "value": "this_is_not_an_int8"},
                           {"display_name": "9", "value": "this_is_not_an_int9"},
                           {"display_name": "10", "value": "this_is_not_an_int10"},
                           {"display_name": "11", "value": "this_is_not_an_int11"},
                           {"display_name": "12", "value": "this_is_not_an_int12"}
                           ],
                       default="this_is_not_an_int1")
    
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
                           {"display_name": "F", "value": "F"},
                           {"display_name": "G", "value": "G"},
                           {"display_name": "H", "value": "H"}
                           ],
                       default="A")
    parameters.add_str(variable_name="starting_tip_p300_column",    
                       display_name="starting tip p300 column",
                       choices=[
                           {"display_name": "1", "value": "this_is_not_an_int1"},
                           {"display_name": "2", "value": "this_is_not_an_int2"},
                           {"display_name": "3", "value": "this_is_not_an_int3"},
                           {"display_name": "4", "value": "this_is_not_an_int4"},
                           {"display_name": "5", "value": "this_is_not_an_int5"},
                           {"display_name": "6", "value": "this_is_not_an_int6"},
                           {"display_name": "7", "value": "this_is_not_an_int7"},
                           {"display_name": "8", "value": "this_is_not_an_int8"},
                           {"display_name": "9", "value": "this_is_not_an_int9"},
                           {"display_name": "10", "value": "this_is_not_an_int10"},
                           {"display_name": "11", "value": "this_is_not_an_int11"},
                           {"display_name": "12", "value": "this_is_not_an_int12"}
                           ],
                       default="this_is_not_an_int1")
    
    #### Lights/Pause  
    parameters.add_bool(variable_name="lights_on",
                        display_name="lights on",
                        description="Do you want the lights turned ON?",
                        default=True)
    
def run(protocol: protocol_api.ProtocolContext):
    # Sets p as variable for protocol.params, this will make it all shorter
    plankton = protocol.params
# =============================================================================

## CONVERTING VARIABLES========================================================
## ============================================================================
    # Sets variables for the starting tips
    starting_tip_p20 = plankton.starting_tip_p20_row + plankton.starting_tip_p20_column.strip("this_is_not_an_int")
    starting_tip_p300 = plankton.starting_tip_p300_row + plankton.starting_tip_p300_column.strip("this_is_not_an_int")

    # Sets variable for the dilution_rate
    dilution_rate = plankton.dilution_rate.strip("_times")
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    # Calculates the volumes that need to be pipetted
    stock_volume = plankton.final_volume / dilution_rate
    reagent_volume = plankton.final_volume - stock_volume   
    total_reagent_volume = reagent_volume * plankton.number_of_primers
    reagent_tube_type, number_of_reagent_tubes, max_volume = LW.which_tube_type(total_reagent_volume,
                                                                                False)
    
    # Sets location for the strips
    stock_strip_columns = ['2', '5', '8', '11']
    dilution_strip_columns = ['2', '5', '8', '11']
    
    number_stock_racks = math.ceil(plankton.number_of_primers / (len(stock_strip_columns)*8))
    number_dilution_racks = math.ceil(plankton.number_of_primers / (len(dilution_strip_columns)*8))
      ## How many strip_racks are needed (1,2,3 or 4) for primer stocks. The same
      ## amount is needed for primer dilutions
    
    #### Pipette tips calculations
    # Calculates the amount of tips needed
    p20_tips_needed_stock, p300_tips_needed_stock = LW.amount_of_tips(stock_volume,
                                                                      plankton.number_of_primers,
                                                                      1,
                                                                      19)
    p20_tips_needed_reagent, p300_tips_needed_reagent = LW.amount_of_tips(reagent_volume,
                                                                          plankton.number_of_primers,
                                                                          16,
                                                                          15)
    
    p20_tips_needed = p20_tips_needed_stock + p20_tips_needed_reagent
    p300_tips_needed = p300_tips_needed_stock + p300_tips_needed_reagent
    
    # Defines how much P20 and P300 tip racks you need and if the pipette is True/False
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               p20_tips_needed)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip_p300,
                                               p300_tips_needed)
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    protocol.comment(f"I need {number_of_reagent_tubes} of {reagent_tube_type}"
                     f"s completely filled with reagent.")
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
                               [1,4,10,7],
                               protocol)
    tips_p300 = LW.loading_tips(simulate,
                               'opentrons_200uL',
                               tip_racks_p300,
                               [7,10,4,1],
                               protocol)
    ## ========================================================================
    #### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20, 
                                    tips_p20,
                                    starting_tip_p20,
                                    P300, 
                                    tips_p300,
                                    starting_tip_p300,
                                    protocol)
    ## ========================================================================
    #### Loading reagent racks
    # Loading reagent rack 
    reagent_racks = LW.loading_tube_racks(simulate = simulate,
                                          tube_type = reagent_tube_type,
                                          reagent_type = 'dilution_reagent',
                                          amount = 1,
                                          deck_positions = [11],
                                          protocol = protocol)
    ## Specific location of tubes
    reagent = LW.tube_locations(source_racks = reagent_racks,
                                specific_columns = False,
                                skip_wells = False,
                                number_of_tubes = number_of_reagent_tubes,
                                reagent_type = 'water',
                                volume = max_volume,
                                protocol = protocol)
    ## ========================================================================
    #### Loading stock racks
    ## Loading stock plates
    stock_racks = LW.loading_tube_racks(simulate = simulate,
                                        tube_type = 'PCR_strips',
                                        reagent_type = 'stocks',
                                        amount = number_stock_racks,
                                        deck_positions = [2,5,8],
                                        protocol = protocol)
    # Specific location of tubes
    stocks = LW.tube_locations(source_racks = stock_racks,
                               specific_columns = stock_strip_columns,
                               skip_wells = False,
                               number_of_tubes = plankton.number_to_dilute,
                               reagent_type = 'primer_stocks',
                               volume = stock_volume,
                               protocol = protocol)
    ## ========================================================================
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    