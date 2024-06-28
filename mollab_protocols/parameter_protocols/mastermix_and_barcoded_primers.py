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
            'protocolName': 'mastermix_and_barcoded_primers',
            'description': 'aliquoting mix and distributing barcoded primers'}
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Mastermix
    parameters.add_int(variable_name="total_mastermix_volume",
                       display_name="total mastermix volume",
                       description="How much volume is in your mastermix tube?",
                       default=3000,
                       minimum=0,
                       maximum=50000,
                       unit="µL MM")
    parameters.add_int(variable_name="mastermix_volume",
                       display_name="mastermix volume per reaction",
                       description="How much mastermix should each reaction get?",
                       default=20,
                       minimum=0,
                       maximum=50,
                       unit="µL MM")
    #### Samples/Barcodes
    parameters.add_int(variable_name="number_of_barcodes",
                       display_name="number of unique barcodes",
                       description="Number of unique barcode combinations. Include samples, mock, NTC, etc.",
                       default=96,
                       minimum=0,
                       maximum=96,
                       unit="barcodes")
    parameters.add_int(variable_name="primer_vol",
                       display_name="primer volume",
                       description="How much (µL) should be added of each primer?",
                       default=3,
                       minimum=0,
                       maximum=5,
                       unit="µL primer")    
    parameters.add_int(variable_name="skipped_forward_barcodes",
                       display_name="forwards to skip",
                       description="How many forward barcodes should WALL-E skip?",
                       default=0,
                       minimum=0,
                       maximum=95,
                       unit="barcodes")
    parameters.add_int(variable_name="skipped_reverse_barcodes",
                       display_name="reverses to skip",
                       description="How many reverse barcodes should WALL-E skip?",
                       default=0,
                       minimum=0,
                       maximum=95,
                       unit="barcodes")
    parameters.add_int(variable_name="strips_per_rack",
                       display_name="strips per rack",
                       description="How many strips do you want in each strip_rack?",
                       default=6,
                       minimum=1,
                       maximum=6,
                       unit="strips")
    
    #### Starting tips
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
    
    parameters.add_bool(variable_name="lights_on",
                        display_name="lights on",
                        description="Do you want the lights turned ON?",
                        default=False)
    parameters.add_bool(variable_name="pause",
                        display_name="pause after mix",
                        description="Do you want to pause after adding mix, before adding primers?",
                        default=False)   
    
def run(protocol: protocol_api.ProtocolContext):
    plankton = protocol.params
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    #### Location of primer strips in racks
    possible_primer_locations = {
        1:['6'],
        2:['3','9'],
        3:['2','7','11'],
        4:['2','5','8','11'],
        5:['1', '3', '6','9','12'],
        6:['1','3','5','7','9','11']
        }
    primer_loc = possible_primer_locations[plankton.strips_per_rack]    
    ## How many tube_strip_racks are needed
    primer_per_rack = 8 * len(primer_loc)
    number_of_primer_racks = math.ceil(plankton.number_of_barcodes / primer_per_rack)
    
    #### Starting tips
    starting_tip_p20_row = plankton.starting_tip_p20_row
    starting_tip_p20_column = plankton.starting_tip_p20_column.strip('this_is_not_an_int')
    starting_tip_p20 = starting_tip_p20_row + starting_tip_p20_column
   
    starting_tip_p300_row = plankton.starting_tip_p300_row
    starting_tip_p300_column = plankton.starting_tip_p300_column.strip('this_is_not_an_int')
    starting_tip_p300 = starting_tip_p300_row + starting_tip_p300_column    
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    protocol.comment('Put your primer strips in the following columns:' +
                      f'{primer_loc}')
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(plankton.lights_on)
## ============================================================================    

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### PIPETTE TIPS
    tips_mastermix = LW.amount_of_tips(plankton.mastermix_volume,
                                       plankton.number_of_barcodes,
                                       16,
                                       19)
    tips_barcodes = LW.amount_of_tips(plankton.primer_vol,
                                       plankton.number_of_barcodes * 2,
                                       1,
                                       15)
    amount_tips_20 = tips_mastermix[0] + tips_barcodes[0]
    amount_tips_300 = tips_mastermix[1] + tips_barcodes[1]
    
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               amount_tips_20)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip_p300,
                                                 amount_tips_300)

    tips_20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'opentrons_20uL',
                              amount = tip_racks_p20,
                              deck_positions = [7,10,11,8],
                              protocol = protocol)
    tips_300 = LW.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               amount = tip_racks_p300,
                               deck_positions = [8,11,10,7],
                               protocol = protocol)
    #### PIPETTES       
    p20, p300 = LW.loading_pipettes(P20,
                                    tips_20,
                                    starting_tip_p20,
                                    P300, 
                                    tips_300,
                                    starting_tip_p300,
                                    protocol)
    
    #### LABWARE
    ## MASTERMIX
    # Decide what tube type you need for the mastermix
    reagent_tube_type, number_of_tubes, max_volume = LW.which_tube_type(
        total_volume = plankton.total_mastermix_volume,
        tube_type = False)
    
    # Load mastermix tube
    mastermix_racks = LW.loading_tube_racks(simulate = simulate,
                                            tube_type = reagent_tube_type,
                                            reagent_type = 'Mastermix',
                                            amount = 1,
                                            deck_positions = [9],
                                            protocol = protocol)
    
    ## Specific location of mastermix
    mastermix_tube = LW.tube_locations(source_racks = mastermix_racks,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = number_of_tubes)
    
    ## PRIMERS
    # Loading forward primers
    forward_racks = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = 'PCR_strips',
                                         reagent_type = 'forward_primers',
                                         amount = number_of_primer_racks,
                                         deck_positions = [1,4],
                                         protocol = protocol)
    # Specific location of the forward primers
    forward_tubes = LW.tube_locations(source_racks = forward_racks,
                                      specific_columns = primer_loc,
                                      skip_wells = False,
                                      number_of_tubes = plankton.number_of_barcodes)
    
    # Loading reverse primers
    reverse_racks = LW.loading_tube_racks(simulate = simulate,
                                          tube_type = 'PCR_strips',
                                          reagent_type = 'reverse_primers',
                                          amount = number_of_primer_racks,
                                          deck_positions = [3,6],
                                          protocol = protocol)
    
    # Specific location of the forward primers
    reverse_tubes = LW.tube_locations(source_racks = reverse_racks,
                                     specific_columns = primer_loc,
                                     skip_wells = False,
                                     number_of_tubes = plankton.number_of_barcodes)
    
    ## Destination plate
    PCR_plate = LW.loading_tube_racks(simulate = simulate,
                                      tube_type = 'plate_96_NIOZholder',
                                      reagent_type = 'PCR-plate',
                                      amount = 1,
                                      deck_positions = [5],
                                      protocol = protocol)
    # Mastermix destinations
    mastermix_destinations = LW.tube_locations(source_racks = PCR_plate,
                                               specific_columns = False,
                                               skip_wells = False,
                                               number_of_tubes = plankton.number_of_barcodes)
    # Primer destinations

    
    
    
    
# =============================================================================



    
    