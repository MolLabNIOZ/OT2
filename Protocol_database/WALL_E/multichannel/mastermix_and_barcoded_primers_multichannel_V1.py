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
            'protocolName': 'mastermix and barcoded primers with multichannel V1',
            'description': 'aliquoting mix and distributing barcoded primers'}
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Mastermix
    parameters.add_int(variable_name="total_mastermix_volume",
                       display_name="total mastermix volume",
                       description="How much volume is in your mastermix tube?",
                       default=2000,
                       minimum=0,
                       maximum=5000,
                       unit="µL MM")
    parameters.add_float(variable_name="mastermix_volume",
                       display_name="mastermix volume per reaction",
                       description="How much mastermix should each reaction get?",
                       default=20.0,
                       minimum=0.0,
                       maximum=50.0,
                       unit="µL MM")
    #### Samples
    parameters.add_int(variable_name="number_of_samples",
                       display_name="How many samples do you have?",
                       description="Number of samples including extraction controls, excluding PCR controls.",
                       default=94,
                       minimum=0,
                       maximum=95,
                       unit="samples")
    parameters.add_int(variable_name="number_of_Mocks",
                       display_name="Do you want to include a Mock?",
                       description="",
                       default=1,
                       minimum=0,
                       maximum=1,
                       unit="Mock(s)")
    parameters.add_int(variable_name="number_of_NTCs",
                       display_name="How many NTCs do you want?",
                       description="",
                       default=1,
                       minimum=1,
                       maximum=5,
                       unit="NTCs")
    #### Barcodes
    parameters.add_float(variable_name="primer_vol",
                       display_name="primer volume",
                       description="How much (µL) should be added of each primer?",
                       default=1.5,
                       minimum=0.0,
                       maximum=5.0,
                       unit="µL primer")    
    parameters.add_int(variable_name="revere_skip_strips",
                       display_name="reverses strips to skip",
                       description="How many reverse barcodes should WALL-E skip?",
                       default=0,
                       minimum=0,
                       maximum=11,
                       unit="strips")
    
    #### Starting tips   
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
    
    parameters.add_bool(variable_name="lights_on",
                        display_name="lights on",
                        description="Do you want the lights turned ON?",
                        default=True)
    parameters.add_bool(variable_name="pause",
                        display_name="pause after adding mix",
                        description="Do you want to pause after adding mix, before adding primers?",
                        default=False)   
def run(protocol: protocol_api.ProtocolContext):
    plankton = protocol.params
    
# =============================================================================

## CONVERTING VARIABLES========================================================
## ============================================================================
    #### Starting tips  
    # Combining the row-variable with the column-variable to create starting tip
    starting_tip_p20 = "A1"
    starting_tip_p300 = plankton.starting_tip_p300_row + str(plankton.starting_tip_p300_column)
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
    number_of_barcodes = plankton.number_of_samples + plankton.number_of_Mocks + plankton.number_of_NTCs
    # For multichannel, fill up with NTCs untill full columns of 8
    half_column_tubes = number_of_barcodes % 8
    extra_tubes = 0
    if half_column_tubes > 0:
        extra_tubes = 8 - half_column_tubes
        number_of_barcodes += extra_tubes
        protocol.comment(f"{extra_tubes} extra NTCs are added to fill up to entire columns. "
                         "This is necesarry to accomodate the multichannel pipette")
    # Check if it fits a plate
    if number_of_barcodes > 96:
        raise Exception(f'You have {number_of_barcodes} reactions. ' +
                        'The max is 96. So please change the amount of samples')
    
    #### Location of primer strips in racks
    possible_primer_locations = {
        1:['6'],
        2:['3','9'],
        3:['2','7','11'],
        4:['2','5','8','11'],
        5:['1','3','6','9','12'],
        6:['1','3','5','7','9','11']
        }    
    primer_loc = possible_primer_locations[math.ceil(number_of_barcodes/8/2)]    
    ## How many tube_strip_racks are needed
    primer_per_rack = 8 * len(primer_loc)
    number_of_primer_racks = math.ceil(number_of_barcodes / primer_per_rack)
# =============================================================================

# COMMENTS=====================================================================
# =============================================================================
    protocol.comment("Put your primer strips in the following columns"
                     f"{primer_loc}")
# =============================================================================

# LIGHTS ON====================================================================
# =============================================================================
    protocol.set_rail_lights(plankton.lights_on)
