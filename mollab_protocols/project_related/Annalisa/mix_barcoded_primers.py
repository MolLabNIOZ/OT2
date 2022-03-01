"""
VERSION: V_March22
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# If mastermix dispense > 19: What is the starting position of the 200µL tips?
starting_tip_p200 = 'A1'
  ## If not applicable, you do not have to change anything
  
# How many samples do you want to include?
number_of_samples = 23   
  ## Max = 24 INCLUDING NTC            

# How many NTCs to include 
number_of_NTCs = 1 
  ## NOTE: The NTC should ALWAYS be at the end                                         

# What is the total volume (µL) of your mix?
start_vol = 1116
  ## The start_vol is the volume (µL) of mix that is in the source        
  ## labware at the start of the protocol.                                  

# Which tube are you using for your mastermix? (options 1.5mL or 5mL)
mastermix_tube_type = 'tube_1.5mL'
  ## For volume < 1300: 'tube_1.5mL'                                        
  ## For volume > 1300: 'tube_5mL'                                          

# What is the volume (µL) of mastermix that needs to be dispensed?
dispension_vol = 43   

# Where is the mastermix tube located in the rack? 
mastermix_source = 'D1'
  ## convenient places:
  ## if mastermix_tube_type ==   'tube_1.5mL'  -->  D1 
  ## if mastermix_tube_type ==   'tube_5mL'    -->  C1
    
                                         
# What is the volume (µL) of primer that needs to be added to the mix?
F_primer_vol = 3
R_primer_vol = 1.5                   
  
# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol                 
# =============================================================================

## IMPORT STATEMENTS===========================================================
## ============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      
import math
  ## To do some calculations  
  
if simulate: #Simulator
    from mollab_modules import volume_tracking_v1 as vt
    import json 
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.     
else: #Robot
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
## ============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
number_of_primers = number_of_samples + number_of_NTCs
## ============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'mix_barcoded_primers_2Rprimers',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Illumina PCR - aliquoting mix and primers, 2 different '
                    'R primers'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix;
    Adding barcoded primers.
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    # Pipette tips
    if dispension_vol >= 19:
      ## When the mm volume to be dispensed >= 19, 200µL tips are          
      ## needed in addition to the 20µL tips.                              
        tips_200 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', 
            2,                                  
            '200tips')                          
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            7,                                  
            '20tips_1')                                
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            10,                                 
            '20tips_2')                         
        tips_20 = [tips_20_1, tips_20_2]
    else:
      ## When the mm volume to be dispensed <=19, only 20µL are needed      
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            2,                                  
            '20tips_1')                           
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            7,                                  
            '20tips_2')                           
        tips_20_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            10,                                 
            '20tips_3')                             
        tips_20 = [tips_20_1, tips_20_2, tips_20_3]
   
    # Tube_racks & plates                                                     
                          
    if mastermix_tube_type == 'tube_1.5mL':
        mastermix_tube = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            3,
            'mastermix_tube')
    
    primer_source = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    
        1,                                  
        'primer_source_1')                       
                        
    if simulate: #Simulator
        if mastermix_tube_type == 'tube_5mL': 
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                      labware_def_5mL = json.load(labware_file)
            mastermix_tube = protocol.load_labware_from_definition( 
                labware_def_5mL,           
                3,                         
                'mastermix_tube')           

    else: #Robot
        if mastermix_tube_type == 'tube_5mL': 
            mastermix_tube = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                3,                                     
                'mastermix_tube')                               
           
    # Pipettes
    if dispension_vol >= 19:
        p300 = protocol.load_instrument(
            'p300_single_gen2',             
            'right',                        
            tip_racks=[tips_200])           
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  
        'left',                             
        tip_racks=tips_20)                  
# =============================================================================

# PREDIFINED VARIABLES=========================================================
# =============================================================================
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
      ## The aspiration_vol is the volume (µL) that is aspirated from the   
      ## container.                                                         
    ##### Variables for volume tracking
    start_height = vt.cal_start_height(mastermix_tube_type, start_vol)
      ## Call start height calculation function from volume tracking module.
    current_height = start_height
      ## Set the current height to start height at the beginning of the     
      ## protocol.                                                       
    F_primer_mix_vol = F_primer_vol + 3
    R_primer_mix_vol = R_primer_vol + 3 
      ## primer_mix_vol = volume for pipetting up and down                  
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    # Setting starting tip                                           
    if dispension_vol >= 19:
        ## If the mm volume to be dispendsed >= 19, assign p300 starting tip
        p300.starting_tip = tips_200.well(starting_tip_p200)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
    
    # Mastermix tube location
    MasterMix = mastermix_tube[mastermix_source]
    
    # Make a list with all 96 wells of the plate                         
    wells = []
    for well in plate_96.wells():
        wells.append(well)
    
    # Create the list of wells where samples should go
    sample_wells = wells[:number_of_primers]
      ## cuts off the list after a the number_of_samples number of wells    
    
    # Create the list of wells where standard sample replicates should go
    slice_std_wells = slice(
        number_of_primers, number_of_primers + number_of_std_samples)
      ## Slice the list - I need the number_of_std_samples of wells after   
      ## the number_of_samples wells. So I need a certain amount of wells   
      ## after the sample wells, but not all of the wells after that.       
      ## This slices the list after the samples and after the std sample    
      ## so that we only take the wells in between.                         
    std_sample_wells = wells[slice_std_wells]

    # Create the list of wells where standerd series should go
    std_series_wells = [] 
    std_series_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in
         ['12', '11', '10']])
    std_series_columns = std_series_columns[:number_of_std_series]
    ## Reserve a column at the end of the plate for every std_series        
    ## Separate the columns into wells and append them to list              
    for column in std_series_columns:
        column = column[:length_std_series]
        ## cut off the columns after a certain std_series length            
        for well in column:
            std_series_wells.append(well)

    # Add the wells of the standards into 1 list 
      ## This needs to be a list separate from the rest of the wells because
      ## they need the same primer from a separate tube.                    
    std_wells = std_sample_wells + std_series_wells 
    # Add all the wells that need mastermix into 1 list
    MasterMixAliquots = sample_wells + std_wells
    
    # Primer locations
    primer_wells = []
    if primer_tube_type == 'PCR_strips':
        primer_columns = []
        if primer_racks >= 1:
            primer_columns_1 = (
                ([primer_source_1.columns_by_name()[column_name] 
                  for column_name in primer_loc]))
            for column in primer_columns_1:
                primer_columns.append(column)
        if primer_racks >= 2:
            primer_columns_2 = (
                ([primer_source_2.columns_by_name()[column_name] 
                  for column_name in primer_loc]))
            for column in primer_columns_2:
                primer_columns.append(column)
        if primer_racks >= 3:
            primer_columns_3 = (
                ([primer_source_3.columns_by_name()[column_name] 
                  for column_name in primer_loc]))
            for column in primer_columns_3:
                primer_columns.append(column)
            ## Make a list of columns, this is a list of lists!             
        for column in primer_columns:
            for well in column:
                primer_wells.append(well)
    if primer_tube_type == 'plate_96':
        if primer_racks == 1:
            for well in primer_source_1.wells():
                primer_wells.append(well)
        if primer_racks == 2: 
            for well in primer_source_2.wells():
                primer_wells.append(well)
        if primer_racks == 3:
            for well in primer_source_3.wells():
                primer_wells.append(well)
    primer_wells = primer_wells[:number_of_primers]
    
    # Set location for primer for standards
    if number_of_std_samples >= 1:
        std_primer = big_primer_source.wells_by_name()[std_primer_loc]
# =============================================================================