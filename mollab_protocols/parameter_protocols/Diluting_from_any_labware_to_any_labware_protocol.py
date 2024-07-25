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
            'protocolName': 'Diluting samples in different tube types',
            'description': 'Diluting anything you want from different tube types to any tube type you want'
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
                           {"display_name": "F", "value": "F_is_not_a_bool"},
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
                           {"display_name": "F", "value": "F_is_not_a_bool"},
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
    plankton = protocol.params
# =============================================================================

## CONVERTING VARIABLES========================================================
## ============================================================================
    #### Starting tips
    starting_tip_p20 = plankton.starting_tip_p20_row[0] + str(plankton.starting_tip_p20_column)
    starting_tip_p300 = plankton.starting_tip_p300_row[0] + str(plankton.starting_tip_p300_column)
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    # Calculates all the volumes that needs to be pipetted
    stock_volume = plankton.final_volume / plankton.dilution_rate
    reagent_volume = plankton.final_volume - stock_volume
    total_reagent_volume = reagent_volume * plankton.number_of_dilutions
    
    # Definees reagent tube
    reagent_tube_type, number_of_reagent_tubes, max_volume = LW.which_tube_type(total_reagent_volume,
                                                                                False)
    # Possible locations of strips in racks
    possible_strip_locations = {
        1:['6'],
        2:['3','9'],
        3:['2','7','11'],
        4:['2','5','8','11'],
        5:['1','3','6','9','12'],
        6:['1','3','5','7','9','11']
        }     
    
    # Calculates number of stock racks
    if plankton.sample_tube_type == "PCR_strips":
        stock_strip_columns = possible_strip_locations[math.ceil(plankton.number_of_dilutions/8/3)]    
        samples_per_rack = len(stock_strip_columns)*8
    if plankton.sample_tube_type == "PCR_plate":
        stock_strip_columns = False
        samples_per_rack = 96
    if plankton.sample_tube_type == "1.5mL_tubes":
        stock_strip_columns = False
        samples_per_rack = 24
    number_of_sample_racks = plankton.number_of_dilutions / samples_per_rack
    
    # Calculates number of destination racks
    if plankton.final_tube_type == "PCR_strips":
        final_strip_columns = possible_strip_locations[math.ceil(plankton.number_of_dilutions/8/3)]  
        destinations_per_rack = len(final_strip_columns)*8
    if plankton.final_tube_type == "PCR_plate":
        final_strip_columns = False
        destinations_per_rack = 96
    if plankton.final_tube_type == "1.5mL_tubes":
        final_strip_columns = False
        destinations_per_rack = 24
    number_of_final_racks = plankton.number_of_dilutions / destinations_per_rack

## ============================================================================

## CHECKS======================================================================
## ============================================================================
    if plankton.final_volume > 180 and plankton.final_tube_type != '1.5mL_tubes':
        check = False
    else:
        check = True
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    if stock_volume < 1:
        raise Exception(f"You would like to dilute {stock_volume} ul. Pipetting"
                        " this amount is not accurate and therefore not advised."
                        " Please enter a bigger final volume or a smaller dilution rate to continue!")
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
        protocol.comment(f"I need {number_of_reagent_tubes} of {reagent_tube_type}"
                         f"s filled to {max_volume} ul.")
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(plankton.lights_on)
## ============================================================================