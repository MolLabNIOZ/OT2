"""
VERSION: V_June22
equimolar_pooling.py is a protocol for pooling samples in equimolar amounts.
First use get_uL_info to get a list of volumes per sample to add to the pool.
Copy that list into this protocol and run this protocol on the OT2

Samples can be provided in a PCR plate, PCR strips or 1.5mL tubes.

You have to provide:
    List with sample volumes 
        make sure the order is similar to the sample orientation
    Location of the starting tip in P20 or P200
    Type of tubes the samples are in
    
The protocol will tell you what tube the pool will be made in.
You need to add buffer PB before the start, so that there is already some 
liquid to pipet small volumes in. The protocol will tell you how much

Updates:
    SV 221201: 
        deleted all offset things
        changed indention levels
        changed the name of plate_96 to NIOZ_plate_96 (because we are using the plate holder)
        added non_skirted_plate_96
    MB 221213:
        changed to tipone 20µL tips and 300µL tips outcommented but ready
    MB 230504:
        Added to option to use a sample plate without NIOZ holder
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the tips?
starting_tip_p20 = 'A1'
starting_tip_p200 = 'A1'

# Use get_uL_info.py to get a list of volumes
DNA_µL_list = ([18.05, 30.4, 42.74, 69.93, 0.0, 0.0, 25.71, 0.0, 8.85, 0.0, 50.25, 9.26, 0.0, 0.0, 15.55, 42.55, 0.0, 14.75, 70.0, 70.0, 70.0, 47.17, 19.92, 70.0, 40.98, 66.23, 33.9, 70.0, 70.0, 9.26, 22.57, 0.0, 0.0, 1.55, 70.0, 16.05, 2.39, 48.08, 15.82, 0.0, 0.0, 0.0, 0.0, 70.0, 4.24, 70.0, 23.15, 37.88, 7.14, 4.61, 2.77, 70.0, 31.45, 0.0, 0.0, 70.0, 0.0, 0.0, 0.0, 0.0, 70.0, 70.0, 66.67, 45.25, 39.37, 70.0, 70.0, 27.78, 0.0, 10.66, 0.0, 0.0, 0.0, 0.0, 70.0, 37.17, 53.19, 56.5, 0.0, 0.0, 67.57, 19.69, 23.7, 15.22, 0.0, 69.44, 0.0, 0.0, 70.0, 70.0, 70.0, 70.0, 70.0, 0.43, 70.0, 0.0])

# Specify the number of samples, to check if the number of volumes is correct    
number_of_samples = 96

# What labware are your samples in?
sample_tube_type = 'plate_96' 
  ##Options:
# sample_tube_type = 'plate_96' (BioRad skirted plate)
# sample_tube_type = 'NIOZ_plate_96' (BioRad skirted plate on NIOZ plate holder)
# sample_tube_type = 'non_skirted_plate_96' (Thermo plate on BioRad plate)
# sample_tube_type = 'PCR_strips'                                        
# sample_tube_type = 'tube_1.5mL'  

if sample_tube_type == 'PCR_strips':
    # In which columns are the strips in the plate (ignore if not using strips)?
    sample_columns = ['2', '5', '8', '11']
      ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
      ## max 4 racks with strips!  

# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol
# =============================================================================

# IMPORT STATEMENTS AND FILES==================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.
import math
  ## To do some calculations 

if simulate: #Simulator
    from mollab_modules import volume_tracking_v2 as vt
    import json 
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.     
else: #Robot
    from data.user_storage.mollab_modules import volume_tracking_v2 as vt
# If not simulated, import the .csv from the robot with robot_specific 
# labware off_set values
    # offsets = pd.read_csv(
    #     "data/user_storage/mollab_modules/labware_offset.csv", sep=';'
    #     )
    #   ## import .csv
    # offsets = offsets.set_index('labware')
      ## remove index column
# =============================================================================

# CALCULATED VARIABLES=========================================================
# ============================================================================= 
# Raise exception when number of volumes and number of samples are different
if len(DNA_µL_list) != number_of_samples:
    raise Exception(
        "The number of volumes provided"
        " is not equal to the given number of samples!")

# Calculate the total pool volume
total_pool_volume = sum(DNA_µL_list)

# calculate total_pool_volume + buffer to add for clean-up 
# to determine what kind of tube to use
PB_volume = total_pool_volume * 5
total_cleanup_volume = total_pool_volume + PB_volume

# Based on total_cleanup_volume, determine tube to pool in
if total_cleanup_volume <= 1500:
    pool_tube_type = 'tube_1.5mL'
elif total_cleanup_volume <=5000:
    pool_tube_type = 'tube_5mL'
## NO OFFSETS YET!
# else:
#     raise Exception("There are no offsets available for 15mL/50mL tubes")
elif total_cleanup_volume <=15000:
    pool_tube_type = 'tube_15mL'
else:
    pool_tube_type = 'tube_50mL'

# Info for comment about how many tubes with how much PB to insert
# And to keep track if more than 1 tube is needed
amount_of_tubes = math.ceil(total_cleanup_volume/50000)
PB_volume = PB_volume / amount_of_tubes
pool_volume_per_tube = total_pool_volume / amount_of_tubes

# How many sample_tube_racks are needed
if sample_tube_type == 'tube_1.5mL':
    samples_per_rack = 24
if sample_tube_type == 'NIOZ_plate_96' or 'non_skirted_plate_96':
    samples_per_rack = 96
if sample_tube_type == 'PCR_strips':
    samples_per_rack = 8 * len(sample_columns)
sample_racks = math.ceil(number_of_samples / samples_per_rack)
  ## How many tube_racks are needed
if sample_racks > 5:
    raise Exception("Sorry, this protocol can only handle 5 sample racks")
# =============================================================================
#%%
# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'equimolar_pooling.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('pooling samples in equimolar amounts'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    pool samples together in different volumes
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading pipette tips
    
    if any(i >= 19 for i in DNA_µL_list):
        # if simulate:
            # with open("labware/tipone_96_tiprack_300ul/"
            #      "tipone_96_tiprack_300ul.json") as labware_file:
            #           labware_def_tipone_300ul = json.load(labware_file)
            # tips_200_1= protocol.load_labware_from_definition( 
            #     labware_def_tipone_300ul,           
            #     11,                         
            #     'tipone_300tips_1')
            # tips_200_2 = protocol.load_labware_from_definition( 
            #     labware_def_tipone_300ul,           
            #     10,                         
            #     'tipone_300tips_2')
        # else:     
            # tips_200_1 = protocol.load_labware(
            #     'tipone_96_tiprack_300ul',  
            #     11,                                  
            #     'tipone_300tips_1')
            # tips_200_2 = protocol.load_labware(
            #     'tipone_96_tiprack_300ul',  
            #     10,                                  
            #     'tipone_300tips_2'))
        tips_200_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  
            11,                                  
            '200tips_1')
        tips_200_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  
            10,                                  
            '200tips_2')
    
    if any(i < 19 for i in DNA_µL_list):
        if simulate:
            with open("labware/tipone_96_tiprack_20ul/"
                 "tipone_96_tiprack_20ul.json") as labware_file:
                      labware_def_tipone_20ul = json.load(labware_file)
            tips_20_1 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
                8,                         
                'tipone_20tips_1')
            tips_20_2 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
                7,                         
                'tipone_20tips_2')
        else:    
            tips_20_1 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                8,                                  
                'tipone_20tips_1')
            tips_20_2 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                7,                                  
                'tipone_20tips_2')
        
    ##### Loading labware
    ## Tube for pooling the samples in
    if pool_tube_type == 'tube_1.5mL':
        pool_tube = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            5,
            'pool_tube_1.5mL')
    elif pool_tube_type == 'tube_5mL':
        if simulate:
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                      "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                    labware_def_5mL = json.load(labware_file)
            pool_tube = protocol.load_labware_from_definition( 
                labware_def_5mL, 
                5, 
                'pool_tube_5mL')
        else:
            pool_tube = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                5,
                'pool_tube_5mL')
    elif pool_tube_type == 'tube_15mL':
        pool_tube = protocol.load_labware(
            'opentrons_15_tuberack_falcon_15ml_conical',
            5,
            'pool_tube_15mL')
    elif pool_tube_type == 'tube_50mL':
        pool_tube = protocol.load_labware(
            'opentrons_6_tuberack_falcon_50ml_conical',
            5,
            'pool_tube_50mL')

    ## Tubes to get samples from
    if sample_tube_type == 'NIOZ_plate_96':
        if simulate:
            with open("labware/biorad_qpcr_plate_nioz_plateholder/"
                      "biorad_qpcr_plate_nioz_plateholder.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            samples1 = protocol.load_labware_from_definition( 
                labware_def_plate_holder,     
                6,                         
                'samples1_NIOZ_plate_96')
            if sample_racks > 1:
                samples2 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    3,                         
                    'samples2_NIOZ_plate_96')
            if sample_racks > 2:
                samples3 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    2,                         
                    'samples3_NIOZ_plate_96')
            if sample_racks > 3:
                samples4 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    1,                         
                    'samples4_NIOZ_plate_96')
            if sample_racks > 4:
                samples5 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    4,                         
                    'samples5_NIOZ_plate_96')
        else:    
            samples1 = protocol.load_labware(
                'biorad_qpcr_plate_nioz_plateholder',
                6,
                'samples1_NIOZ_plate_96')
            if sample_racks > 1:
                samples2 = protocol.load_labware(
                    'biorad_qpcr_plate_nioz_plateholder',
                    3,
                    'samples2_NIOZ_plate_96')
            if sample_racks > 2:
                samples3 = protocol.load_labware(
                    'biorad_qpcr_plate_nioz_plateholder',
                    2,
                    'samples3_NIOZ_plate_96')
            if sample_racks > 3:
                samples4 = protocol.load_labware(
                    'biorad_qpcr_plate_nioz_plateholder',
                    1,
                    'samples4_NIOZ_plate_96')
            if sample_racks > 4:
                samples5 = protocol.load_labware(
                    'biorad_qpcr_plate_nioz_plateholder',
                    4,
                    'samples5_NIOZ_plate_96')
                
    if sample_tube_type == 'plate_96':
        samples1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            6,
            'samples1_plate_96')
        if sample_racks > 1:
            samples2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                3,
                'samples2_plate_96')
        if sample_racks > 2:
            samples3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                2,
                'samples3_plate_96')
        if sample_racks > 3:
            samples4 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                1,
                'samples4_plate_96')
        if sample_racks > 4:
            samples5 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                4,
                'samples5_plate_96')
        
    elif sample_tube_type == 'non_skirted_plate_96':
        if simulate:
            with open("labware/thermononskirtedinbioradskirted_96_wellplate_200ul/"
                      "thermononskirtedinbioradskirted_96_wellplate_200ul.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            samples1 = protocol.load_labware_from_definition( 
                labware_def_plate_holder,     
                6,                         
                'samples1_non_skirted_plate_96')
            if sample_racks > 1:
                samples2 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    3,                         
                    'samples2_non_skirted_plate_96')
            if sample_racks > 2:
                samples3 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    2,                         
                    'samples3_non_skirted_plate_96')
            if sample_racks > 3:
                samples4 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    1,                         
                    'samples4_non_skirted_plate_96')
            if sample_racks > 4:
                samples5 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    4,                         
                    'samples5_non_skirted_plate_96')
        else:    
            samples1 = protocol.load_labware(
                'thermononskirtedinbioradskirted_96_wellplate_200ul',
                6,
                'samples1_non_skirted_plate_96')
            if sample_racks > 1:
                samples2 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',
                    3,
                    'samples2_non_skirted_plate_96')
            if sample_racks > 2:
                samples3 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',
                    2,
                    'samples3_non_skirted_plate_96')
            if sample_racks > 3:
                samples4 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',
                    1,
                    'samples4_non_skirted_plate_96')
            if sample_racks > 4:
                samples5 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',
                    4,
                    'samples5_non_skirted_plate_96')
    
    elif sample_tube_type == 'PCR_strips':
        if simulate:
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            samples1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                6,                         
                'samples1_pcr_strips')
            if sample_racks > 1:
                samples2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips,     
                    3,                         
                    'samples2_pcr_strips')
            if sample_racks > 2:
                samples3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips,     
                    2,                         
                    'samples3_pcr_strips')
            if sample_racks > 3:
                samples4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips,     
                    1,                         
                    'samples4_pcr_strips')
            if sample_racks > 4:
                samples5 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips,     
                    4,                         
                    'samples5pcr_strips')
        else:
            samples1 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                6,                                     
                'samples1_pcr_strips')
            if sample_racks > 1:
                samples2 = protocol.load_labware( 
                    'pcrstrips_96_wellplate_200ul',        
                    3,                                     
                    'samples2_pcr_strips')
            if sample_racks > 2:
                samples3 = protocol.load_labware( 
                    'pcrstrips_96_wellplate_200ul',        
                    2,                                     
                    'samples3_pcr_strips')
            if sample_racks > 3:
                samples4 = protocol.load_labware( 
                    'pcrstrips_96_wellplate_200ul',        
                    1,                                     
                    'samples4_pcr_strips')
            if sample_racks > 4:
                samples5 = protocol.load_labware( 
                    'pcrstrips_96_wellplate_200ul',        
                    4,                                     
                    'samples5_pcr_strips')
        
    elif sample_tube_type == 'tube_1.5mL':
        samples1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            6,
            'samples1_tube_1.5mL')
        if sample_racks > 1:
            samples2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                3,
                'samples2_tube_1.5mL')
        if sample_racks > 2:
            samples3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                2,
                'samples3_tube_1.5mL')
        if sample_racks > 3:
            samples4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                1,
                'samples4_tube_1.5mL')
        if sample_racks > 4:
            samples5 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                4,
                'samples5_tube_1.5mL')
    
    ## Pipettes
    if any(i >= 19 for i in DNA_µL_list):
        p300 = protocol.load_instrument(
            'p300_single_gen2',             
            'right',                        
            tip_racks=[tips_200_1,tips_200_2]) 
    
    if any(i < 19 for i in DNA_µL_list):
        p20 = protocol.load_instrument(
            'p20_single_gen2',                  
            'left',                             
            tip_racks=[tips_20_1,tips_20_2])
# =============================================================================

# PREDIFINED VARIABLES=========================================================
# =============================================================================
    ##### Variables for volume tracking
    start_height = vt.cal_start_height(pool_tube_type, PB_volume)
      ## Call start height calculation function from volume tracking module.
    current_height = start_height
      ## Set the current height to start height at the beginning of the     
      ## protocol.                                                             
# =============================================================================    

# SETTING LOCATIONS============================================================
# =============================================================================
    # Setting starting tip    
    if any(i >= 19 for i in DNA_µL_list):
        p300.starting_tip = tips_200_1.well(starting_tip_p200)
    if any(i < 19 for i in DNA_µL_list):
        p20.starting_tip = tips_20_1.well(starting_tip_p20)
        
    # Make a list of all possible sample wells in the sample racks
    sample_wells = []
    
    # For PCR_strips this depends on the used columns
    if sample_tube_type == 'PCR_strips':
        sample_columns = (
            ([samples1.columns_by_name()[column_name] 
              for column_name in sample_columns]))
        if sample_racks > 1:
            sample_columns_2 = (
                ([samples2.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_2:
                sample_columns.append(column)
        if sample_racks > 2:
            sample_columns_3 = (
                ([samples3.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_3:
                sample_columns.append(column)
        if sample_racks > 3:
            sample_columns_4 = (
                ([samples4.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_4:
                sample_columns.append(column)
        if sample_racks > 4:
            sample_columns_5 = (
                ([samples5.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_5:
                sample_columns.append(column)
 
        for column in sample_columns:
            for well in column:
                sample_wells.append(well)
    
    # For plates and 1.5mL tubes, all wells should be included                      
    else:
        for well in samples1.wells():
            sample_wells.append(well)
            if sample_racks > 1:
                for well in samples2.wells():
                    sample_wells.append(well)
            if sample_racks > 2:
                for well in samples3.wells():
                    sample_wells.append(well)
            if sample_racks > 3:
                for well in samples4.wells():
                    sample_wells.append(well)
            if sample_racks > 4:
                for well in samples5.wells():
                    sample_wells.append(well)
    
    # Cut of sample_wells list after certain amount of samples
    sample_wells = sample_wells[:number_of_samples]
    
## PIPETTING===================================================================
## ============================================================================
## COMMENTS--------------------------------------------------------------------    
    protocol.pause("Insert " + str(amount_of_tubes) + " " + pool_tube_type + 
                   " containing " + str(round(PB_volume/1000,3)) + 
                   "mL PB buffer into "
                   "the appropriate rack on slot 5")
## ----------------------------------------------------------------------------   
## LIGHTS----------------------------------------------------------------------    
    protocol.set_rail_lights(True)
## ----------------------------------------------------------------------------
## THE ACTUAL POOLING----------------------------------------------------------
    pooled_volume = 1
    for volume, well in zip(DNA_µL_list, sample_wells):
        ## for each well do the following
        if volume > 0:
            # Determine pipette to use, depending on volume
            if volume < 19:
                pipette = p20
            else:
                pipette = p300
            
            # determine pipette_height in the pool_tube
            direction = 'filling'
            current_height, pip_height, bottom_reached = vt.volume_tracking(
                pool_tube_type, volume, current_height,direction)
            
            # Pick up a tip
            pipette.pick_up_tip()
            
            # Take up the specified volume per sample       
            pipette.aspirate(volume, well)
            
            # Take an air gap, to prevent cross_contamination
            pipette.aspirate(1, well.top())
            
            # Determine tube to pool in
            pool_tube_number = math.ceil(pooled_volume / pool_volume_per_tube) - 1     
            pool_tube_well = str(pool_tube.wells()[pool_tube_number])
            pool_tube_well = pool_tube_well.split(" ", 1)[0]
            
            # Dispense in the pool_tube, 
            pipette.dispense(volume + 10, pool_tube[pool_tube_well].bottom(pip_height))
            
            # Keep track of already pooled volume, to go to next tube if necesarry 
            pooled_volume = pooled_volume + volume
            
            # drop tip
            pipette.drop_tip()
## ============================================================================    
    
# TURN RAIL LIGHT OFF==========================================================
# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================    