# =============================================================================    

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### PIPETTE TIPS
    tips_mastermix = LW.amount_of_tips(plankton.mastermix_volume,
                                       number_of_barcodes,
                                       16,
                                       19)
    tips_barcodes = LW.amount_of_tips(plankton.primer_vol,
                                       number_of_barcodes * 2 + 7, # added 7 to compensate for incomplete columns of tips, for the multichannel
                                       1,
                                       15)
    amount_tips_20 = tips_mastermix[0] + tips_barcodes[0]
    amount_tips_300 = tips_mastermix[1] + tips_barcodes[1]
    
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               amount_tips_20)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip_p300,
                                                 amount_tips_300)

    tips_20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'tipone_20uL',
                              amount = tip_racks_p20,
                              deck_positions = [7,10,11,8],
                              protocol = protocol)
    tips_300 = LW.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               amount = tip_racks_p300,
                               deck_positions = [8,11,10,7],
                               protocol = protocol)
    #### PIPETTES
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
    #### LABWARE 
    ## MASTERMIX
    # Decide what tube type you need for the mastermix
    if plankton.total_mastermix_volume > 1500 and plankton.mastermix_volume <= 19:
        mm_tube_type = '1.5mL_tubes'
    else:
        mm_tube_type = False
    reagent_tube_type, number_of_tubes, max_volume = LW.which_tube_type(
        total_volume = plankton.total_mastermix_volume,
        tube_type = mm_tube_type)

    # Load mastermix tube
    mastermix_racks = LW.loading_tube_racks(simulate = simulate,
                                            tube_type = reagent_tube_type,
                                            reagent_type = 'Mastermix',
                                            amount = 1,
                                            deck_positions = [9],
                                            protocol = protocol)
    
    ## Specific location of mastermix
    mm_volume_per_tube = plankton.total_mastermix_volume / number_of_tubes
    mastermix_tube = LW.tube_locations(source_racks = mastermix_racks,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = number_of_tubes,
                                       reagent_type = 'mastermix',
                                       volume = mm_volume_per_tube,
                                       protocol = protocol) 
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
                                      number_of_tubes = number_of_barcodes,
                                      reagent_type = 'forward_primer',
                                      volume = plankton.primer_vol/number_of_barcodes,
                                      protocol = protocol)
    F_primer_wells = forward_tubes

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
                                     number_of_tubes = number_of_barcodes,
                                     reagent_type = 'reverse_primer',
                                     volume = plankton.primer_vol/number_of_barcodes,
                                     protocol = protocol)
    # Creating Reverse primer list, based on skipped primers
    from_starting_R_primer_to_end = reverse_tubes[slice(plankton.revere_skip_strips * 8, number_of_barcodes)]
    from_start_to_starting_R_primer = reverse_tubes[slice(0,plankton.revere_skip_strips*8)]
    R_primers = from_starting_R_primer_to_end + from_start_to_starting_R_primer
    R_primer_wells = R_primers[:number_of_barcodes]
    
    # Give starting primers a distinctive color
    start_primer = protocol.define_liquid(
        name= "start primer",
        description = "The primer that is assigned to the first sample",
        display_color = "#C70039")
    F_primer_wells[0].load_liquid(liquid=start_primer, volume = 30)
    R_primer_wells[0].load_liquid(liquid=start_primer, volume = 30)
    
    ## Destination plate
    PCR_plate = LW.loading_tube_racks(simulate = simulate,
                                      tube_type = 'plate_96_NIOZholder',
                                      reagent_type = 'PCR-plate',
                                      amount = 1,
                                      deck_positions = [5],
                                      protocol = protocol)
    # Mastermix destinations
    PCR_plate_destination = LW.multiple_reagent_tube_locations(source_racks = PCR_plate,
                                                               specific_columns = False,
                                                               skip_wells = False,
                                                               reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'Mock': plankton.number_of_Mocks, 'NTC': plankton.number_of_NTCs + extra_tubes},
                                                               volume = (plankton.mastermix_volume + (plankton.primer_vol *2))/number_of_barcodes + 5,
                                                               protocol = protocol)
# =============================================================================

# THE ACTUAL PIPETTING=========================================================
# =============================================================================   
    left_pipette.reset_tipracks()
    left_pipette.configure_nozzle_layout(style=protocol_api.SINGLE, start='A1', tip_racks=tips_20)      

#### MasterMix
    if number_of_tubes > 1:
        action_at_bottom = 'next_tube'
    else:
        action_at_bottom = 'continue_at_bottom'
    PM.aliquoting_reagent(reagent_source = mastermix_tube,
                          reagent_tube_type = reagent_tube_type,
                          reagent_startvolume = (number_of_barcodes/len(mastermix_tube)) * plankton.mastermix_volume,
                          aliquot_volume = plankton.mastermix_volume,
                          destination_wells = PCR_plate_destination[0]+PCR_plate_destination[1]+PCR_plate_destination[2],
                          p20 = left_pipette,
                          p300 = right_pipette,
                          action_at_bottom = action_at_bottom,
                          pause = plankton.pause,
                          protocol = protocol)

    if plankton.pause:
        protocol.pause("Please insert the primers and then continue")

#### Primers    
    #### Forward primers
    PM.transferring_reagents_multichannel(source_wells = F_primer_wells,
                                          destination_wells = PCR_plate_destination[0]+PCR_plate_destination[1]+PCR_plate_destination[2],
                                          transfer_volume = plankton.primer_vol,
                                          airgap = True,
                                          mix = True,
                                          p20 = left_pipette,
                                          tips_20 = tips_20,
                                          p300 = right_pipette,
                                          tips_300 = tips_300,
                                          protocol = protocol)
    #### Reverse primers
    PM.transferring_reagents_multichannel(source_wells = R_primer_wells,
                                          destination_wells = PCR_plate_destination[0]+PCR_plate_destination[1]+PCR_plate_destination[2],
                                          transfer_volume = plankton.primer_vol,
                                          airgap = True,
                                          mix = True,
                                          p20 = left_pipette,
                                          tips_20 = tips_20,
                                          p300 = right_pipette,
                                          tips_300 = tips_300,
                                          protocol = protocol)  

# =============================================================================

# LIGHTS OFF===================================================================
# =============================================================================
    protocol.set_rail_lights(False)
# =============================================================================
        