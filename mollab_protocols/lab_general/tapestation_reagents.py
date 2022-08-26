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
# If applicable: What is the starting position of the first 20µL tip?
starting_tip_p20 = 'A1'
# If applicable: What is the starting position of the first 200µL tip?
starting_tip_p200 = 'A1'
  ## If volume-wise p20 or p200 is not applicable, this variable won't be used

# How many primers do you want to dilute? 
number_of_samples = 30
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
sample_tube_type = 'PCR_strip'
  ## Samples in strips = 'PCR_strip'                                       
  ## Samples in plate = 'plate_96'  
  ## Samples in 1.5mL tubes = 'tube_1.5mL'             
sample_columns = ['2', '7','11']
  ## optional:
  ##    3 strips per rack: ['2', '7', '11'] 
  ##    4 strips per rack: ['2', '5', '8','11']
  ##    6 strips per rack: ['1', '3', '5', '7', '9', '11']

first_sample = 'A1'
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
                                      
##### Import volume_tracking module 
# volume tracking module is imported inside the def
                                          
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
if tapestation_kit == 'D5000' or 'gDNA':
    buffer_vol = 10
    sample_vol = 1  
if tapestation_kit == 'HS-D1000' or 'HS-D5000':
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
    # IMPORT for simulator
    if not protocol.is_simulating(): 
        from data.user_storage.mollab_modules import volume_tracking_v1 as vt
    else:
        import json
        from mollab_modules import volume_tracking_v1 as vt
# =============================================================================

# OFFSETS======================================================================
# =============================================================================
    # If not simulated, import the .csv from the robot with robot_specific  
    # labware off_set values
    if not protocol.is_simulating():
        offsets = pd.read_csv(
            "data/user_storage/mollab_modules/labware_offset.csv", sep=';'
            )
          ## import .csv
        offsets = offsets.set_index('labware')
          ## remove index column
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    labwares = {}
 
    # Pipette tips   
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  
        10,                                  
        '20tips_1')        
    labwares[tips_20_1] = 'filtertips_20'                   
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  
        7,                                  
        '20tips_2')    
    labwares[tips_20_2] = 'filtertips_20'                                         
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
    labwares[reagent_tube] = '1.5mL_tubes'
    
    destination_plate = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        
        3,                                      
        'destination_plate')  
    labwares[destination_plate] = 'plate_96'
    
    if sample_tube_type == 'tube_1.5mL':
        sample_source_1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            2,
            'sample_source_1')
        labwares[sample_source_1] = '1.5mL_tubes'
        sample_source_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            5,
            'sample_source_2')
        labwares[sample_source_2] = '1.5mL_tubes'
        sample_source_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            8,
            'sample_source_3')
        labwares[sample_source_3] = '1.5mL_tubes'
        sample_source_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            11,
            'sample_source_4')
        labwares[sample_source_4] = '1.5mL_tubes'
    
    if sample_tube_type == 'plate_96':
        sample_source_1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            2,                                  
            'sample_source_1')
        labwares[sample_source_1] = 'plate_96'
        sample_source_2 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            5,                                  
            'sample_source_2')
        labwares[sample_source_2] = 'plate_96'
    
    if not protocol.is_simulating():
        if sample_racks >= 1:
            sample_source_1 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                11,                                      
                'sample_source_1') 
            labwares[sample_source_1] = 'pcr_strips'
        if sample_racks >= 2:
            sample_source_2 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                8,                                      
                'sample_source_2') 
            labwares[sample_source_2] = 'pcr_strips'
        if sample_racks >= 3:
            sample_source_3 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                5,                                      
                'sample_source_3')
            labwares[sample_source_3] = 'pcr_strips'
        if sample_racks >= 4:
            sample_source_4 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                2,                                      
                'sample_source_4') 
            labwares[sample_source_4] = 'pcr_strips'
    else:
        with open("labware/pcrstrips_96_wellplate_200ul/"
                  "pcrstrips_96_wellplate_200ul.json") as labware_file:
                labware_def_pcrstrips = json.load(labware_file)
        if sample_racks >= 1:
            sample_source_1 = protocol.load_labware_from_definition(
                labware_def_pcrstrips,
                11,
                'sample_source_1')
            labwares[sample_source_1] = 'pcr_strips'
        if sample_racks >= 2:
            sample_source_2 = protocol.load_labware_from_definition(
                labware_def_pcrstrips,
                8,
                'sample_source_2')
            labwares[sample_source_2] = 'pcr_strips'
        if sample_racks >= 3:
            sample_source_3 = protocol.load_labware_from_definition(
                labware_def_pcrstrips,
                5,
                'sample_source_3')
            labwares[sample_source_3] = 'pcr_strips'
        if sample_racks >= 4:
            sample_source_4 = protocol.load_labware_from_definition(
                labware_def_pcrstrips,
                2,
                'sample_source_4')
            labwares[sample_source_4] = 'pcr_strips'
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
    reagent_source = reagent_tube.wells_by_name('A1')
    
    # Create an empty list to append the wells for the sample_sources to
    sample_sources = []
    sample_sources_string = []

    # Add wells to the list of sample sources, if plate_96
    if sample_sources == 'plate_96':
        if sample_racks >= 1:
            for well in sample_source_1.wells():
                sample_sources.append(well)
                sample_sources_string.append(str(well))
        if sample_racks >= 2:
            for well in sample_source_2.wells():
                sample_sources.append(well)
                sample_sources_string.append(str(well))
    # Add wells to the list of sample sources, if 1.5mL_tubes
    if sample_sources == '1.5mL_tubes':            
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
    if sample_sources == 'pcr_strips':
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
            first_sample + ' of sample_source_1 on 2')
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

