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
metadata = {
            'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Barcoded qPCR preperation V1.0',
            'description': 'Aliquoting the qPCR mastermix and the barcoded primers.'
            }
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Mastermix & primers
    # Mastermix
    parameters.add_int(variable_name="total_mastermix_volume",
                       display_name="total mastermix volume",
                       description="How much volume is in your mastermix tube?",
                       default=3000,
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
    # Primers
    parameters.add_float(variable_name="primer_vol",
                       display_name="primer volume",
                       description="How much (µL) should be added of each primer?",
                       default=1.5,
                       minimum=0.0,
                       maximum=5.0,
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
    
    #### Samples
    # Samples & PCR controls
    parameters.add_int(variable_name="number_of_samples",
                       display_name="How many samples do you have?",
                       description="Number of samples including extraction controls, excluding PCR controls, standard samples and dilution series.",
                       default=65,
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
    # Standard dilution series & standard sample
    parameters.add_int(variable_name="number_of_std_series",
                       display_name="How many dilution standard series do you have?",
                       description="Replicates of the dilution standard serie",
                       default=3,
                       minimum=0,
                       maximum=4,
                       unit="dilution series")
    parameters.add_int(variable_name="length_std_series",
                       display_name="What is the length of the standard dilution serie?",
                       description="length of the dilution standard serie",
                       default=8,
                       minimum=1,
                       maximum=8,
                       unit="reactions")
    parameters.add_int(variable_name="number_of_std_samples",
                       display_name="Number of std samples",
                       description="Number of replicates of the standard sample",
                       default=6,
                       minimum=1,
                       maximum=6,
                       unit="replicates")
    
    #### Barcodes for standard dilution series and standard sample
    parameters.add_bool(variable_name="stdseries_unique_barcodes",
                        display_name="stdseries unique barcodes",
                        description="Should each dilution series get a unique barcode?",
                        default=False)
    parameters.add_bool(variable_name="std_unique_barcodes",
                        display_name="std unique barcodes",
                        description="Should the standard samples each get unique barcodes?",
                        default=False)
    
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
    # Checking if the row is F
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

# CALCULATED VARIABLES=========================================================
# =============================================================================
    # Calculates the total reaction amount to check if it fits on 1 plate
    total_reactions = (plankton.number_of_samples +
                       plankton.number_of_Mocks +
                       plankton.number_of_NTCs +
                       (plankton.number_of_std_series *8) +
                       plankton.number_of_std_samples)
    if total_reactions > 96:
        raise Exception(f'You have {total_reactions} reactions. ' +
                        'This is more than 96 reactions and not possible.')
    else:
        protocol.comment(f'You have {total_reactions} reactions.')
        
    # Determines how many unique primers you need
    total_unique_primers = (plankton.number_of_samples + plankton.number_of_Mocks +
                            plankton.number_of_NTCs)
    
    if plankton.stdseries_unique_barcodes == True and plankton.std_unique_barcodes == False:
        total_unique_primers += plankton.number_of_std_series + 1
    
    elif plankton.stdseries_unique_barcodes == False and plankton.std_unique_barcodes == True:
        total_unique_primers += plankton.number_of_std_samples + 1
    
    elif plankton.stdseries_unique_barcodes == True and plankton.std_unique_barcodes == True:
        total_unique_primers += plankton.number_of_std_samples + plankton.number_of_std_series
    
    else:
        total_unique_primers += 1
# =============================================================================

# LIGHTS=======================================================================
# =============================================================================
# If for any reason the lights are on at the start, turn them off
    protocol.set_rail_lights(False)
# =============================================================================
    # Calculates how many tip racks per size are needed and sets pipette true or false    
    tip_racks_p20, tip_racks_p300, P20, P300 = LW.number_of_tip_racks_2_0(volumes_aliquoting = plankton.mastermix_volume,
                                                                          number_of_aliquotes = total_reactions,
                                                                          volumes_transfering = plankton.primer_vol,
                                                                          number_of_transfers = total_reactions,
                                                                          starting_tip_p20 = starting_tip_p20,
                                                                          starting_tip_p300 = starting_tip_p300)
    # loading tipracks
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