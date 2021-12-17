"""
VERSION: V_Dec21
general_illumina_PCR_WALL-E.py is a protocol written for WALL-E for the adding
of mastermix and barcoded primers to a 96-wells plate

You have to provide:
    Number of samples (excl. NTC and mock)
    Number of NTCs 
        NOTE: The NTC should ALWAYS be at the end of the plate, this is
        for the protocol for EVE (who skips the last well)
    Do you want the robot to add a mock sample?:
        if True -- robot adds an extra well + primer combination
    Whether you are doing a qPCR or not 
    Volume of your mastermix
    Tube your mastermix is in (1.5mL or 5mL tube)
        (Location of your mastermix tube in the rack)
    Volume of the mastermix that is to be dispensed
    Tube your primers are in (PCR strips or 96-well plate)
        (If primers are in strips, you need to provide in which columns of
         the rack you are putting the strips. Usually columns 2, 5, 8 and 11
         are used)
    Volume of the primer that is to be dispensed
    
The number of unique primer combinations is based on the number of samples +
the number of NTCs + the mock. 

You can choose whether you want to do a qPCR or not.

When not doing a qPCR:
    Lights are turned on and off
    Mastermix is aliquoted from the mastermix tube into the plate
    Primers are added from the primer source to the plate 

In addition for the qPCR:
    The lights are not turned on and off
    Primer is added from a separate 1.5mL tube to the standard
    series and the standard sample wells. 
        NOTE: the standard series are pipetted into the last 3 columns of 
        the plate. The standard sample is pipetted in the wells directly 
        following the sample wells (incl. NTC and mock).

Updates:
(SV) 211027: 
    - added choice between 5mL or 1.5mL mm tube
(MB) 211203: 
    - use p20 instead of p300 for MM volumes <19µL
(SV) 211213: 
    - added choice between 96_well plate and primers as primer source
    - rearranged variables to set
    - primer for standards is added from a separate tube to standard series
    and standard sample
    - clean up
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# If mastermix dispense > 19: What is the starting position of the 200µL tips?
starting_tip_p200 = 'A1'
  ## If not applicable, you do not have to change anything
  
# How many samples do you want to include?
number_of_samples = 28   
  ## If NOT qPCR and NOT mock                                MAX == 95      
  ## If NOT qPCR but incl. mock                              MAX == 94      
  ## If qPCR    MAX ==  number of samples -                                 
  ##                    (number of std series * length of std series) -     
  ##                    number of standard sample replicates                

# How many NTCs to include 
number_of_NTCs = 1 
  ## NOTE: The NTC should ALWAYS be at the end of your plate!!              

# Will a mock sample be included?
mock = False
  ## True if mock has to be added by the robot.                             
  ## False if mock is not added by the robot.                               

# What is the total volume (µL) of your mix?
start_vol = 1108.8
  ## The start_vol_m is the volume (µL) of mix that is in the source        
  ## labware at the start of the protocol.                                  
  
# Are you doing a qPCR or a regular PCR?
qPCR = False
  ## True or False                                                          
  ## Lights off if qPCR, standard sample and/or standard dilution series                                        ##
if qPCR:
    # How many dilution serie replicates do you want to include?
    number_of_std_series = 1  
    # How many dilutions are in the standard dilution series?
    length_std_series = 8  
      ## length_of_std_series  MAX == 8                                     
    # How many replicates of the standard sample are you taking?
    number_of_std_samples = 6
    # In what well is the primer for the standards (sample and series) located?
    std_primer_loc = 'D1'
                   
else:
    ## If we are not doing a qPCR - protocol uses these values.             
    number_of_std_series = 0  
    length_std_series = 0
    number_of_std_samples = 0

# Which tube are you using for your mastermix? (options 1.5mL or 5mL)
mastermix_tube_type = 'tube_1.5mL'
  ## For volume < 1300: 'tube_1.5mL'                                        
  ## For volume > 1300: 'tube_5mL'                                          

# What is the volume (µL) of mastermix that needs to be dispensed?
dispension_vol = 19   

# Where is the mastermix tube located in the rack? 
mastermix_source = 'C1'
  ## convenient places:
  ## if mastermix_tube_type ==   'tube_1.5mL'  -->  D1 
  ## if mastermix_tube_type ==   'tube_5mL'    -->  C1
    
# What labware are your primers in?
primer_tube_type = 'PCR_strips'
  ## Primers in strips = 'PCR_strips'                                       
  ## Primers in plate = 'plate_96'                                          
# What is the volume (µL) of primer that needs to be added to the mix?
primer_vol = 1
# In which columns are the strips in the plate (ignore if not using strips)?
primer_loc = ['2', '7', '11']
  ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
  ## max 4 racks with strips!                                               
  
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
number_of_primers = number_of_samples + number_of_NTCs
  ## Calculate how many unique primer pairs are needed.                    
if mock:
    number_of_primers = number_of_primers + 1    
      ## If a mock is used, there should be 1 more unique primer pair.     
      
if primer_tube_type == 'PCR_strips':
    if len(primer_loc) == 3:
        primer_racks = math.ceil(number_of_primers / 24)  
    if len(primer_loc) == 4: 
        primer_racks = math.ceil(number_of_primers / 32)     
  ## How many tube_strip_racks are needed (1,2 or 3)

if primer_tube_type == 'plate_96':
    primer_racks = math.ceil(number_of_primers / 96)
  ## *this isn't really used yet as we also only add one sample plate
  ##  so for now we cannot add >primer pairs, but if we add another 
  ##  destination plate it would be possible -- didn't do this because
  ##  we don't have plates with more than 96 primer combinatons
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'general_illumina_PCR_WALL-E',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Illumina (q)PCR - aliquoting mix and primers '),
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
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        
        6,                                      
        'plate_96')   
    if qPCR:
        big_primer_source = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            8,
            'big_primer_source')                          
    
    if mastermix_tube_type == 'tube_1.5mL':
        mastermix_tube = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            3,
            'mastermix_tube')
    
    if primer_tube_type == 'plate_96':
        primer_source_1 = protocol.load_labware(
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
        if primer_tube_type == 'PCR_strips':
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            primer_source_1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                4,                         
                'primer_source_1')         
            if primer_racks >=2:
                primer_source_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    1,                     
                    'primer_source_2')    
            if primer_racks >=3:
                primer_source_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips,
                    11,                   
                    'primer_source_3')      
    else: #Robot
        if mastermix_tube_type == 'tube_5mL': 
            mastermix_tube = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                3,                                     
                'mastermix_tube')                               
        if primer_tube_type == 'PCR_strips':
            primer_source_1 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                4,                                     
                'primer_source_1')                      
            if primer_racks >=2:
                primer_source_2 = protocol.load_labware( 
                    'pcrstrips_96_wellplate_200ul',    
                    1,                                 
                    'primer_source_2')                 
            if primer_racks >=3:
                primer_source_3 = protocol.load_labware( 
                    'pcrstrips_96_wellplate_200ul',    
                    11,                                
                    'primer_source_3')  
           
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
    primer_mix_vol = primer_vol + 3
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

## PIPETTING===================================================================
## ============================================================================
## LIGHTS----------------------------------------------------------------------
    if qPCR:
        protocol.set_rail_lights(False)
    if not qPCR:
        protocol.set_rail_lights(True)
## ----------------------------------------------------------------------------
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
## ADDING PRIMERS FOR SAMPLES TO THE MIX---------------------------------------
    for primer_well, sample_well in zip(primer_wells, sample_wells):
      ## Loop trough primer_wells and sample_wells                          
        p20.pick_up_tip()
        p20.aspirate(primer_vol, primer_well)
        p20.dispense(primer_vol, sample_well)
        p20.mix(3, primer_mix_vol, sample_well)
        p20.dispense(10, sample_well)
        p20.drop_tip()       
## ----------------------------------------------------------------------------
## ADDING PRIMERS FOR STANDARDS TO THE MIX-------------------------------------
    for well in std_wells:
        p20.pick_up_tip()
        p20.aspirate(primer_vol, std_primer)
          ## use last primer pair for NTC and std series
        p20.dispense(primer_vol, well)
        p20.mix(3, primer_mix_vol, well)
        p20.dispense(10, well)
        p20.drop_tip()   
## ----------------------------------------------------------------------------
## LIGHTS----------------------------------------------------------------------
    if not qPCR:
        protocol.set_rail_lights(False)
# ----------------------------------------------------------------------------
## ============================================================================