# LABWARE OFFSET===============================================================    
# =============================================================================
    if not protocol.is_simulating():
        for labware in labwares:
            offset_x = offsets.at[labwares[labware],'x_offset']
            offset_y = offsets.at[labwares[labware],'y_offset']
            offset_z = offsets.at[labwares[labware],'z_offset']
            labware.set_offset(
                x = offset_x, 
                y = offset_y, 
                z = offset_z)
# =============================================================================   

# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.pause("You will need " + str(volume_of_buffer) + " of the " +
                   tapestation_kit + " reagent buffer in"
                   " a 1.5mL tube on A1 of the reagent tube rack.")              
# =============================================================================
 
## PIPETTING===================================================================
## ============================================================================
## Variables for volume tracking and aliquoting--------------------------------
    source = reagent_source
    destination = primer_dilution_wells
    start_height = vt.cal_start_height('tube_5mL', 5000)
    current_height = start_height
    container = 'tube_5mL'
    if water_volume >= 19:
        pipette = p300
    else:
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
            container, water_volume, current_height)
              ## call volume_tracking function, obtain current_height,      
              ## pip_height and whether bottom_reached.                     
        
        if bottom_reached:
            ## continue with next tube, reset vt                            
            current_height = start_height
            current_height, pip_height, bottom_reached = (
                vt.volume_tracking(
                    container, water_volume, current_height))
            counter = counter + 1
            source = water_sources[counter]
            aspiration_location = source.bottom(current_height)
            protocol.comment(
            "Continue with tube " + str(counter + 1) + " of reagent")
       
        else:
            aspiration_location = source.bottom(pip_height)
              ## Set the location of where to aspirate from.                
        
        #### The actual aliquoting
        pipette.aspirate(water_volume, aspiration_location)
          ## Aspirate the set volume from the source                        
        pipette.dispense(water_volume + 10, well)
          ## dispense the set volume + extra to avoid drops in the well     
        pipette.dispense(10, aspiration_location)
          ## Alternative for blow-out                                        
    pipette.drop_tip()
      ## when entire plate is full, drop tip                               
## ----------------------------------------------------------------------------        
## Adding primer stocks--------------------------------------------------------         
    for primer_stock, primer_dilution in zip(
            primer_stock_sources, primer_dilution_wells):
        p20.pick_up_tip()
        p20.aspirate(primer_stock_volume, primer_stock)
        p20.dispense(primer_stock_volume, primer_dilution)
        primer_mix_volume = primer_stock_volume + 3 
        p20.mix(3, primer_mix_volume, primer_dilution)
        p20.dispense(20, primer_dilution)
        p20.drop_tip()
## ----------------------------------------------------------------------------    
## ============================================================================
 