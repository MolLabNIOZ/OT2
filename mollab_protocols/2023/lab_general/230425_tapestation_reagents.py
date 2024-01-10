"""
Version: V_Aug22

tapestation_reagents.py is a protocol written to add the reagents of any
TapeStation assay from a 1.5mL tube to a 96-wells plate and add the samples
from 1.5mL tubes, PCR strips or a 96-wells plate to the reagents. It is also
possible to do one of the 2.

You have to provide:
    starting_tip_p20
        You will only need 20uL tips because the volume is never higher.
        NOTE: this protocol uses TipOne filter tips.
    
The reagent tube should always be put in A1

## Updates
221206 (SV) - added different plates as labware cleaned up some unnecessary stuff
230425 (MB) - added the option to skipp samples
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the first 20µL tip?
starting_tip_p20 = 'B8'
  
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
sample_tubes = 'plate_96'
## Options: 
    #sample_tubes = 'plate_96' (BioRad skirted plate)
    #sample_tubes = 'cool_rack_plate_96' (BioRad skirted plate in Eppendorf cooler)
    #sample_tubes = 'NIOZ_plate_96' (BioRad skirted plate in NIOZ plate holder)
    #sample_tubes = 'non_skirted_plate_96' (Thermo non-skirted plate in BioRad skirted plate)
    #sample_tubes = 'PCR_strips' (Westburg flat-cap strips or similar in BioRad skirted plate)
    #sample_tubes = 'tubes_1.5mL' (any 1.5mL tubes)          

# When using PCR strips:
sample_columns = ['2', '5', '8', '11']
## Options: 
    #3 strips per rack: ['2', '7', '11'] 
    #4 strips per rack: ['2', '5', '8','11'] = STANDARD
    #6 strips per rack: ['1', '3', '5', '7', '9', '11']

# What is the location of your first sample? 
first_sample = 'A1'
  ## 'A1' is standard for tubes and plates. 
  ## 'A2' is standard for tube_strips
# Are there any other samples that you want to skip?
skipped_wells = [4,5,7,9,12,13,16,31,32,39,40,41,42,53,54,
                    56,57,58,59,68,70,71,72,73,78,79,84,86,87]
    ## This is the index of the samples, where the first sample = 0
    ## If you don't want to skip, set an empty list: skipped_wells = ([])
# How many samples do you have in total (minus the skipped-samples)
number_of_samples =  66   
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
    sample_mix_vol = 2
     ## setting the sample_mix_vol = volume for pipetting up and down    
if tapestation_kit == 'D5000':
    buffer_vol = 10
    sample_vol = 1
    sample_mix_vol = 5
if tapestation_kit == 'gDNA':
    buffer_vol = 10
    sample_vol = 1 
    sample_mix_vol = 5
if tapestation_kit == 'HS-D1000':
    buffer_vol = 2
    sample_vol = 2
    sample_mix_vol = 3
if tapestation_kit == 'HS-D5000':
    buffer_vol = 2
    sample_vol = 2
    sample_mix_vol = 3
if tapestation_kit == 'RNA':
    buffer_vol = 5
    sample_vol = 1
    sample_mix_vol = 3
if tapestation_kit == 'HS-RNA':
    buffer_vol = 1
    sample_vol = 2
    sample_mix_vol = 2.5

# What is the total volume of buffer that is needed for the amount of samples?
# +10µL for minimum volume in tube
volume_of_buffer_needed = buffer_vol * (number_of_samples + 10)
volume_of_buffer = volume_of_buffer_needed - 100

number_of_samples = number_of_samples + len(skipped_wells)

# How many sample racks are needed?   
if sample_tubes == 'PCR_strips':
    if sample_columns == ['2', '7','11']:
        sample_racks = math.ceil(number_of_samples / 24)
    elif sample_columns == ['2', '5', '8','11']:
        sample_racks = math.ceil(number_of_samples / 32)
    elif sample_columns == ['1', '3', '5', '7', '9', '11']:
        sample_racks = math.ceil(number_of_samples / 48)
elif sample_tubes == 'tubes_1.5mL':
    sample_racks = math.ceil(number_of_samples / 24)
elif (sample_tubes == 'plate_96' or 
      sample_tubes == 'cool_rack_plate_96' or 
      sample_tubes == 'NIOZ_plate_96' or 
      sample_tubes == 'non_skirted_plate_96'):
    sample_racks = math.ceil(number_of_samples / 96)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': '221208_tapestation_reagents.py',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('A protocol for distribution of TapeStation reagents and samples.'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    A protocol for the distribution of TapeStation reagents and samples. 
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    # Pipette tips
    if simulate:
        with open("labware/tipone_96_tiprack_20ul/"
                  "tipone_96_tiprack_20ul.json") as labware_file:
                labware_def_tipone_96_tiprack_20ul = json.load(labware_file)
        tips_20_1 = protocol.load_labware_from_definition(
            labware_def_tipone_96_tiprack_20ul,
            10,                                  
            'tipone_20tips_1')
        tips_20_2 = protocol.load_labware_from_definition(
            labware_def_tipone_96_tiprack_20ul,
            7,                                  
            'tipone_20tips_2')
    else:    
        tips_20_1 = protocol.load_labware(
            'tipone_96_tiprack_20uL',  
            10,                                  
            'tipone_20tips_1')        
        tips_20_2 = protocol.load_labware(
            'tipone_96_tiprack_20uL',  
            7,                                  
            'tipone_20tips_2')
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
        'reagent_tube_1.5mL')
    
    destination = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        
        3,                                      
        'destination_plate_96')  
    
    if sample_tubes == 'tubes_1.5mL':
        sample_source_1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            11,
            'sample_source_1_tubes_1.5mL')
        sample_source_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            8,
            'sample_source_2_tubes_1.5mL')
        sample_source_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            5,
            'sample_source_3_tubes_1.5mL')
        sample_source_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            2,
            'sample_source_4_tubes_1.5mL')
    
    if sample_tubes == 'plate_96':
        sample_source_1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            11,                                  
            'sample_source_1_plate_96')
        sample_source_2 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            8,                                  
            'sample_source_2_plate_96')
    if sample_tubes == 'cool_rack_plate_96':
        if simulate:
            with open("labware/biorad_qpcr_plate_eppendorf_cool_rack/"
                      "biorad_qpcr_plate_eppendorf_cool_rack.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            sample_source_1 = protocol.load_labware_from_definition( 
                labware_def_plate_holder,     
                11,     
                'sample_source_1_cool_rack_plate_96')                    
            sample_source_2 = protocol.load_labware_from_definition( 
                labware_def_plate_holder,     
                8,                         
                'sample_source_2_cool_rack_plate_96') 
        else:
            sample_source_1 = protocol.load_labware(
                'biorad_qpcr_plate_eppendorf_cool_rack',
                11,
                'sample_source_1_cool_rack_plate_96')
            sample_source_2 = protocol.load_labware(
                'biorad_qpcr_plate_eppendorf_cool_rack',
                8,
                'sample_source_2_cool_rack_plate_96')
    if sample_tubes == 'NIOZ_plate_96':
        if simulate:
            with open("labware/biorad_qpcr_plate_nioz_plateholder/"
                      "biorad_qpcr_plate_nioz_plateholder.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            sample_source_1 = protocol.load_labware_from_definition( 
                labware_def_plate_holder,     
                11,                         
                'sample_source_1_NIOZ_plate_96')
            sample_source_2 = protocol.load_labware_from_definition( 
                labware_def_plate_holder,     
                8,                         
                'sample_source_2_NIOZ_plate_96')   
        else:        
            sample_source_1 = protocol.load_labware(
                'biorad_qpcr_plate_nioz_plateholder',
                11,
                'sample_source_1_NIOZ_plate_96')        
            sample_source_2 = protocol.load_labware(
                'biorad_qpcr_plate_nioz_plateholder',
                8,
                'sample_source_2_NIOZ_plate_96')
    if sample_tubes == 'non_skirted_plate_96':
        if simulate:
            with open("labware/thermononskirtedinbioradskirted_96_wellplate_200ul/"
                      "thermononskirtedinbioradskirted_96_wellplate_200ul.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            sample_source_1 = protocol.load_labware_from_definition( 
                labware_def_plate_holder,     
                11,                         
                'sample_source_1_non_skirted_plate_96')   
            sample_source_2 = protocol.load_labware_from_definition( 
                labware_def_plate_holder,     
                8,                         
                'sample_source_2_non_skirted_plate_96')   
        else:
            sample_source_1 = protocol.load_labware(
                'thermononskirtedinbioradskirted_96_wellplate_200ul',
                11,
                'sample_source_1_non_skirted_plate_96')        
            sample_source_2 = protocol.load_labware(
                'thermononskirtedinbioradskirted_96_wellplate_200ul',
                8,
                'sample_source_2_non_skirted_plate_96')            
    if sample_tubes == 'PCR_strips':
        if simulate:
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            sample_source_1 = protocol.load_labware_from_definition(
                    labware_def_pcrstrips,
                    11,
                    'sample_source_1_PCR_strips')
            sample_source_2 = protocol.load_labware_from_definition(
                    labware_def_pcrstrips,
                    8,
                    'sample_source_2_PCR_strips')
            sample_source_3 = protocol.load_labware_from_definition(
                    labware_def_pcrstrips,
                    5,
                    'sample_source_3_PCR_strips')
            sample_source_4 = protocol.load_labware_from_definition(
                    labware_def_pcrstrips,
                    2,
                    'sample_source_4_PCR_strips')
        else:
            sample_source_1 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    11,                                      
                    'sample_source_1_PCR_strips') 
            sample_source_2 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    8,                                      
                    'sample_source_2_PCR_strips') 
            sample_source_3 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    5,                                      
                    'sample_source_3_PCR_strips')
            sample_source_4 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    2,                                      
                    'sample_source_4_PCR_strips') 
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    # Setting starting tip                                           
    p20.starting_tip = tips_20_1.well(starting_tip_p20)     
    
    # Destination wells
    destination_wells = []
    for well in destination.wells():
        destination_wells.append(well)
    sample_wells = destination_wells[:number_of_samples - len(skipped_wells)]
    
    # Name the well where the reagent tube is
    reagent_source = reagent_tube.wells_by_name()['A1']
    
    # Create an empty list to append the wells for the sample_sources to
    sample_sources = []
    sample_sources_string = []

    if sample_tubes == 'PCR_strips':
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
    else:          
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
              
    ## Cut slice out off list of sample_sources, starting with the 
    ## indicated first sample and ending after the number_of_samples                        
    first_sample_index = sample_sources_string.index(
        first_sample + ' of sample_source_1_' + sample_tubes + ' on 11')
      ## Determine the index of the first sample in the list made from 
      ## strings -- we cannot find strings in the normal robot list
      ## so we needed to convert the wells to strings.
    slice_sample_sources = slice(
        first_sample_index, 
        first_sample_index + number_of_samples)
      ## Determine the slice 
    ## Cut sample slice out of sample_source_wells list
    sample_sources = sample_sources[slice_sample_sources]
    ## Remove wells to skipp
    for index in sorted(skipped_wells, reverse=True):
        del sample_sources[index]
        # In reverse order, so that the index does not shift
# =============================================================================      

# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.pause("You will need " + str(volume_of_buffer_needed) + "uL of the " +
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
    if start_height < 20:
        start_height = 0
    current_height = start_height
      ## Set the current height to start height at the beginning of the     
      ## protocol.                                                          
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
        if start_height >= 20:
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
        else:
            aspiration_location = source
              ## Set the location of where to aspirate from.
        
        #### The actual aliquoting
        pipette.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the set volume from the source                        
        pipette.dispense(dispension_vol, well)
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
 