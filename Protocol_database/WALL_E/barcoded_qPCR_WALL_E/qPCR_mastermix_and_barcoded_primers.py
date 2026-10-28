# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
simulate = False
#### Import opentrons protocol API v2
from opentrons import protocol_api
#### Import math 
import math ## To do some calculations
#### Import itertools, to flatten list of lists
import itertools
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
            'protocolName': 'Barcoded qPCR preperation V1.2',
            'description': 'Aliquoting mastermix for samples, standard series and standard sample and barcoded primers.'}
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
                       default=64,
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
    #### Standard dilution series & standard sample
    parameters.add_int(variable_name="number_of_std_series",
                       display_name="How many standard series?",
                       description="Replicates of the dilution standard serie",
                       default=3,
                       minimum=0,
                       maximum=4,
                       unit="replicates")
    parameters.add_int(variable_name="length_std_series",
                       display_name="How many dilutions per series?",
                       description="How many different dilutions do you have in your standard series?",
                       default=8,
                       minimum=1,
                       maximum=8,
                       unit="reactions")
    parameters.add_int(variable_name="number_of_std_samples",
                       display_name="Number of std samples",
                       description="Number of replicates of the standard sample",
                       default=6,
                       minimum=0,
                       maximum=6,
                       unit="replicates")
    parameters.add_bool(variable_name="standards_unique_barcodes",
                        display_name="standards unique barcodes",
                        description="Do you want the standard series and standard samples to get unique barcodes?",
                        default=False)
    #### Barcodes
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
    
    #### Starting tips
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
    
    parameters.add_bool(variable_name="pause",
                        display_name="pause after mix",
                        description="Do you want to pause after adding mix, before adding primers?",
                        default=False)   
    
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

# CALCULATED VARIABLES=========================================================
# =============================================================================
    # Calculates the total reaction amount to check if it fits on 1 plate    
    total_reactions = (plankton.number_of_samples +
                       plankton.number_of_Mocks +
                       plankton.number_of_NTCs +
                       (plankton.number_of_std_series * plankton.length_std_series) +
                       plankton.number_of_std_samples)
    if total_reactions > 96:
        raise Exception(f'You have {total_reactions} reactions. ' +
                        'This is more than what fits in a plate.')
    
    # Calculate the number of unique barcodes needed:
    if plankton.standards_unique_barcodes:
        number_of_barcodes = total_reactions
    else:
        number_of_barcodes = (plankton.number_of_samples +
                              plankton.number_of_Mocks +
                              plankton.number_of_NTCs)  
    
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

# LIGHTS=======================================================================
# =============================================================================
# If for any reason the lights are on at the start, turn them off
    protocol.set_rail_lights(False)
