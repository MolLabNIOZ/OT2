"""
WALL-E protocol for barcoded qPCRs
Samples will get unique barcodes
Standard sample replicates will all get the same barcode
Dilution series will get either all the same barcode or the same within series, 
but unique among series
"""
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
            'protocolName': 'Barcoded qPCR preperation V0.1',
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
    parameters.add_int(variable_name="number_of_samples",
                       display_name="How many samples do you have?",
                       description="Number of samples including extraction controls, excluding PCR controls, standard samples and dilution series.",
                       default=65,
                       minimum=0,
                       maximum=95,
                       unit="samples")
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
# =============================================================================
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):
    plankton = protocol.params
    #### Starting tips
    #Wwhat is the well of the first tipboxes for eithe p20 and p300 tips
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
        
    #### MASTERMIX
    # What is the total startvolume (µL) of your mastermix?
    total_mastermix_volume = plankton.total_mastermix_volume
    # What is the volume (µL) of mastermix that needs to be aliquoted per reaction?
    mastermix_volume = plankton.mastermix_volume
    
    #### SAMPLES
    # How many samples do you want to include?
    number_of_samples = plankton.number_of_samples     ##!!! NOTE: include in this number the mock too
    # Which specific wells (index) do you want to skip? Leave empty if you do not want to skip
    skipped_wells = []  
    # How many NTCs to include 
    number_of_NTCs = plankton.number_of_NTCs
    
    ####STANDARDS
    # How many dilution serie replicates do you want to include?
    number_of_std_series = plankton.number_of_std_series 
      ## If none -- fill in 0
    # How many dilutions are in the standard dilution series?
    length_std_series = plankton.length_std_series  ## length_of_std_series  MAX == 8                                     
    # How many replicates of the standard sample do you want?
    number_of_std_samples = plankton.number_of_std_samples 
    
    #### PRIMERS
    # In what columns of the rack are the strips located? 
    primer_loc = ['1', '3', '5', '7', '9', '11']  ## max 2 racks with strips
    # What is the volume (µL) of each primer that needs to be added to the mix?
    primer_vol = plankton.primer_vol
    # How many primers should WALL-E skip, or index of first_primer?
    skipped_F_primers = plankton.skipped_forward_barcodes
    skipped_R_primers = plankton.skipped_reverse_barcodes
    # Should the standard samples each get unique barcodes?
    std_unique_barcodes = plankton.std_unique_barcodes
    # Should each dilution series get a unique barcode?
    stdseries_unique_barcodes = plankton.stdseries_unique_barcodes
    
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
    # If a standard sample is taken, add 1 to the total number of samples
    if number_of_std_samples >= 1:
        total_number_of_samples = number_of_samples + 1     
    else:
        total_number_of_samples = number_of_samples
    
    # Check if everything fits on a plate
    total_reactions = (number_of_samples + 
                       number_of_std_samples + 
                       number_of_NTCs + 
                       (number_of_std_series*8))
    if total_reactions > 96:
        raise Exception(f'You have {total_reactions} reactions. ' +
                        'This is more than 96 reactions and not possible.')
    # Check how many unique primers are needed
    total_unique_primers = number_of_samples + number_of_NTCs
    if std_unique_barcodes:
        total_unique_primers += number_of_std_samples     

# =============================================================================

