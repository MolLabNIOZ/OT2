"""
A protocol for preparing a qPCR with EVE

This protocol distributes mastermix for your samples and if desired for NTCs,
standard samples and standard dilution series.
After that samples will be transferred. If desired a replicate of standard
sample will be transferred.

This protocol can distribute mastermix for your standard dilution series, but
the dilution series itself has to be added in the postPCR lab. This can be done
by MO.


"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
#### Starting tips
starting_tip_p20 = 'A1'
starting_tip_p300 = 'A1'

#### MasterMix information
# Do you want Mastermix aliquoted, or only samples.
mastermix = False
# What is the total starting volume (µL) of your MasterMix?
master_mix_total_volume = 1140
# What is the volume (µL) of MasterMix that needs to be dispensed?
master_mix_aliquot_volume = 20

#### Sample information
# How many samples do you want to include?
number_of_samples = 50
    ## Max 96 minus controls and standards
# Do you want repeats of the samples on the same PCR plate?
replicates = 1 # single PCRs = 1, duplicates = 2, etc.
    ## NTCs will also be repeated
# How much (µL) sample do you want to add in the PCR?
sample_transfer_volume = 5
# In what kind of tubes are your samples?
sample_tube_type = '1.5mL_tubes'
  ## Other options: 'PCR_strips', 'skirted_plate_96', '1.5mL_tubes'
if sample_tube_type == 'PCR_strips':    
# In which columns are the strips in the plate (ignore if not using strips)?
    sample_columns = ['2', '7','11'] 
    # max 4 racks with strips
else: 
    sample_columns = False
#### What else do you want to include in the PCR?
# How many NTCs do you want to include?
number_of_NTCs = 2 
    ## NTCs will be located right after your samples or sample replicates

# Do you want to include a standard dilution series?
standard_dilution_series = True 
    ## Boolean True or False
if standard_dilution_series:
    # How many dilution serie replicates do you want to include?
    number_of_std_series = 3
    ## Standard dilution series consist of 8 different dilutions and
    ## will be added to the columns on the right of the plate.
    ## This protocol only adds the mastermix, dilution series itself have to be 
    ## added in the postPCR Lab by MO

# Do you want to include a standard sample?
standard_samples = True # Boolean True or False
    ## This is a replicate of a mix of your samples which will be included on
    ## all your PCR plates in order to be able to normalize results over 
    ## multiple PCR plates.
    ## This sample should be provided in the same kind of tube as your samples
    ## and should be located directly behind your samples.
if standard_samples:
    # How many standard_samples do you want to include?
    number_of_std_samples = 6
    # How much volume is in your tube?
    standard_sample_start_volume = 150
# =============================================================================

# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
#### Simulation or robot run
simulate = True

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
if standard_samples:
    total_number_of_samples = number_of_samples + 1
      ## If a standard sample is taken, add 1 to the total number of samples
else:
    total_number_of_samples = number_of_samples
    
if sample_tube_type == '1.5mL_tubes':
    samples_per_rack = 24
if sample_tube_type == 'skirted_plate_96':
    samples_per_rack = 96
if sample_tube_type == 'PCR_strips':
    samples_per_rack = 8 * len(sample_columns)
number_of_sample_racks = math.ceil(total_number_of_samples / samples_per_rack)
  ## How many tube_strip_racks are needed (1,2 or 3)
# =============================================================================
  
# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'qPCR_protocol',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('qPCR - aliquoting mix and samples'),
    'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix;
    Adding samples from different labware.
    """
# =============================================================================