# =============================================================================    

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### PIPETTE TIPS
    # Calculates how many tip racks per size are needed and set pipettes to true or false    
    tip_racks_p20, tip_racks_p300, P20, P300 = LW.number_of_tip_racks_2_0(volumes_aliquoting = plankton.mastermix_volume,
                                                                          number_of_aliquotes = total_reactions,
                                                                          volumes_transfering = plankton.primer_vol,
                                                                          number_of_transfers = total_reactions * 2,
                                                                          starting_tip_p20 = starting_tip_p20,
                                                                          starting_tip_p300 = starting_tip_p300)
    # oading tip racks
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
                                       number_of_tubes = number_of_tubes,
                                       reagent_type = 'mastermix',
                                       volume = plankton.total_mastermix_volume,
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
                                      number_of_tubes = 96,
                                      reagent_type = 'forward_primer',
                                      volume = plankton.primer_vol/number_of_barcodes,
                                      protocol = protocol)
    # Creating Forward primer list, based on skipped primers
    from_starting_F_primer_to_end = forward_tubes[slice(plankton.skipped_forward_barcodes, 96)]
    from_start_to_starting_F_primer = forward_tubes[slice(0,plankton.skipped_forward_barcodes)]
    F_primers = from_starting_F_primer_to_end + from_start_to_starting_F_primer
    F_primer_wells = F_primers[:number_of_barcodes]
    
    # Loading reverse primers
    reverse_racks = LW.loading_tube_racks(simulate = simulate,
                                          tube_type = 'PCR_strips',
                                          reagent_type = 'reverse_primers',
                                          amount = number_of_primer_racks,
                                          deck_positions = [3,6],
                                          protocol = protocol)    
    # Specific location of the reverse primers
    reverse_tubes = LW.tube_locations(source_racks = reverse_racks,
                                     specific_columns = primer_loc,
                                     skip_wells = False,
                                     number_of_tubes = 96,
                                     reagent_type = 'reverse_primer',
                                     volume = plankton.primer_vol/number_of_barcodes,
                                     protocol = protocol)
    # Creating Reverse primer list, based on skipped primers
    from_starting_R_primer_to_end = reverse_tubes[slice(plankton.skipped_reverse_barcodes, 96)]
    from_start_to_starting_R_primer = reverse_tubes[slice(0,plankton.skipped_reverse_barcodes)]
    R_primers = from_starting_R_primer_to_end + from_start_to_starting_R_primer
    R_primer_wells = R_primers[:number_of_barcodes]
    
    # Give starting primers a distinctive color
    start_primer = protocol.define_liquid(
        name= "start primer",
        description = "The primer that is assigned to the first sample",
        display_color = "#C70039")
    F_primers[0].load_liquid(liquid=start_primer, volume = 30)
    R_primers[0].load_liquid(liquid=start_primer, volume = 30)
    
    ## Primer stock for standard series and standard sample
    if not plankton.standards_unique_barcodes:
        primer_stock_rack = LW.loading_tube_racks(simulate = simulate,
                                                  tube_type = '1.5mL_tubes',
                                                  reagent_type = 'primer_stock',
                                                  amount = 1,
                                                  deck_positions = [2],
                                                  protocol = protocol)
        forward_stock = LW.tube_locations(source_racks = primer_stock_rack,
                                          specific_columns = ['1'],
                                          skip_wells = False,
                                          number_of_tubes = 1,
                                          reagent_type = 'forward_primer',
                                          volume = 50,
                                          protocol = protocol)
        
        reverse_stock = LW.tube_locations(source_racks = primer_stock_rack,
                                          specific_columns = ['1'],
                                          skip_wells = [0],
                                          number_of_tubes = 1,
                                          reagent_type = 'reverse_primer',
                                          volume = 50,
                                          protocol = protocol)
    
        protocol.comment('Forward primer for std and/or stdseries should go '+
                         f'into {forward_stock}.\n'+
                         'Reverse primer for std and/or stdseries should go '+
                         f'into {reverse_stock}\n')
    
    ## Destination plate
    qPCR_plate = LW.loading_tube_racks(simulate = simulate,
                                      tube_type = 'plate_96_NIOZholder',
                                      reagent_type = 'PCR-plate',
                                      amount = 1,
                                      deck_positions = [5],
                                      protocol = protocol)
    
    # Destinations on the PCR plate
    sample_destination = LW.multiple_reagent_tube_locations(source_racks = qPCR_plate,
                                                               specific_columns = False,
                                                               skip_wells = False,
                                                               reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'Mock': plankton.number_of_Mocks, 'NTC': plankton.number_of_NTCs, 'standard_samples': plankton.number_of_std_samples},
                                                               volume = (plankton.mastermix_volume + (plankton.primer_vol *2))/number_of_barcodes + 5,
                                                               protocol = protocol)
    sample_destination = list(itertools.chain(*sample_destination))
    
    stdseries_dest = []
    if plankton.number_of_std_series > 0:
        specific_qPCR_columns = ['12','11','10','9']        
        for i in range(plankton.number_of_std_series):
            column = []
            column.append(specific_qPCR_columns[i])
            destination = LW.tube_locations(source_racks = qPCR_plate,
                                                specific_columns = column,
                                                skip_wells = False,
                                                number_of_tubes = plankton.length_std_series,
                                                reagent_type = 'dilution_series',
                                                volume = plankton.mastermix_volume,
                                                protocol = protocol)
            stdseries_dest = stdseries_dest + destination
    
    # Destinations on the PCR plate where unique barcodes should go:
    if plankton.standards_unique_barcodes:
        unique_primer_dest = sample_destination + stdseries_dest
    else:
        unique_primer_dest = sample_destination[:number_of_barcodes]
        stock_primer_dest = sample_destination[number_of_barcodes:] + stdseries_dest              
        
        # Make a list of len(stock_primer_dest) length with the stock tubes
        forward_stocks = []
        reverse_stocks = []
        for i in range(len(stock_primer_dest)):
            forward_stocks.append(forward_stock[0])
            reverse_stocks.append(reverse_stock[0])
            
# =============================================================================

# THE ACTUAL PIPETTING=========================================================
# =============================================================================
    #### MasterMix
    PM.aliquoting_reagent(reagent_source = mastermix_tube,
                          reagent_tube_type = reagent_tube_type,
                          reagent_startvolume = plankton.total_mastermix_volume,
                          aliquot_volume = plankton.mastermix_volume,
                          destination_wells = sample_destination + stdseries_dest,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'continue_at_bottom',
                          pause = plankton.pause,
                          protocol = protocol)
    
    if plankton.pause:
        protocol.pause("Please insert the primers and then continue")
        
    #### Transferring unique barcodes
    ## Forward primers
    PM.transferring_reagents(source_wells = F_primer_wells,
                              destination_wells = unique_primer_dest,
                              transfer_volume = plankton.primer_vol,
                              airgap = True,
                              mix = True,
                              p20 = p20,
                              p300 = p300,
                              protocol = protocol)
    ## Reverse primers
    PM.transferring_reagents(source_wells = R_primer_wells,
                              destination_wells = unique_primer_dest,
                              transfer_volume = plankton.primer_vol,
                              airgap = True,
                              mix = True,
                              p20 = p20,
                              p300 = p300,
                              protocol = protocol)
    
    #### Transferring single barcode to standards
    if not plankton.standards_unique_barcodes:
        ## Forward
        PM.transferring_reagents(source_wells = forward_stocks,
                                  destination_wells = stock_primer_dest,
                                  transfer_volume = plankton.primer_vol,
                                  airgap = True,
                                  mix = True,
                                  p20 = p20,
                                  p300 = p300,
                                  protocol = protocol)
        
        ## Reverse
        PM.transferring_reagents(source_wells = reverse_stocks,
                                  destination_wells = stock_primer_dest,
                                  transfer_volume = plankton.primer_vol,
                                  airgap = True,
                                  mix = True,
                                  p20 = p20,
                                  p300 = p300,
                                  protocol = protocol)    
# =============================================================================

# LIGHTS OFF===================================================================
# =============================================================================
    protocol.set_rail_lights(False)
# =============================================================================