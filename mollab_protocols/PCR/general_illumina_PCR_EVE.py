"""
general_illumina_PCR_EVE.py is a protocol written for EVE for adding the 
samples to the mastermix with barcoded primers in a 96-well plate.

You have to provide:
    Number of samples (excl. NTC and mock)
    What is the volume (µL) of sample that nees to be dded
    Will you add a mock sample?:
        if True - an extra sample will be added to the number of samples
    In what kind of tubes your samples are (PCR strips or 1.5mL tubes)
    Whether you are doing a qPCR or not:
        if True lights will not be turned on
        you have the option to add x replicates of a standard sample
            this standard sample will be pipetted from the last source labware
            to the last x wells of the destination (before NTC)

EVE adds samples (sample volume) from the source labware (1.5mL tubes or 
strips) to the destination labware (96-wells plate). 

Updates:
(SV) 211028: 
    - added option for standard sample
(MB) 211203:
    - added option for sample in strips
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'H2'

# How many samples do you want to include?
number_of_samples = 6   
  ## If NOT qPCR and NOT mock                                MAX == 95      
  ## If NOT qPCR but incl. mock                              MAX == 94      
  ## If qPCR    MAX ==  number of samples -                                 
  ##                    (number of std series * length of std series) -     
  ##                    number of standard sample replicates                

# What volume (µL) of sample needs to be added to the mix?
sample_vol = 8 

# Will a mock sample be included?
mock = True
  ## True if mock has to be added by the robot.                             
  ## False if mock is not added by the robot.                               
  ## One extra sample will be added to to the total number of tubes to      
  ## pipette from. Location of this tube does not have to be in a specific 
  ## place in the sample list.                          

# In what kind of tubes are your samples?
sample_tubes = 'PCR_strips'
  ## Options: 'PCR_strips' or 'tubes_1.5mL'                                 
if sample_tubes == 'PCR_strips':
    strip_positions = ['2', '5', '8','11']     
      ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                 
      ## max 4 racks with strips!                                           
      
# Are you doing a qPCR or a regular PCR?
qPCR = True
 ## True or False                                                           
 ## Lights off if qPCR, optionel standard sample                             
if qPCR:
    # How many replicates of the standard sample are you taking?
    number_of_std_samples = 6
      ## If a standard sample is taken, the last sample in the source        
      ## labware is pipetted number_of_std_samples time in the last         
      ## number_of_std_samples wells of the destination plate (before NTC)  
else:
    ## If we are not doing a qPCR - protocol uses these values.             
    number_of_std_samples = 0

# Do you want to simulate the protocol?
simulate = False
  ## True for simulating protocol, False for robot protocol                 
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      
import math
  ## To do some calculations (rounding up)
if simulate: #Simulator
    import json 
      ## Import json to import custom labware with labware_from_definition, 
      ## so that we can use the simulate_protocol with custom labware.      
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
if mock:
    number_of_samples = number_of_samples + 1
      ## If a mock sample is taken, add 1 to the total number of samples
if number_of_std_samples >= 1:
    number_of_samples = number_of_samples + 1
      ## If a standard sample is taken, add 1 to the total number of samples
if sample_tubes == 'PCR_strips':
    if strip_positions == ['2', '7', '11']:
        tubes_per_rack = 24
    elif strip_positions == ['2', '5', '8','11']:
        tubes_per_rack = 32
if sample_tubes == 'tubes_1.5mL':
    tubes_per_rack = 24
    ## In order to calculte how many tube_racks are needed, we need to 
    ## calculate how many samples there can be in a rack. 
sample_racks = math.ceil(number_of_samples / tubes_per_rack)
  ## How many tube_racks are needed (1,2,3 or 4)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'general_illumina_PCR_EVE',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Illumina (q)PCR - adding samples'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Adding samples from 1.5 mL tubes or PCR_strips to a 96 wells plate.
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    # Pipette tips
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  
        7,                                  
        '20tips_1')                                
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  
        10,                                 
        '20tips_2')                         

    # Tube_racks & plates
    if sample_tubes == 'tubes_1.5mL':
        sample_tubes_1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            4,                                                       
            'sample_tubes_1')                                        
        if sample_racks >= 2:
            sample_tubes_2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                1,                                                       
                'sample_tubes_2')                                        
        if sample_racks >= 3:
            sample_tubes_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                3,                                                       
                'sample_tubes_3')                                        
        if sample_racks >= 4:
            sample_tubes_4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                11,                                                      
                'sample_tubes_4')                                        
    
    if simulate: #Simulator
        if sample_tubes == 'PCR_strips':
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            sample_strips_1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, 
                4,                     
                'sample_strips_1')       
            if sample_racks >= 2:
                sample_strips_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    1,                     
                    'sample_strips_2')     
            if sample_racks >= 3:
                sample_strips_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    3,                    
                    'sample_strips_3')                            
            if sample_racks >= 4:
                sample_strips_4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    11,                   
                    'sample_strips_4') 
        with open("labware/biorad_qpcr_plate_eppendorf_cool_rack/"
                    "biorad_qpcr_plate_eppendorf_cool_rack.json") as labware_file:
                  labware_def_cool_rack = json.load(labware_file)
        plate_96 = protocol.load_labware_from_definition( 
            labware_def_cool_rack,  
            5,                     
            '96well_plate_rack')        
    else: #Robot
        if sample_tubes == 'PCR_strips':  
            sample_tubes_1 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',    
                4,                                
                'sample_strips_1')                 
            if sample_racks >= 2:
                sample_strips_2 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',    
                1,                                 
                'sample_strips_2')                 
            if sample_racks >= 3:
                sample_strips_3 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',   
                3,                               
                'sample_strips_3')                 
            if sample_racks >= 4:
                sample_strips_4 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',    
                11,                                
                'sample_strips_4')  
        plate_96 = protocol.load_labware(
            'biorad_qpcr_plate_eppendorf_cool_rack',
            5,                                      
            '96well_plate_rack')                                                          
        
    # Pipettes
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  
        'left',                             
        tip_racks=[tips_20_1, tips_20_2])   
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
      ## The starting_tip is the location of first pipette tip in the box   

    # Sample source wells
    sample_sources = []
      ## Create an empty list to append wells to.                           
    if sample_tubes == 'tubes_1.5mL':  
        sample_sources = sample_tubes_1.wells()
        if sample_racks >= 2:
            sample_sources = sample_sources + sample_tubes_2.wells()
        if sample_racks >= 3:
            sample_sources = sample_sources + sample_tubes_3.wells()    
        if sample_racks >= 4:
            sample_sources = sample_sources + sample_tubes_4.wells()
        sample_sources = sample_sources[:number_of_samples]
        
        if number_of_std_samples >= 1:
            std_source = [sample_sources[-1]] * (number_of_std_samples - 1)
            for well in std_source:
                sample_sources.append(well)
            ## adds the same well (where the std_sample is) to the sample  
            ## sources list, so will pipete number_of_std_samples times from   
            ## the same well                                               
    if sample_tubes == 'PCR_strips':
        sample_columns = (
            ([sample_strips_1.columns_by_name()[column_name] 
              for column_name in strip_positions])) 
        if sample_racks >= 2:
            sample_columns2 = (
                ([sample_strips_2.columns_by_name()[column_name] 
                  for column_name in strip_positions]))
            for column in sample_columns2:
                sample_columns.append(column)
        if sample_racks >= 3:
            sample_columns3 = (
                ([sample_strips_3.columns_by_name()[column_name] 
                  for column_name in strip_positions]))
            for column in sample_columns3:
                sample_columns.append(column)
        if sample_racks >= 4:
            sample_columns4 = (
                ([sample_strips_4.columns_by_name()[column_name] 
                  for column_name in strip_positions]))
            for column in sample_columns4:
                sample_columns.append(column)
            ## Make a list of columns, this is a list of lists!             
        
        for column in sample_columns:
            for well in column:
                sample_sources.append(well)
        sample_sources = sample_sources[:number_of_samples]
          ## Separate the columns into wells and append them to list        
        
        if number_of_std_samples >= 1:
            std_source = [sample_sources[-1]] * (number_of_std_samples - 1)
            for well in std_source:
                sample_sources.append(well)
            ## adds the same well (where the std_sample is) to the sample  
            ## sources list, so will pipete number_of_std_samples times from   
            ## the same well             
# =============================================================================

# ADDING SAMPLES===============================================================
# =============================================================================
    ## Loop through source and destination wells
    for sample_tube, well in zip(sample_sources, plate_96.wells()):
        p20.pick_up_tip()
        p20.aspirate(sample_vol, sample_tube)
        p20.dispense(sample_vol, well)
        sample_mix_vol = sample_vol + 3
          ## primer_mix_vol = volume for pipetting up and down              
        p20.mix(3, sample_mix_vol, well)
        p20.dispense(10, well)
        p20.drop_tip()
# =============================================================================
    