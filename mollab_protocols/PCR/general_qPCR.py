"""
qPCR.py is a protocol written for EVE for the adding of mastermix and samples 
to a 96-wells plate.

"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# If mastermix dispense > 19: What is the starting position of the 200µL tips?
starting_tip_p200 = 'A1'
  ## If not applicable, you do not have to change anything
  
# How many samples do you want to include?
number_of_samples = 6     
  ## MAX ==  number of samples -                                 
  ##         (number of std series * length of std series) -     
  ##         number of standard sample replicates

# How many NTCs to include 
number_of_NTCs = 2 
  ## NOTE: The NTC should ALWAYS be at the end of your plate!!                     

# What is the total volume (µL) of your mix?
start_vol = 1108.8
  ## The start_vol_m is the volume (µL) of mix that is in the source        
  ## labware at the start of the protocol.  
  
# How many dilution serie replicates do you want to include?
number_of_std_series = 1  
# How many dilutions are in the standard dilution series?
length_std_series = 8  
  ## length_of_std_series  MAX == 8                                     
# How many replicates of the standard sample are you taking?
number_of_std_samples = 8

# Which tube are you using for your mastermix? (options 1.5mL or 5mL)
mastermix_tube_type = 'tube_5mL'
  ## For volume < 1300: 'tube_1.5mL'                                        
  ## For volume > 1300: 'tube_5mL'     

# What is the volume (µL) of mastermix that needs to be dispensed?
dispension_vol = 19     

# Where is the mastermix tube located in the rack? 
mastermix_source = 'C1'
  ## convenient places:
  ## if mastermix_tube_type ==   'tube_1.5mL'  -->  D1 
  ## if mastermix_tube_type ==   'tube_5mL'    -->  C1 

# What labware are your samples in?
sample_tube_type = 'plate_96'
  ## Samples in strips = 'PCR_strip'                                       
  ## Primers in plate = 'plate_96'  
  ## Samples in 1.5mL tubes = 'tube_1.5mL'                                         
# What is the volume (µL) of sample that needs to be added to the mix?
sample_vol = 1
  ## MAX = 17µL
# In which columns are the strips in the plate (ignore if not using strips)?
sample_columns = ['2', '5', '8','11']
  ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
  ## max 4 racks with strips!  
# What is the location of your first sample (fill in if you have a plate)?                                    
first_sample = 'A1'
  ## 'A1' is standard. But if you have more samples in the plate than
  ## fit in the qPCR, change the first well position.

# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol                 
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
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
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================                   
if sample_tube_type == 'tube_1.5mL':
    sample_racks = math.ceil(number_of_samples / 24)
if sample_tube_type == 'PCR_strip':
    if len(sample_columns) == 3:
        sample_racks = math.ceil(number_of_samples / 24)  
    if len(sample_columns) == 4: 
        sample_racks = math.ceil(number_of_samples / 32)     
  ## How many tube_strip_racks are needed (1,2 or 3)
if sample_tube_type == 'plate_96':
    sample_racks = math.ceil(number_of_samples / 96)
    ## *this isn't really used yet as we also only add one sample plate
    ##  so for now we cannot add >primer pairs, but if we add another 
    ##  destination plate it would be possible -- didn't do this because
    ##  we don't have plates with more than 96 primer combinatons
if number_of_std_samples >= 1:
    number_of_samples = number_of_samples + 1
      ## If a standard sample is taken, add 1 to the total number of samples
first_sample_string = (first_sample + ' of sample_source_1 on 2')
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'qPCR',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('qPCR - aliquoting mix and samples'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix;
    Adding samples from different labware.
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
            4,                                  
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
            4,                                  
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
    destination_plate = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        
        3,                                      
        'plate_96')   
    
    if mastermix_tube_type == 'tube_1.5mL':
        mastermix_tube = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            1,
            'mastermix_tube')
    
    if sample_tube_type == 'tube_1.5mL':
        sample_source_1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            2,
            'sample_source_1')
        if sample_racks >= 2:
            sample_source_2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                5,
                'sample_source_2')
        if sample_racks >= 3:
            sample_source_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                8,
                'sample_source_3')
        if sample_racks >= 4:
            sample_source_4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                11,
                'sample_source_4')
    if sample_tube_type == 'plate_96':
        sample_source_1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            2,                                  
            'sample_source_1')
        sample_source_2 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            5,                                  
            'sample_source_2')
    
    if simulate: #Simulator
        if mastermix_tube_type == 'tube_5mL': 
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                 "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                      labware_def_5mL = json.load(labware_file)
            mastermix_tube = protocol.load_labware_from_definition( 
                labware_def_5mL,           
                1,                         
                'mastermix_tube')   
        if sample_tube_type == 'PCR_strip':
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            sample_source_1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                2,                         
                'sample_source_1')         
            if sample_racks >=2:
                sample_source_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    5,                     
                    'sample_source_2')    
            if sample_racks >=3:
                sample_source_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips,
                    8,                   
                    'sample_source_3')    
            if sample_racks >=4:
                sample_source_4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips,
                    11,                   
                    'sample_source_4')     
    else: 
        if mastermix_tube_type == 'tube_5mL': 
            mastermix_tube = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                1,                                     
                'mastermix_tube')  
        if sample_tube_type == 'PCR_strips':
            sample_source_1 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                2,                                     
                'sample_source_1')                      
            if sample_racks >=2:
                sample_source_2 = protocol.load_labware_( 
                    'pcrstrips_96_wellplate_200ul',    
                    5,                                 
                    'sample_source_2')                 
            if sample_racks >=3:
                sample_source_3 = protocol.load_labware( 
                    'pcrstrips_96_wellplate_200ul',    
                    8,                                
                    'sample_source_3') 
            if sample_racks >=4:
                sample_source_4 = protocol.load_labware( 
                    'pcrstrips_96_wellplate_200ul',    
                    11,                                
                    'sample_source_4') 
                
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
    sample_mix_vol = sample_vol + 3
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
    
    # Make a list of all possible wells in the destination plate
    wells = []
    for well in destination_plate.wells():
        wells.append(well)
    # Create a list of wells where samples should go
    sample_wells = wells[:number_of_samples]
    
    #Create a list of wells where standard sample replicates should go
    slice_std_sample_wells = slice(
        number_of_samples, number_of_samples + number_of_std_samples)
    std_sample_wells = wells[slice_std_sample_wells]
      ## Slice the list after the number of samples, and after the number
      ## of standard sample replicates to retrieve the wells in between
    
    # Create the list of wells where NTCs should go
    slice_NTC_wells = slice(
        number_of_samples + number_of_std_samples,
        number_of_samples + number_of_std_samples + number_of_NTCs)
    NTC_wells = wells[slice_NTC_wells]
      ## Slice the list after the number of samples + the number of standard
      ## sample replicates, and after that + the number of NTCs to retrieve
      ## the wells in between (the last of the wells that need to be filled)
    
    # Create the list of wells where standerd series should go
    std_series_wells = [] 
    std_series_columns = (
        [destination_plate.columns_by_name()[column_name] for column_name in
         ['12', '11', '10']])
    std_series_columns = std_series_columns[:number_of_std_series]
    ## Reserve a column at the end of the plate for every std_series        
    ## Separate the columns into wells and append them to list              
    for column in std_series_columns:
        column = column[:length_std_series]
        ## cut off the columns after a certain std_series length            
        for well in column:
            std_series_wells.append(well)
    
    # Create a list with wells where mastermix should go
    MasterMixAliquots = (
        sample_wells + std_sample_wells + NTC_wells + std_series_wells)
    
    sample_sources = []
    if sample_tube_type == 'tube_1.5mL' or sample_tube_type == 'plate_96':
        if sample_racks >= 1:
            for well in sample_source_1.wells():
                sample_sources.append(well)
        if sample_racks >= 2:
            for well in sample_source_2.wells():
                sample_sources.append(well)
        if sample_racks >= 3:
            for well in sample_source_3.wells():
                sample_sources.append(well)
        if sample_racks >= 4:
            for well in sample_source_4.wells():
                sample_sources.append(well)
        first_sample_index = sample_sources.index(first_sample_string)
          ## Determine the index of the first sample in the list     
        slice_sample_sources = slice(
            first_sample_index, 
            first_sample_index + number_of_samples)
          ## Slice the list after the number of wells to skip.
        sample_sources = sample_sources[slice_sample_sources]
        if number_of_std_samples >= 1:
            std_source = [sample_sources[-1]] * (number_of_std_samples - 1)
            for well in std_source:
                sample_sources.append(well)
                  ## adds the same well (where the std_sample is) to the sample  
                  ## sources list, so will pipete number_of_std_samples times from   
                  ## the same well  
    if sample_tube_type == 'PCR_strips':
        sample_source_columns = []
        if sample_racks == 1:
            sample_columns_1 = (
                ([sample_source_1.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_1:
                sample_source_columns.append(column)
        if sample_racks == 2:
            sample_columns_2 = (
                ([sample_source_2.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_2:
                sample_source_columns.append(column)
        if sample_racks == 3:
            sample_columns_3 = (
                ([sample_source_3.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_3:
                sample_source_columns.append(column)
        if sample_racks == 4:
            sample_columns_4 = (
                ([sample_source_4.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_4:
                sample_source_columns.append(column)
          ## Make a list of columns, this is a list of lists!   
        for column in sample_source_columns:
            for well in column:
                sample_sources.append(well)
          ## Separate the columns into wells and append them to list 
        sample_sources = sample_sources[:number_of_samples]
        if number_of_std_samples >= 1:
            std_source = ([sample_sources[-1]]) * (number_of_std_samples - 1)
            for well in std_source:
                sample_sources.append(well)
                  ## adds the same well (where the std_sample is) to the sample  
                  ## sources list, so will pipete number_of_std_samples times
                  ## from the same well  
# =============================================================================              
              
## PIPETTING===================================================================
## ============================================================================
## ALIQUOTING MASTERMIX--------------------------------------------------------
    if dispension_vol >= 19:
        pipette = p300
    else:
        pipette = p20
    for i, well in enumerate(MasterMixAliquots):
      ## aliquot mix, for each well do the following:                       
        if i == 0: 
            pipette.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    
        elif i % 8 == 0:
            pipette.drop_tip()
            pipette.pick_up_tip()
              ## Then, after every 8th well, drop tip and pick up new       
    
        current_height, pip_height, bottom_reached = vt.volume_tracking(
                mastermix_tube_type, dispension_vol, current_height)
                  ## call volume_tracking function, obtain current_height,  
                  ## pip_height and whether bottom_reached.                 
        
        if bottom_reached:
            aspiration_location = MasterMix.bottom(z=1)
            protocol.comment("You've reached the bottom of the tube!")
              ## If bottom is reached keep pipetting from bottom + 1        
        else:
            aspiration_location = MasterMix.bottom(pip_height)
              ## Set the location of where to aspirate from.                

        #### The actual aliquoting of mastermix                             
        pipette.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the       
          ## location specified in aspiration_location.                     
        pipette.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the         
          ## location specified in well (so a new well every time the       
          ## loop restarts)                                                 
        pipette.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill      
          ## completely when using a disposal volume by dispensing some     
          ## of the volume after each pipetting step. (blow-out to many     
          ## bubbles)                                                       
    pipette.drop_tip()   
## ----------------------------------------------------------------------------
## ADDING SAMPLES--------------------------------------------------------------
    ## Loop through source and destination wells
    for sample_tube, well in zip(sample_sources, destination_plate.wells()):
        p20.pick_up_tip()
        p20.aspirate(sample_vol, sample_tube)
        p20.dispense(sample_vol, well)
        sample_mix_vol = sample_vol + 3
          ## primer_mix_vol = volume for pipetting up and down              
        p20.mix(3, sample_mix_vol, well)
        p20.dispense(10, well)
        p20.drop_tip()
# ----------------------------------------------------------------------------
# =============================================================================