# LIGHTS=======================================================================
# =============================================================================
# If for any reason the lights are on at the start, turn them off
    protocol.set_rail_lights(False)
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
#### PIPETTE TIPS
    p20_tips_total = 0
    p300_tips_total = 0
    
    # tips needed for MM
    p20_tips_needed, p300_tips_needed = LW.amount_of_tips(mastermix_volume,
                                                          total_reactions,
                                                          16,
                                                          19)
    p20_tips_total += p20_tips_needed
    p300_tips_total += p300_tips_needed
    
    # tips needed for primers
    p20_tips_needed, p300_tips_needed = LW.amount_of_tips(primer_vol,
                                                          total_reactions*2,
                                                          1,
                                                          19)
    p20_tips_total += p20_tips_needed
    p300_tips_total += p300_tips_needed
    
    # racks needed
    p20_tip_racks, P20 = LW.number_of_tipracks(starting_tip_p20, p20_tips_total)
    p300_tip_racks, P300 = LW.number_of_tipracks(starting_tip_p300, p300_tips_total)
    
    print(p20_tip_racks)
    print(p300_tip_racks)
    
    # loading tipracks
    tips_20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'tipone_20uL',
                              amount = p20_tip_racks,
                              deck_positions = [7,10,11,8],
                              protocol = protocol)
    tips_300 = LW.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               amount = p300_tip_racks,
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
    ### MASTERMIX
    # What kind of tube
    reagent_tube_type, number_of_tubes, max_volume = LW.which_tube_type(total_volume = total_mastermix_volume,
                                                                    tube_type = False)
    # Loading the rack
    mastermix_rack = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = reagent_tube_type,
                                           reagent_type = 'Mastermix',
                                           amount = 1,
                                           deck_positions = [9],
                                           protocol = protocol)
    # Identify specific tube location
    MasterMix = LW.tube_locations(source_racks = mastermix_rack,
                                  specific_columns = False,
                                  skip_wells = False,
                                  number_of_tubes = 1,
                                  reagent_type = 'mastermix',
                                  volume = total_mastermix_volume,
                                  protocol = protocol)

    ### PRIMERS
    # forward primer set
    forward_racks = LW.loading_tube_racks(simulate = simulate,
                                          tube_type = 'PCR_strips',
                                          reagent_type = 'forward_primers',
                                          amount = math.ceil(total_unique_primers/(8 * len(primer_loc))),
                                          deck_positions = [1,4],
                                          protocol = protocol)
    forward_tubes = LW.tube_locations(source_racks = forward_racks,
                                      specific_columns = primer_loc,
                                      skip_wells = skipped_wells,
                                      number_of_tubes = total_unique_primers,
                                      reagent_type = 'forward_primer',
                                      volume = primer_vol/total_unique_primers,
                                      protocol = protocol)
    # reverse primer set
    reverse_racks = LW.loading_tube_racks(simulate = simulate,
                                          tube_type = 'PCR_strips',
                                          reagent_type = 'reverse_primers',
                                          amount = math.ceil(total_unique_primers/(8 * len(primer_loc))),
                                          deck_positions = [3,6],
                                          protocol = protocol)
    
    reverse_tubes = LW.tube_locations(source_racks = reverse_racks,
                                      specific_columns = primer_loc,
                                      skip_wells = skipped_wells,
                                      number_of_tubes = total_unique_primers,
                                      reagent_type = 'reverse_primer',
                                      volume = primer_vol/total_unique_primers,
                                      protocol = protocol)
    # primers for standard and dilution series
    primer_stock_rack = LW.loading_tube_racks(simulate = simulate,
                                              tube_type = '1.5mL_tubes',
                                              reagent_type = 'primer_stock',
                                              amount = 1,
                                              deck_positions = [2],
                                              protocol = protocol)
    if not stdseries_unique_barcodes:
        forward_stock = LW.tube_locations(source_racks = primer_stock_rack,
                                          specific_columns = ['1'],
                                          skip_wells = False,
                                          number_of_tubes = 1,
                                          reagent_type = 'forward_primer',
                                          volume = primer_vol,
                                          protocol = protocol)
        reverse_stock = LW.tube_locations(source_racks = primer_stock_rack,
                                          specific_columns = ['1'],
                                          skip_wells = [0],
                                          number_of_tubes = 1,
                                          reagent_type = 'reverse_primer',
                                          volume = primer_vol,
                                          protocol = protocol)
    else:
        forward_stock = LW.tube_locations(source_racks = primer_stock_rack,
                                          specific_columns = ['1'],
                                          skip_wells = False,
                                          number_of_tubes = number_of_std_series,
                                          reagent_type = 'forward_primer',
                                          volume = primer_vol,
                                          protocol = protocol)
        reverse_stock = LW.tube_locations(source_racks = primer_stock_rack,
                                          specific_columns = ['6'],
                                          skip_wells = False,
                                          number_of_tubes = number_of_std_series,
                                          reagent_type = 'reverse_primer',
                                          volume = primer_vol,
                                          protocol = protocol)

    protocol.comment('Forward primer for std and/or stdseries should go into '+
                     f'{forward_stock}.\n'+
                     'Reverse primer for std and/or stdseries should go into '+
                     f'{reverse_stock}\n')

    ### PCR_PLATE
    qPCR_plate = LW.loading_tube_racks(simulate = simulate,
                                      tube_type = 'plate_96_NIOZholder',
                                      reagent_type = 'PCR-plate',
                                      amount = 1,
                                      deck_positions = [5],
                                      protocol = protocol)
# =============================================================================

