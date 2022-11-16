"""
Version: V_Aug22

tapestation_reagents.py is a protocol written to add the reagents of any
TapeStation assay from a 1.5mL tube to a 96-wells plate and add the samples
from 1.5mL tubes, PCR strips or a 96-wells plate to the reagents. It is also
possible to do one of the 2.

The reagent tube should always be put in A1
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the first 20µL tip?
starting_tip_p20 = 'A1'

# How many primers do you want to dilute? 
number_of_samples = 5
  ## The maximum number of samples is 96, as the TapeStation can only measure
  ## one plate at the time anyway.

# Which Tapestation kit are you using?
tapestation_kit = 'D1000'  
  ## Options are:
  ##    'D1000'
  ##    'D5000'  
  ##    'HS-D1000'
  ##    'HS-D5000'
  ##    'gDNA'
  ##    'RNA'
  ##    'HS-RNA'

# What labware are your samples in?
sample_tube_type = 'plate_96'
  ## Samples in strips = 'PCR_strips'                                       
  ## Samples in plate = 'plate_96'  
  ## Samples in 1.5mL tubes = 'tube_1.5mL'             
sample_columns = ['2', '7','11']
  ## optional:
  ##    3 strips per rack: ['2', '7', '11'] 
  ##    4 strips per rack: ['2', '5', '8','11']
  ##    6 strips per rack: ['1', '3', '5', '7', '9', '11']

# What is the location of your first sample (fill in if you have a plate)? 
first_sample = 'A1'
  ## 'A1' is standard for tubes and plates. 
  ## 'A2' is standard for tube_strips
  ## But if you have more samples in the plate than
  ## fit in the qPCR, change the first well position.
  
# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol          
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
                                      
if simulate: #Simulator
    from mollab_modules import volume_tracking_v1 as vt
    import json 
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.     
else: #Robot
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
                                          
# Import other modules
import math
  ## math to do some calculations (rounding up)  
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
# Setting buffer and sample volume - dependent on the chosen tapestation kit
if tapestation_kit == 'D1000':
    buffer_vol = 3
    sample_vol = 1  
if tapestation_kit == 'D5000':
    buffer_vol = 10
    sample_vol = 1  
if tapestation_kit == 'gDNA':
    buffer_vol = 10
    sample_vol = 1 
if tapestation_kit == 'HS-D1000':
    buffer_vol = 2
    sample_vol = 2
if tapestation_kit == 'HS-D5000':
    buffer_vol = 2
    sample_vol = 2
if tapestation_kit == 'RNA':
    buffer_vol = 5
    sample_vol = 1  
if tapestation_kit == 'HS-RNA':
    buffer_vol = 1
    sample_vol = 2  

# What is the total volume of buffer that is needed for the amount of samples?
# +10µL for minimum volume in tube
volume_of_buffer = buffer_vol * number_of_samples + 10

# How many sample racks are needed?   
if sample_tube_type == 'PCR_strips':
    if sample_columns == ['2', '7','11']:
        sample_racks = math.ceil(number_of_samples / 24)
    elif sample_columns == ['2', '5', '8','11']:
        sample_racks = math.ceil(number_of_samples / 32)
    elif sample_columns == ['1', '3', '5', '7', '9', '11']:
        sample_racks = math.ceil(number_of_samples / 48)
elif sample_tube_type == 'tube_1.5mL':
    sample_racks = math.ceil(number_of_samples / 24)
elif sample_tube_type == 'plate_96':
    sample_racks = math.ceil(number_of_samples / 96)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'tapestation_reagents.py',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('A protocol for the 10x dilution of many primers.'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Dilute primers 10x - a protocol for the dilution of many primers
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    # Pipette tips   
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  
        10,                                  
        '20tips_1')        
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  
        7,                                  
        '20tips_2')    
    tips_20 = [tips_20_1, tips_20_2]
        
    # Pipettes          
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  
        'left',                             
        tip_racks=tips_20)
    
    # Labware
    reagent_tube = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        1,
        'reagent_tube')
    
    destination_plate = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        
        3,                                      
        'destination_plate')  
    
    if sample_tube_type == 'tube_1.5mL':
        sample_source_1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            11,
            'sample_source_1')
        sample_source_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            8,
            'sample_source_2')
        sample_source_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            5,
            'sample_source_3')
        sample_source_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            2,
            'sample_source_4')
    
    if sample_tube_type == 'plate_96':
        sample_source_1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            11,                                  
            'sample_source_1')
        sample_source_2 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            8,                                  
            'sample_source_2')
    
    if sample_tube_type == 'PCR_strips':
        if simulate:
    
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            if sample_racks >= 1:
                sample_source_1 = protocol.load_labware_from_definition(
                    labware_def_pcrstrips,
                    11,
                    'sample_source_1')
            if sample_racks >= 2:
                sample_source_2 = protocol.load_labware_from_definition(
                    labware_def_pcrstrips,
                    8,
                    'sample_source_2')
            if sample_racks >= 3:
                sample_source_3 = protocol.load_labware_from_definition(
                    labware_def_pcrstrips,
                    5,
                    'sample_source_3')
            if sample_racks >= 4:
                sample_source_4 = protocol.load_labware_from_definition(
                    labware_def_pcrstrips,
                    2,
                    'sample_source_4')
        else:
            if sample_racks >= 1:
                sample_source_1 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    11,                                      
                    'sample_source_1') 
            if sample_racks >= 2:
                sample_source_2 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    8,                                      
                    'sample_source_2') 
            if sample_racks >= 3:
                sample_source_3 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    5,                                      
                    'sample_source_3')
            if sample_racks >= 4:
                sample_source_4 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    2,                                      
                    'sample_source_4') 
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    # Setting starting tip                                           
    p20.starting_tip = tips_20_1.well(starting_tip_p20)     
    
    # Destination wells
    destination_wells = []
    for well in destination_plate.wells():
        destination_wells.append(well)
    sample_wells = destination_wells[:number_of_samples]
    
    # Name the well where the reagent tube is
    reagent_source = reagent_tube.wells_by_name()['A1']
    
    # Create an empty list to append the wells for the sample_sources to
    sample_sources = []
    sample_sources_string = []

    # Add wells to the list of sample sources, if plate_96
    if sample_tube_type == 'plate_96':
        if sample_racks >= 1:
            for well in sample_source_1.wells():
                sample_sources.append(well)
                sample_sources_string.append(str(well))
        if sample_racks >= 2:
            for well in sample_source_2.wells():
                sample_sources.append(well)
                sample_sources_string.append(str(well))
    # Add wells to the list of sample sources, if 1.5mL_tubes
    if sample_tube_type == '1.5mL_tubes':            
        if sample_racks >= 1:
            for well in sample_source_1.wells():
                sample_sources.append(well)
                sample_sources_string.append(str(well))
        if sample_racks >= 2:
            for well in sample_source_2.wells():
                sample_sources.append(well)
                sample_sources_string.append(str(well))
        if sample_racks >= 3:
            for well in sample_source_3.wells():
                sample_sources.append(well)
                sample_sources_string.append(str(well))
        if sample_racks >= 4:
            for well in sample_source_4.wells():
                sample_sources.append(well)
                sample_sources_string.append(str(well))
    # Add columns to a list of columns
    if sample_tube_type == 'pcr_strips':
        sample_source_columns = (
                ([sample_source_1.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
        if sample_racks >= 2:
            sample_columns_2 = (
                ([sample_source_2.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_2:
                sample_source_columns.append(column)
        if sample_racks >= 3:
            sample_columns_3 = (
                ([sample_source_3.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_3:
                sample_source_columns.append(column)
        if sample_racks >= 4:
            sample_columns_4 = (
                ([sample_source_4.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_4:
                sample_source_columns.append(column)
          ## Make a list of columns, this is a list of lists!   
        for column in sample_source_columns:
            for well in column:
                sample_sources.append(well)
                sample_sources_string.append(str(well))
              ## Separate the columns into wells and append them to list 
              
    ## Cut slice out off list of sample_sources, starting with the 
    ## indicated first sample and ending after the number_of_samples                        
    first_sample_index = sample_sources_string.index(
        first_sample + ' of sample_source_1 on 11')
      ## Determine the index of the first sample in the list made from 
      ## strings -- we cannot find strings in the normal robot list
      ## so we needed to convert the wells to strings.
    slice_sample_sources = slice(
        first_sample_index, 
        first_sample_index + number_of_samples)
      ## Determine the slice 
    ## Cut sample slice out of sample_source_wells list
    sample_sources = sample_sources[slice_sample_sources]
# =============================================================================      

# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.pause("You will need " + str(volume_of_buffer) + "uL of the " +
                   tapestation_kit + " reagent buffer in"
                   " a 1.5mL tube on A1 of the reagent tube rack.")              
# =============================================================================


## PIPETTING===================================================================
## ============================================================================
## Variables for volume tracking and aliquoting--------------------------------
    aspiration_vol = buffer_vol + (buffer_vol/100*2)
      ## The aspiration_vol is the volume (µL) that is aspirated from the   
      ## container.         
    dispension_vol = buffer_vol                                                
    ##### Variables for volume tracking
    start_height = vt.cal_start_height('tube_1.5mL', volume_of_buffer)
      ## Call start height calculation function from volume tracking module.
    current_height = start_height
      ## Set the current height to start height at the beginning of the     
      ## protocol.                                                          
    sample_mix_vol = sample_vol + 3
     ## setting the sample_mix_vol = volume for pipetting up and down    
    source = reagent_source
      ## setting the reagent source
    destination = sample_wells
    current_height = start_height
    container = 'tube_1.5mL'
    pipette = p20 
## ---------------------------------------------------------------------------- 
## Aliquoting water------------------------------------------------------------
    for i, well in enumerate(destination):
      ## aliquot in the correct wells, for each well do the following:  
        if i == 0: 
            pipette.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    
        elif i % 8 == 0:
            pipette.drop_tip()
            pipette.pick_up_tip()
              ## Then, after every 8th well, drop tip and pick up new      
        
        current_height, pip_height, bottom_reached = vt.volume_tracking(
            container, buffer_vol, current_height)
              ## call volume_tracking function, obtain current_height,      
              ## pip_height and whether bottom_reached.                     
        
        if bottom_reached:
            ## continue with next tube, reset vt                            
            current_height = start_height
            current_height, pip_height, bottom_reached = (
                vt.volume_tracking(
                    container, buffer_vol, current_height))
            aspiration_location = source.bottom(current_height)
       
        else:
            aspiration_location = source.bottom(pip_height)
              ## Set the location of where to aspirate from.                
        
        #### The actual aliquoting
        pipette.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the set volume from the source                        
        pipette.dispense(dispension_vol, well.bottom(-1))
          ## dispense the set volume + extra to avoid drops in the well     
        pipette.dispense(10, aspiration_location)
          ## Alternative for blow-out                                        
    pipette.drop_tip()
      ## when entire plate is full, drop tip                               
## ----------------------------------------------------------------------------        
## Adding samples stocks--------------------------------------------------------         
    for sample_source, sample_well in zip(sample_sources, sample_wells):
        p20.pick_up_tip()
        p20.aspirate(sample_vol, sample_source)
        p20.dispense(sample_vol, sample_well)
        p20.mix(3, sample_mix_vol, sample_well)
        p20.dispense(20, sample_well)
        p20.drop_tip()
## ----------------------------------------------------------------------------    
## ============================================================================
 