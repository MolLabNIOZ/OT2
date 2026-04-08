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
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules_v5 as PM
from data.user_storage.mollab_modules import LabWare_v3 as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Diluting barcoded primers in PCR-strips with multichannel V1',
            'description': 'Dilute your barcoded primers 10 or 5 times from your primer strip stocks to primer strip working dilutions.'
            }
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}
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
    parameters.add_int(variable_name="start_primer",
                       display_name="starting primer",
                       description="with what barcode do you want to start your set",
                       default=1,
                       minimum=1,
                       maximum=96,
                       unit="barcode")
    parameters.add_float(variable_name="final_volume",
                       display_name="final volume",
                       description="What do you want the final volume to be?",
                       default=20.0,
                       minimum=1.0,
                       maximum=50.0,
                       unit="µL")
    #### Dilution rate
    parameters.add_int(variable_name="dilution_rate",    
                       display_name="dilution rate",
                       choices=[
                           {"display_name": "10 times", "value": 10},
                           {"display_name": "5 times", "value": 5}
                           ],
                       default=10)
    
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
    # Sets p as variable for protocol.params, this will make it all shorter
    plankton = protocol.params
# =============================================================================

## CONVERTING VARIABLES========================================================
## ============================================================================
    #### Starting tips
    starting_tip_p20 = 'A1'
    # Combining the row-variable with the column-variable to create starting tip
    if plankton.starting_tip_p300_row == 'this_is_not_false':
        starting_tip_p300_row = 'F'
    else:
        starting_tip_p300_row = plankton.starting_tip_p300_row
    starting_tip_p300 = starting_tip_p300_row + str(plankton.starting_tip_p300_column)
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    # Calculates the volumes that need to be pipetted
    stock_volume = plankton.final_volume / plankton.dilution_rate
    reagent_volume = plankton.final_volume - stock_volume   
    
    # Sets location for the strips
    possible_primer_locations = {
        1:['6'],
        2:['3','9'],
        3:['2','7','11'],
        4:['2','5','8','11'],
        5:['1','3','6','9','12'],
        6:['1','3','5','7','9','11']
        }    
    stock_strip_columns = dilution_strip_columns = possible_primer_locations[math.ceil(plankton.number_of_primers/8/2)]
    ## How many tube_strip_racks are needed
    primer_per_rack = 8 * len(stock_strip_columns)
    # How many strip_racks are needed (1,2,3 or 4)
    number_stock_racks = number_dilution_racks = math.ceil(plankton.number_of_primers / primer_per_rack)
      
    #### Pipette tips calculations
    # Calculates the amount of tips needed
    p20_tips_needed_stock, p300_tips_needed_stock = LW.amount_of_tips(stock_volume,
                                                                      plankton.number_of_primers,
                                                                      1,
                                                                      19)
    p20_tips_needed_reagent, p300_tips_needed_reagent = LW.amount_of_tips(reagent_volume,
                                                                          plankton.number_of_primers,
                                                                          16,
                                                                          19)
    
    p20_tips_needed = p20_tips_needed_stock + p20_tips_needed_reagent
    p300_tips_needed = p300_tips_needed_stock + p300_tips_needed_reagent
    
    # Defines how much P20 and P300 tip racks you need and if the pipette is True/False
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               p20_tips_needed)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip_p300,
                                               p300_tips_needed)
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(True)
## ============================================================================    

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_20 = LW.loading_tips(simulate,
                              'tipone_20uL',
                              tip_racks_p20,
                              [4,7,10],
                              protocol)
    tips_300 = LW.loading_tips(simulate,
                               'opentrons_200uL',
                               tip_racks_p300,
                               [10],
                               protocol)
    ## ========================================================================
    #### Loading pipettes
    left = 'P20multi'
    if P300:
        right = 'P300'
    else:
        right = False
    left_pipette, right_pipette = LW.loading_pipettes(left,
                                                      right,
                                                      tips_20,
                                                      starting_tip_p20, 
                                                      tips_300,
                                                      starting_tip_p300,
                                                      protocol)
    ## ========================================================================
    #### Loading reagent racks
    # Decide what tube type you need for the dilution reagent
    total_reagent_volume = (reagent_volume * plankton.number_of_primers) * 1.2 #+20%
    # Multichannel can only pipette from 1.5ml tubes or smaller
    if total_reagent_volume > 1500 and reagent_volume <= 19:
        reagent_tube_type = '1.5mL_tubes'
    else:
        reagent_tube_type = False
    
    reagent_tube_type, number_of_reagent_tubes, max_volume = LW.which_tube_type(total_reagent_volume,
                                                                                reagent_tube_type)
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
    # Loading stock plates
    stock_racks = LW.loading_tube_racks(simulate = simulate,
                                        tube_type = 'PCR_strips',
                                        reagent_type = 'stocks',
                                        amount = number_stock_racks,
                                        deck_positions = [5,8],
                                        protocol = protocol)
    # Specific location of tubes
    stocks = LW.tube_locations(source_racks = stock_racks,
                               specific_columns = stock_strip_columns,
                               skip_wells = False,
                               number_of_tubes = plankton.number_of_primers,
                               reagent_type = 'primer_stocks',
                               volume = stock_volume,
                               protocol = protocol)
    ## ========================================================================
    #### Loading dilution racks
    # Loading dilution plates
    dilution_racks = LW.loading_tube_racks(simulate = simulate,
                                        tube_type = 'PCR_strips',
                                        reagent_type = 'dilution',
                                        amount = number_dilution_racks,
                                        deck_positions = [6,9],
                                        protocol = protocol)
    # Specific location of tubes
    dilutions = LW.tube_locations(source_racks = dilution_racks,
                               specific_columns = dilution_strip_columns,
                               skip_wells = False,
                               number_of_tubes = plankton.number_of_primers,
                               reagent_type = 'primer_working_dilution',
                               volume = plankton.final_volume,
                               protocol = protocol)
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    protocol.comment(f"I need {number_of_reagent_tubes} {reagent_tube_type}"
                     f" filled to {math.ceil((total_reagent_volume / number_of_reagent_tubes)*1.2)}µL with reagent.")
    protocol.comment("Put your primer strips in the following columns"
                     f"{stock_strip_columns}")
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Aliquoting reagents
    left_pipette.reset_tipracks()
    left_pipette.configure_nozzle_layout(style=protocol_api.SINGLE, start='A1', tip_racks=tips_20)      
    
    if number_of_reagent_tubes > 1:
        action_at_bottom = 'next_tube'
    else:
        action_at_bottom = 'continue_at_bottom'
        
    PM.aliquoting_reagent(reagent_source = reagent,
                          reagent_tube_type = reagent_tube_type,
                          reagent_startvolume = total_reagent_volume / number_of_reagent_tubes,
                          aliquot_volume = reagent_volume,
                          destination_wells = dilutions,
                          p20 = left_pipette,
                          p300 = right_pipette,
                          action_at_bottom = action_at_bottom,
                          pause = False,
                          protocol = protocol)
    
    # # Transfering stocks
    PM.transferring_reagents_multichannel(source_wells = stocks,
                                           destination_wells = dilutions,
                                           transfer_volume = stock_volume,
                                           airgap = True,
                                           mix = True,
                                           p20 = left_pipette,
                                           tips_20 = tips_20,
                                           p300 = right_pipette,
                                           tips_300 = tips_300,
                                           protocol = protocol)
## ============================================================================
 
## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================