# DESTINATION LOCATIONS========================================================
# =============================================================================
#### MASTERMIX    
    sample_std_dest = LW.tube_locations(source_racks = qPCR_plate,
                                        specific_columns = False,
                                        skip_wells = skipped_wells,
                                        number_of_tubes = number_of_samples + 
                                                          number_of_std_samples + 
                                                          number_of_NTCs,
                                        reagent_type = 'standard_samples',
                                        volume = 10,
                                        protocol = protocol)
    
    if number_of_std_series > 0:
        specific_qPCR_columns = ['12','11','10','9','8','7','6','5','4','3','2','1']
        stdseries_dest = []        
        for i in range(number_of_std_series):
            column = []
            column.append(specific_qPCR_columns[i])
            destination = LW.tube_locations(source_racks = qPCR_plate,
                                                specific_columns = column,
                                                skip_wells = False,
                                                number_of_tubes = length_std_series,
                                                reagent_type = 'dilution_series',
                                                volume = 10,
                                                protocol = protocol)
            stdseries_dest = stdseries_dest + destination
    
   
    
    
    if number_of_std_samples > 0 and not std_unique_barcodes:
        std_primer_destination = sample_std_dest[total_unique_primers:total_unique_primers + number_of_std_samples]
        unique_primer_dest = sample_std_dest[:total_unique_primers]
    else:
        unique_primer_dest = sample_std_dest
         
# =============================================================================    
    
# THE ACTUAL PIPETTING ========================================================
# =============================================================================
#### Aliquoting mastermix
    PM.aliquoting_reagent(reagent_source = MasterMix,
                          reagent_tube_type = reagent_tube_type,
                          reagent_startvolume = total_mastermix_volume,
                          aliquot_volume = mastermix_volume,
                          destination_wells = sample_std_dest + stdseries_dest,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'raise_error',
                          pause = False,
                          protocol = protocol)        
#### Transferring unique barcodes
    # Forward
    PM.transferring_reagents(source_wells = forward_tubes,
                             destination_wells = unique_primer_dest,
                             transfer_volume = primer_vol,
                             airgap = True,
                             mix = True,
                             p20 = p20,
                             p300 = p300,
                             protocol = protocol)
    # Reverse
    PM.transferring_reagents(source_wells = reverse_tubes,
                             destination_wells = unique_primer_dest,
                             transfer_volume = primer_vol,
                             airgap = True,
                             mix = True,
                             p20 = p20,
                             p300 = p300,
                             protocol = protocol)
#### Transferring single barcode to standard samples
    if not std_unique_barcodes:
        
        forward_stocks = []
        reverse_stocks = []
        for i in range(number_of_std_samples):
            forward_stocks.append(forward_stock[0])
            reverse_stocks.append(reverse_stock[0])
        
        # Forward
        PM.transferring_reagents(source_wells = forward_stocks,
                                 destination_wells = std_primer_destination,
                                 transfer_volume = primer_vol,
                                 airgap = True,
                                 mix = True,
                                 p20 = p20,
                                 p300 = p300,
                                 protocol = protocol)
        # Reverse
        PM.transferring_reagents(source_wells = reverse_stocks,
                                 destination_wells = std_primer_destination,
                                 transfer_volume = primer_vol,
                                 airgap = True,
                                 mix = True,
                                 p20 = p20,
                                 p300 = p300,
                                 protocol = protocol)

#### Transferring single barcode to standard dilution series
    if number_of_std_series > 0:
        if stdseries_unique_barcodes:
            for i in range(number_of_std_series):
                forward_stocks = []
                reverse_stocks = []
                for x in range(length_std_series):
                    forward_stocks.append(forward_stock[i])
                    reverse_stocks.append(reverse_stock[i])
                
                destinations = stdseries_dest[length_std_series*i:length_std_series*(i+1)]
                
                # Forward
                PM.transferring_reagents(source_wells = forward_stocks,
                                         destination_wells = destinations,
                                         transfer_volume = primer_vol,
                                         airgap = True,
                                         mix = True,
                                         p20 = p20,
                                         p300 = p300,
                                         protocol = protocol)
                # Reverse
                PM.transferring_reagents(source_wells = reverse_stocks,
                                         destination_wells = destinations,
                                         transfer_volume = primer_vol,
                                         airgap = True,
                                         mix = True,
                                         p20 = p20,
                                         p300 = p300,
                                         protocol = protocol)
        else:
            forward_stocks = []
            reverse_stocks = []
            for i in range(number_of_std_series * length_std_series):
                forward_stocks.append(forward_stock[0])
                reverse_stocks.append(reverse_stock[0])
            
            # Forward
            PM.transferring_reagents(source_wells = forward_stocks,
                                     destination_wells = stdseries_dest,
                                     transfer_volume = primer_vol,
                                     airgap = True,
                                     mix = True,
                                     p20 = p20,
                                     p300 = p300,
                                     protocol = protocol)
            # Reverse
            PM.transferring_reagents(source_wells = reverse_stocks,
                                     destination_wells = stdseries_dest,
                                     transfer_volume = primer_vol,
                                     airgap = True,
                                     mix = True,
                                     p20 = p20,
                                     p300 = p300,
                                     protocol = protocol)
            
            
            
            
            
        
        
       
   


    
    
    
    
    