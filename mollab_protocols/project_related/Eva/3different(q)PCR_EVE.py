"""
VERSION: V_Oct22
3different(q)PCR.py is a protocol written for EVE for the adding of 3 different
mastermixes and 3x the same samples to a 96-wells plate.
The plate will be devided in 3 equal parts 
(colums 1 to 4 is PCR1, columns 5 to 8 is PCR2, columns 9 to 12 is PCR3)
The first few spots per area are reserved for a std_dil_series 



You have to provide:
    Location of the starting tips in both the P20 and P200
    Number of samples (excl. NTC, standard sample, standard dilutions)
    Number of NTCs 
        NOTE: The NTC should ALWAYS be at the end of the plate
    Volume of your mastermixes
    Whether you are doing a qPCR or not
    Tube your mastermix is in (1.5mL or 5mL tube)
        (Location of your mastermix tube in the rack)
    Volume of the mastermix that is to be dispensed
    Tube your samples are in (PCR strips, 96-well plate, 1.5 mL tubes)
        (If samples are in strips, you need to provide in which columns of
         the rack you are putting the strips. Usually columns 2, 5, 8 and 11
         are used)
    Volume of the sample that is to be dispensed
    Location of the first sample
        This is the well where your first sample is located. Usually this is 
        A1, but when you have your samples in a plate and they don't all
        fit in one PCR you'll have to do another PCR with samples
        starting from a different sample. 
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol     
  
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# If mastermix dispense > 19: What is the starting position of the 200µL tips?
starting_tip_p200 = 'A1'
  ## If not applicable, you do not have to change anything                 

# What is the volume (µL) of mastermix that needs to be dispensed?
dispension_vol = 24  
# What is the total volume (µL) of your mix?
start_vol = 800
  ## The start_vol_m is the volume (µL) of mix that is in the source        
  ## labware at the start of the protocol.  
# Which tube are you using for your mastermix? (options 1.5mL or 5mL)
mastermix_tube_type = 'tube_1.5mL'
  ## For volume < 1300: 'tube_1.5mL'                                        
  ## For volume > 1300: 'tube_5mL'     
# Where is the mastermix tube located in the rack? 

# How many samples do you want to include?
number_of_samples = 23     
  ## MAX ==  32 - number_of_NTCs -                                 
  ##         (number of std series * length of std series) -     
  ##         number of standard sample replicates
# How many NTCs to include 
number_of_NTCs = 1 
  ## NOTE: The NTC come after samples and std_samples     
# What labware are your samples in?
sample_tube_type = 'tube_1.5mL'
  ## Samples in strips = 'PCR_strip'                                       
  ## Primers in plate = 'plate_96'  
  ## Samples in 1.5mL tubes = 'tube_1.5mL'                                         
# In which columns are the strips in the plate (ignore if not using strips)?
sample_columns = ['2', '5', '8','11']
  ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
  ## max 4 racks with strips!  
# What is the volume (µL) of sample that needs to be added to the mix?
sample_vol = 1
  ## MAX = 17µL
# What is the location of your first sample (fill in if you have a plate)?                                    
first_sample = 'A1'
  ## 'A1' is standard for tubes and plates. 
  ## 'A2' is standard for tube_strips
  ## But if you have more samples in the plate than
  ## fit in the qPCR, change the first well position.

# How many dilution serie replicates do you want to include?
number_of_std_series = 0 
  ## If none -- fill in 0
# How many dilutions are in the standard dilution series?
length_std_series = 0
  ## length_of_std_series  MAX == 8

# How many different PCRs do you want in 1 plate?
number_of_PCRs = 1
  ## Max 3. Provide as many mastermixes.  
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
total_number_of_samples = (
    number_of_samples + 
    number_of_NTCs + 
    (number_of_std_series * length_std_series))

if sample_tube_type == 'tube_1.5mL':
    samples_per_rack = 24
if sample_tube_type == 'plate_96':
    samples_per_rack = 96
if sample_tube_type == 'PCR_strip':
    samples_per_rack = 8 * len(sample_columns)
sample_racks = math.ceil(total_number_of_samples / samples_per_rack)
  ## How many tube_strip_racks are needed (1,2 or 3)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': '3different_qPCR',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('qPCR - aliquoting mix and samples'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    In a plate, Aliquoting 3 different mastermixes;
    Adding samples in 3fold from different labware.
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
        sample_source_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            5,
            'sample_source_2')
        sample_source_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            8,
            'sample_source_3')
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
    if sample_tube_type == 'PCR_strip':
        sample_source_1 = protocol.load_labware(
            'pcrstrips_96_wellplate_200ul',
            2,
            'sample_source_1')
        sample_source_2 = protocol.load_labware(
            'pcrstrips_96_wellplate_200ul',
            5,
            'sample_source_2')
        sample_source_3 = protocol.load_labware(
            'pcrstrips_96_wellplate_200ul',
            8,
            'sample_source_3')
        sample_source_4 = protocol.load_labware(
            'pcrstrips_96_wellplate_200ul',
            11,
            'sample_source_4')
        
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
            sample_source_2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, 
                5,                     
                'sample_source_2')    
            sample_source_3 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,
                8,                   
                'sample_source_3')    
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
            sample_source_2 = protocol.load_labware_( 
                'pcrstrips_96_wellplate_200ul',    
                5,                                 
                'sample_source_2')                 
            sample_source_3 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',    
                8,                                
                'sample_source_3') 
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
    MasterMix1 = mastermix_tube['A1']
    MasterMix2 = mastermix_tube['A2']
    MasterMix3 = mastermix_tube['A3']
    
    # Make a list of all possible wells in the destination plate
    MM_wells = []
    for well in destination_plate.wells():
        MM_wells.append(well)
    # Create a list of wells where samples should go
    MM1_wells = MM_wells[:total_number_of_samples]
    PCRs = {tuple(MM1_wells): MasterMix1}
    if number_of_PCRs > 1:
        MM2_wells = MM_wells[32:32 + total_number_of_samples]
        PCRs = {tuple(MM1_wells): MasterMix1, 
                tuple(MM2_wells): MasterMix2}
        if number_of_PCRs > 2:
            MM3_wells = MM_wells[64:64 + total_number_of_samples]
            PCRs = {tuple(MM1_wells): MasterMix1, 
                    tuple(MM2_wells): MasterMix2, 
                    tuple(MM3_wells): MasterMix3}
    
    # Where should sample go
    sample_slice = slice((number_of_std_series * length_std_series), 
                        (number_of_std_series * length_std_series) + number_of_samples)
    
    # Where are the samples located
    sample_source_wells = []
    sample_source_wells_string = []
      ## The string list is needed to be able to start at another well
    if sample_tube_type == 'tube_1.5mL' or sample_tube_type == 'plate_96':
        if sample_racks >= 1:
            for well in sample_source_1.wells():
                sample_source_wells.append(well)
                sample_source_wells_string.append(str(well))
        if sample_racks >= 2:
            for well in sample_source_2.wells():
                sample_source_wells.append(well)
                sample_source_wells_string.append(str(well))
        if sample_racks >= 3:
            for well in sample_source_3.wells():
                sample_source_wells.append(well)
                sample_source_wells_string.append(str(well))
        if sample_racks >= 4:
            for well in sample_source_4.wells():
                sample_source_wells.append(well)
                sample_source_wells_string.append(str(well))

    if sample_tube_type == 'PCR_strip':
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
                sample_source_wells.append(well)
                sample_source_wells_string.append(str(well))
          ## Separate the columns into wells and append them to list 
    ## Cut slice out off list of sample_sources, starting with the 
    ## indicated first sample and ending after the number_of_samples                        
    first_sample_index = sample_source_wells_string.index(
        first_sample + ' of sample_source_1 on 2')
      ## Determine the index of the first sample in the list made from 
      ## strings -- we cannot find strings in the normal robot list
      ## so we needed to convert the wells to strings.
    slice_sample_sources = slice(
        first_sample_index, 
        first_sample_index + number_of_samples)
      ## Determine the slice
      ## Cut sample slice out of sample_source_wells list
    sample_sources = sample_source_wells[slice_sample_sources]
# =============================================================================              
              
## PIPETTING===================================================================
## ============================================================================
## ALIQUOTING MASTERMIX--------------------------------------------------------
    if dispension_vol >= 19:
        pipette = p300
    else:
        pipette = p20
    
    for MM_wells in PCRs:
        current_height = start_height
        MMtube = PCRs[MM_wells]

        for i, well in enumerate(MM_wells):
          ## aliquot mix, for each well do the following:                       
            if i == 0: 
                pipette.pick_up_tip()
                  ## If we are at the first well, start by picking up a tip.    
            elif i % 16 == 0:
                pipette.drop_tip()
                pipette.pick_up_tip()
                  ## Then, after every 8th well, drop tip and pick up new       
        
            current_height, pip_height, bottom_reached = vt.volume_tracking(
                    mastermix_tube_type, dispension_vol, current_height)
                      ## call volume_tracking function, obtain current_height,  
                      ## pip_height and whether bottom_reached.                 
        
            if bottom_reached:
                aspiration_location = MMtube.bottom(z=1)
                protocol.comment("You've reached the bottom of the tube!")
                  ## If bottom is reached keep pipetting from bottom + 1        
            else:
                aspiration_location = MMtube.bottom(pip_height)
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

# ## ----------------------------------------------------------------------------
# ## ADDING SAMPLES--------------------------------------------------------------
    ## Loop through source and destination wells
    for MM_wells in PCRs:
        destination_wells = MM_wells[sample_slice]
        for sample_tube, well in zip(sample_sources, destination_wells):
            p20.pick_up_tip()
            p20.aspirate(sample_vol, sample_tube)
            p20.dispense(sample_vol, well)
            sample_mix_vol = sample_vol + 3
              ## primer_mix_vol = volume for pipetting up and down              
            p20.mix(3, sample_mix_vol, well)
            p20.dispense(10, well)
            p20.drop_tip()
# # -----------------------------------------------------------------------------
# # =============================================================================