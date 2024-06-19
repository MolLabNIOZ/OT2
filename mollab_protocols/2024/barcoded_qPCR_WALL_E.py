"""
WALL-E protocol for barcoded qPCRs
Samples will get unique barcodes
Standard sample replicates will all get the same barcode
Dilution series will get either all the same barcode or the same within series, 
but unique among series
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================

#### Starting tips
#Wwhat is the well of the first tipboxes for eithe p20 and p300 tips
starting_tip_p20 = 'A1'
starting_tip_p300 = 'A1'

#### MASTERMIX
# What is the total startvolume (µL) of your mastermix?
total_mastermix_volume = 924
# What is the volume (µL) of mastermix that needs to be aliquoted per reaction?
mastermix_volume = 19

#### SAMPLES
# How many samples do you want to include?
number_of_samples = 6     ##!!! NOTE: include in this number the mock too
# Which specific wells (index) do you want to skip? Leave empty if you do not want to skip
skipped_wells = []  
# How many NTCs to include 
number_of_NTCs = 2

####STANDARDS
# How many dilution serie replicates do you want to include?
number_of_std_series = 3 
  ## If none -- fill in 0
# How many dilutions are in the standard dilution series?
length_std_series = 8  ## length_of_std_series  MAX == 8                                     
# How many replicates of the standard sample do you want?
number_of_std_samples = 6 

#### PRIMERS
# In what columns of the rack are the strips located? 
primer_loc = ['1', '3', '5', '7', '9', '11']  ## max 2 racks with strips
# What is the volume (µL) of each primer that needs to be added to the mix?
primer_vol = 1.5
# How many primers should WALL-E skip, or index of first_primer?
skipped_F_primers = 0 
skipped_R_primers = 0
# Should the standard samples each get unique barcodes?
std_unique_barcodes = False
# Should each dilution series get a unique barcode?
stdseries_unique_barcodes = True
# =============================================================================

# SIMULATE=====================================================================
# =============================================================================
# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol  
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
#### Import math 
import math
  ## To do some calculations  
                                      
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
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

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'general_PCR_protocol',
    'author': 'MB <maartje.brouwer@nioz.nl>, RDB <rob.de.beer@nioz.nl>',
    'description': ('qPCR - aliquoting mix and samples'),
    'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix;
    Adding samples from different labware.
    """
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
                                                          total_reactions,
                                                          1,
                                                          19)
    p20_tips_total += p20_tips_needed
    p300_tips_total += p300_tips_needed
    
    # racks needed
    p20_tip_racks = LW.number_of_tipracks(starting_tip_p20, p20_tips_total)
    p300_tip_racks = LW.number_of_tipracks(starting_tip_p300, p300_tips_total)
    
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
    P20 = False
    P300 = False    
    if p20_tip_racks > 0:
        P20 = True
    if p300_tip_racks > 0:
        P300 = True
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
                                  number_of_tubes = 1)

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
                                      number_of_tubes = total_unique_primers)
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
                                      number_of_tubes = total_unique_primers)
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
                                          number_of_tubes = 1)
        reverse_stock = LW.tube_locations(source_racks = primer_stock_rack,
                                          specific_columns = ['1'],
                                          skip_wells = [0],
                                          number_of_tubes = 2)
    else:
        forward_stock = LW.tube_locations(source_racks = primer_stock_rack,
                                          specific_columns = ['1'],
                                          skip_wells = False,
                                          number_of_tubes = number_of_std_series)
        reverse_stock = LW.tube_locations(source_racks = primer_stock_rack,
                                          specific_columns = ['6'],
                                          skip_wells = False,
                                          number_of_tubes = number_of_std_series)

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
                                                          number_of_NTCs)
    
    if number_of_std_series > 0:
        specific_qPCR_columns = ['12','11','10','9','8','7','6','5','4','3','2','1']
        stdseries_dest = []        
        for i in range(number_of_std_series):
            column = []
            column.append(specific_qPCR_columns[i])
            destination = LW.tube_locations(source_racks = qPCR_plate,
                                                specific_columns = column,
                                                skip_wells = False,
                                                number_of_tubes = length_std_series)
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
            
            
            
            
            
        
        
       
   


    
    
    
    
    