# CHECK IF EVERYTHING FITS ON THE PLATE========================================
# =============================================================================    
    total_reactions = number_of_samples * replicates + number_of_NTCs
    if standard_dilution_series:
        total_reactions = total_reactions + (number_of_std_series*8)
    if standard_samples:
        total_reactions = total_reactions + number_of_std_samples
    if total_reactions > 96:
        raise Exception(f'You have a total of {total_reactions} reactions. '
                        f'This will not fot on a PCR plate.')
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Loading pipette tips
    # If master_mix_aliquot_volume >= 19, you need P300 tips, else you only 
    # need P20 tips
    if master_mix_aliquot_volume >= 19:
        tips_20 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'tipone_20uL',
                                  amount = 2,
                                  deck_positions = [7,10],
                                  protocol = protocol)
        P300 = True
        tips_300 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'opentrons_200uL',
                                  amount = 1,
                                  deck_positions = [11],
                                  protocol = protocol)
    else:
        tips_20 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'tipone_20uL',
                                  amount = 3,
                                  deck_positions = [7,10,11],
                                  protocol = protocol)
        P300 = False
        tips_300 = False
        
    #### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20 = True, 
                                    tips_20 = tips_20,
                                    starting_tip_p20 = starting_tip_p20,
                                    P300 = P300, 
                                    tips_300 = tips_300,
                                    starting_tip_p300 = starting_tip_p300,
                                    protocol = protocol)
    
    #### Loading labware
    ### MasterMix
    # What kind of tube do you need for the specified volume?
    reagent_tube_type, number_of_tubes, max_volume = LW.which_tube_type(
        total_volume = master_mix_total_volume, tube_type = False)
    if mastermix:
        protocol.comment(f'Please provide your mastermix in a {reagent_tube_type}.'
                         f' 5mL and 1.5mL tubes we have available in amber.')
    # Load the correct rack for the specified tube type
    mastermix_racks = LW.loading_tube_racks(simulate = simulate,
                                      tube_type = reagent_tube_type,
                                      reagent_type = 'Mastermix',
                                      amount = 1,
                                      deck_positions = [8],
                                      protocol = protocol)
    # Where is the masterMix tube located
    mastermix_tube = LW.tube_locations(source_racks = mastermix_racks,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = 1)
    
    ### Samples
    # Load the correct rack for the specified tube type
    sample_racks = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = sample_tube_type,
                                         reagent_type = 'sample_rack',
                                         amount = number_of_sample_racks,
                                         deck_positions = [1,3,4,6],
                                         protocol = protocol)
    # Make a list with all sample locations
    sample_tubes = LW.tube_locations(source_racks = sample_racks,
                                     specific_columns = sample_columns,
                                     skip_wells = False,
                                     number_of_tubes = number_of_samples)
    sample_sources = sample_tubes * replicates
        
    # If you have a standard sample, define the location
    if standard_samples:
        standard_tube = [LW.tube_locations(source_racks = sample_racks,
                                         specific_columns = sample_columns,
                                         skip_wells = False,
                                         number_of_tubes = number_of_samples + 1)[-1]]
        standard_sources = standard_tube * number_of_std_samples
    
    ### PCR plate
    qPCR_plate = LW.loading_tube_racks(simulate = simulate,
                                       tube_type = 'plate_96_NIOZholder',
                                       reagent_type = 'qPCR-plate',
                                       amount = 1,
                                       deck_positions = [5],
                                       protocol = protocol)
    ## Where goes what in the plate?
    # Define all wells in the plate
    qPCR_wells = LW.tube_locations(source_racks = qPCR_plate,
                                   specific_columns = False,
                                   skip_wells = False,
                                   number_of_tubes = 96)
    # Where do samples go?
    sample_destinations = qPCR_wells[:(number_of_samples)*replicates]
    # Where do NTCs go?
    NTC_destinations = qPCR_wells[(number_of_samples)*replicates:(
        (number_of_samples)*replicates) + number_of_NTCs]
    # Where does the standard_sample go?
    if standard_samples:
        standard_sample_destinations = qPCR_wells[
            ((number_of_samples)*replicates) + number_of_NTCs:(
                (number_of_samples)*replicates) + number_of_NTCs + number_of_std_samples]
    # Where does the standard dilution series go?
    if standard_dilution_series:
        specific_qPCR_columns = ['12','11','10','9','8','7','6','5','4','3','2','1']
        std_dilution_destinations = []
        for i in range(number_of_std_series):
            column = []
            column.append(specific_qPCR_columns[i])
            destination = LW.tube_locations(source_racks = qPCR_plate,
                                     specific_columns = column,
                                     skip_wells = False,
                                     number_of_tubes = 8)
            std_dilution_destinations = std_dilution_destinations + destination
    
    # Where should mastermix go?
    mastermix_destinations = sample_destinations + NTC_destinations
    if standard_samples:
        mastermix_destinations = mastermix_destinations + standard_sample_destinations
    if standard_dilution_series:
        mastermix_destinations = mastermix_destinations + std_dilution_destinations    
# =============================================================================     
    
# LIGHTS OFF===================================================================
# =============================================================================
    # In case the lights were on before the start, they should be turned off 
    # during a qPCR
    protocol.set_rail_lights(False)
# =============================================================================

# THE ACTUAL PIPETTING ========================================================
# =============================================================================
    #### Aliquoting mastermix
    if mastermix:
        PM.aliquoting_reagent(reagent_source = mastermix_tube,
                          reagent_tube_type = reagent_tube_type,
                          reagent_startvolume = master_mix_total_volume,
                          aliquot_volume = master_mix_aliquot_volume,
                          destination_wells = mastermix_destinations,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'raise_error',
                          pause = False,
                          protocol = protocol)
    
    #### Transferring samples
    PM.transferring_reagents(source_wells = sample_sources,
                             destination_wells = sample_destinations,
                             transfer_volume = sample_transfer_volume,
                             airgap = True,
                             mix = True,
                             p20 = p20,
                             p300 = p300,
                             protocol = protocol)
    #### Transferring standard sample
    if standard_samples:
        PM.transferring_reagents(source_wells = standard_sources,
                                 destination_wells = standard_sample_destinations,
                                 transfer_volume = sample_transfer_volume,
                                 airgap = True,
                                 mix = True,
                                 p20 = p20,
                                 p300 = p300,
                                 protocol = protocol)

