"""
VERSION: V_Jan21
general_(q)PCR.py is a protocol written for EVE for the adding of mastermix 
and samples to a 96-wells plate.

You have to provide:
    Location of the starting tips in both the P20 and P200
    Number of samples (excl. NTC, standard sample, standard dilutions)
    Number of NTCs 
        NOTE: The NTC should ALWAYS be at the end of the plate
    Volume of your mastermix
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

When not doing a qPCR:
    Lights are turned on and off
    Mastermix is aliquoted from the mastermix tube into the plate
    Samples are added from the sample sources to the plate 

In addition for the qPCR:
    The lights are not turned on and off
    If standard sample: the last sample well is added number of standard 
    samples times.
        NOTE: the standard series are pipetted into the last 3 columns of 
        the plate. The standard sample is pipetted in the wells directly 
        following the sample wells (incl. NTC and mock).

In addition for replicates:
    You can indicate if you want your samples replicated in the PCR.
    This will only replicate the samples.
    This will add all samples once first and after that add them all
    again. 
    NTCs, std_samples and std_dilution_series come after the replicates
    
It is also possible to do a so-called 'redo' PCR. If you set this variable
to True the protocol doesn't take samples from the regular sample sources 
(so starting in the top left corner, A1, B1, C1... etc. ), but from the wells
specified by you! This is only neccessary when using a plate or strips, 
for 1.5mL tubes you can change the location. 
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'D9'
# If mastermix dispense > 19: What is the starting position of the 200µL tips?
starting_tip_p200 = 'A1'
  ## If not applicable, you do not have to change anything
  
# How many samples do you want to include?
number_of_samples = 5     
  ## MAX ==  number of samples -                                 
  ##         (number of std series * length of std series) -     
  ##         number of standard sample replicates

# How many NTCs to include 
number_of_NTCs = 1 
  ## NOTE: The NTC come after samples and std_samples                     

# What is the total volume (µL) of your mix?
start_vol = 1500
  ## The start_vol_m is the volume (µL) of mix that is in the source        
  ## labware at the start of the protocol.  
  
# Are you doing a qPCR or a regular PCR?
qPCR = False
  ## True or False                                                          
  ## Lights off if qPCR, standard sample and/or standard dilution series 
if qPCR:  
    # How many dilution serie replicates do you want to include?
    number_of_std_series = 2 
      ## If none -- fill in 0
    # How many dilutions are in the standard dilution series?
    length_std_series = 8
      ## length_of_std_series  MAX == 8                                     
    # How many replicates of the standard sample are you taking?
    number_of_std_samples = 0
else:
    ## If we are not doing a qPCR - protocol uses these values.             
    number_of_std_series = 0  
    length_std_series = 0
    number_of_std_samples = 0

# Which tube are you using for your mastermix? (options 1.5mL or 5mL)
mastermix_tube_type = 'tube_5mL'
  ## For volume < 1300: 'tube_1.5mL'                                        
  ## For volume > 1300: 'tube_5mL'     
# Where is the mastermix tube located in the rack? 
mastermix_source = 'C1'
  ## convenient places:
  ## if mastermix_tube_type ==   'tube_1.5mL'  -->  D1 
  ## if mastermix_tube_type ==   'tube_5mL'    -->  C1 

# What is the volume (µL) of mastermix that needs to be dispensed?
dispension_vol = 18.8     

# What labware are your samples in?
sample_tube_type = 'PCR_strip'
  ## Samples in strips = 'PCR_strip'                                       
  ## Primers in plate = 'plate_96'  
  ## Samples in 1.5mL tubes = 'tube_1.5mL'                                         
# In which columns are the strips in the plate (ignore if not using strips)?
sample_columns = ['2', '5', '8','11']
  ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
  ## max 4 racks with strips!  
# What is the volume (µL) of sample that needs to be added to the mix?
sample_vol = 1.2
  ## MAX = 17µL
# What is the location of your first sample (fill in if you have a plate)?                                    
first_sample = 'A2'
  ## 'A1' is standard for tubes and plates. 
  ## 'A2' is standard for tube_strips
  ## But if you have more samples in the plate than
  ## fit in the qPCR, change the first well position.

# Are you doing a redo PCR?
redo = False
  ## True or false
if redo:
    samples_sample_source_1 = (
        ['F3','A5'])
    samples_sample_source_2 = (
        [])
    samples_sample_source_3 = (
        [])
    samples_sample_source_4 = (
        [])
  ## Fill in the wells that your samples need to go in

# Do yu want your samples in duplicate or triplicate?
replicates = 1
  ## If you want all samples to be included in duplicate or triplicate (or more)
  ## indicate that here. replicates = 1, means every sample is added once.
  ## Replicated = 2, means every sample is added in duplo
  ## Replicates = 3, means every sample is added im trplo, etc...
  ## Replicates come after the entire sample set, before NTCs, std_samples and
  ## dilution series.
  ## Only the samples will be replicated, not the NTC, std_samples, std_dilution_series
  
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
if number_of_std_samples >= 1:
    total_number_of_samples = number_of_samples + 1
      ## If a standard sample is taken, add 1 to the total number of samples
else:
    total_number_of_samples = number_of_samples

if sample_tube_type == 'tube_1.5mL':
    samples_per_rack = 24
if sample_tube_type == 'plate_96':
    samples_per_rack = 96
if sample_tube_type == 'PCR_strip':
    samples_per_rack = 8 * len(sample_columns)
sample_racks = math.ceil(total_number_of_samples / samples_per_rack)
  ## How many tube_strip_racks are needed (1,2 or 3)

aspiration_vol = dispension_vol + (dispension_vol/100*2)
  ## The aspiration_vol is the volume (µL) that is aspirated from the   
      ## container.    
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
    if aspiration_vol > 20:
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
    if aspiration_vol > 20:
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
    if aspiration_vol > 20:
        ## If the mm volume to be dispendsed >= 19, assign p300 starting tip
        p300.starting_tip = tips_200.well(starting_tip_p200)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
    
    # Mastermix tube location
    MasterMix = mastermix_tube[mastermix_source]
    
    # Make a list of all possible wells in the destination plate
    destination_wells = []
    for well in destination_plate.wells():
        destination_wells.append(well)
    # Create a list of wells where samples should go
    sample_wells = destination_wells[:number_of_samples*replicates]
    
    #Create a list of wells where standard sample replicates should go
    slice_std_sample_wells = slice(
        (number_of_samples * replicates), (number_of_samples * replicates)+ number_of_std_samples)
    std_sample_wells = destination_wells[slice_std_sample_wells]
      ## Slice the list after the number of samples, and after the number
      ## of standard sample replicates to retrieve the wells in between
    
    # Create the list of wells where NTCs should go
    slice_NTC_wells = slice(
        (number_of_samples * replicates)+ number_of_std_samples,
        (number_of_samples * replicates)+ number_of_std_samples + number_of_NTCs)
    NTC_wells = destination_wells[slice_NTC_wells]
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
    
    if redo:
        ## This is the part of the protocol that accesses the specific
        ## sample wells specified in the variables to set
        ## NOTE: this only works for 96wells plate, when you need to redo 
        ## samples with other labware you can rearrange the order of tubes
        sample_sources = []
        wells_sample_source_1 = (
            [sample_source_1.wells_by_name()[well_name] for well_name in
            samples_sample_source_1])
        for well in wells_sample_source_1:
            sample_sources.append(well)
        wells_sample_source_2 = (
            [sample_source_2.wells_by_name()[well_name] for well_name in
            samples_sample_source_2])
        for well in wells_sample_source_2:
            sample_sources.append(well)
        wells_sample_source_3 = (
            [sample_source_3.wells_by_name()[well_name] for well_name in
            samples_sample_source_3])
        for well in wells_sample_source_3:
            sample_sources.append(well)
        wells_sample_source_4 = (
            [sample_source_4.wells_by_name()[well_name] for well_name in
            samples_sample_source_4])
        for well in wells_sample_source_4:
            sample_sources.append(well)
        
    else: 
        ## This is the part of the protocol that access the sample wells in
        ## a normal PCR (where you don't need to access specific wells)
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

        ## Determine position of the std_sample
        slice_std_sample = slice(
            first_sample_index + number_of_samples,
            first_sample_index + number_of_samples + 1)
        ## If you have a std sample included, this will be added as the last sample  
        std_source = sample_source_wells[slice_std_sample] * number_of_std_samples
          ## Makes a list of len number_of_std_samples of the std_source well
        
        ## Cut sample slice out of sample_source_wells list
        sample_sources = sample_source_wells[slice_sample_sources]
        ## If replicates are desired, this copies the sample_sources list
        sample_sources = sample_sources * replicates
       
        ## If you have a std sample included, this will add the std_samples 
        ## to the end of the sample_sources list
        sample_sources = sample_sources + std_source
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
## LIGHTS----------------------------------------------------------------------
    if not qPCR:
        protocol.set_rail_lights(False)
# ----------------------------------------------------------------------------
# =============================================================================