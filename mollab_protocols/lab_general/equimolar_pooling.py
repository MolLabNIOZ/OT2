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
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the tips?
starting_tip_p20 = 'A1'
starting_tip_p200 = 'A1'

DNA_µL_list = ([4.0, 0.26666666666666666, 1.1111111111111112, 
                0.42105263157894735, 8.0, 0.4444444444444444, 
                1.0, 4.444444444444445, 13.333333333333334,  
                30.769230769230766])
number_of_samples = 12

if len(DNA_µL_list) != number_of_samples:
    raise Exception("the number of volumes provided is not equal to the given number of samples")

# What labware are your samples in?
sample_tube_type = 'plate_96' 
  ##Other options:
# sample_tube_type = 'PCR_strip'                                        
# sample_tube_type = 'tube_1.5mL'  

if sample_tube_type == 'PCR_strips':
    # In which columns are the strips in the plate (ignore if not using strips)?
    sample_columns = ['2', '7','11']
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
import pandas as pd
  ## For accessing offset .csv file
import math
  ## To do some calculations 
if simulate:
    import json
      ## For accessing custom labware
# =============================================================================

# CALCULATED VARIABLES=========================================================
# ============================================================================= 
# Calculate the total pool volume
total_pool_volume = sum(DNA_µL_list)

# calculate total_pool_volume + buffer to add for clean-up 
# to determine what kind of tube to use
total_cleanup_volume = total_pool_volume * 6

# Based on total_cleanup_volume, determine tube to pool in
if total_cleanup_volume <= 1500:
    pool_tube_type = 'tube_1.5mL'
elif total_cleanup_volume <=5000:
    pool_tube_type = 'tube_5mL'
## NO OFFSETS YET!
# elif total_cleanup_volume <=15000:
#     pool_tube_type = 'tube_15mL'
# elif total_cleanup_volume <=50000:
#     pool_tube_type = 'tube_50mL'    

# Check what pipette(s) + tips are needed
if any(i >= 19 for i in DNA_µL_list):
    p200 = True
if any(i < 19 for i in DNA_µL_list):
    p20 = True

# How many sample_tube_racks are needed
if sample_tube_type == 'tube_1.5mL':
    samples_per_rack = 24
if sample_tube_type == 'plate_96':
    samples_per_rack = 96
if sample_tube_type == 'PCR_strip':
    samples_per_rack = 8 * len(sample_columns)
sample_racks = math.ceil(number_of_samples / samples_per_rack)
  ## How many tube_racks are needed
if sample_racks > 5:
    raise Exception("Sorry, this protocol can only handle 5 sample racks")

# If not simulated, import the .csv from the robot with robot_specific 
# labware off_set values
if not simulate:
    offsets = pd.read_csv(
        "data/user_storage/mollab_modules/labware_offset.csv", sep=';'
        )
      ## import .csv
    offsets = offsets.set_index('labware')
      ## remove index column
# =============================================================================

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
    labwares = {}
      ## empty dict to add labware and labware_names to, to loop through
      
    ##### Loading pipettetips
    if p200:
        tips_200_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  
            11,                                  
            '200tips')
        labwares[tips_200_1] = 'filtertips_200'
        tips_200_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  
            10,                                  
            '200tips')
        labwares[tips_200_2] = 'filtertips_200'
    
    if p20:
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            8,                                  
            '20tips')
        labwares[tips_20_1] = 'filtertips_20'
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            7,                                  
            '20tips')
        labwares[tips_20_2] = 'filtertips_20'
        
    
    ##### Loading labware
    ## Tube for pooling the samples in
    if pool_tube_type == 'tube_1.5mL':
        pool_tube = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            5,
            'pool_tube')
        labwares[pool_tube] = '1.5mL_tubes'
    elif pool_tube_type == 'tube_5mL':
        if simulate:
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                      "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                    labware_def_5mL = json.load(labware_file)
            pool_tube = protocol.load_labware_from_definition( 
                labware_def_5mL, 
                5, 
                'pool_tube')
        else:
            pool_tube = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                5,
                'pool_tube')
            labwares[pool_tube] = '5mL_screw_cap'
    ## NO OFFSETS YET!
    # elif pool_tube_type == 'tube_15mL':
    #     pool_tube = protocol.load_labware(
    #         'opentrons_15_tuberack_falcon_15ml_conical',
    #         5,
    #         'pool_tube')
    # elif pool_tube_type == 'tube_50mL':
    #     pool_tube = protocol.load_labware(
    #         'opentrons_6_tuberack_falcon_50ml_conical',
    #         5,
    #         'pool_tube')

    ## Tubes to get samples from
    if sample_tube_type == 'plate_96':
        samples1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            6,
            'samples1')
        labwares[samples1] = 'plate_96'
        if sample_racks > 1:
            samples2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                3,
                'samples2')
            labwares[samples2] = 'plate_96'
            if sample_racks > 2:
                samples3 = protocol.load_labware(
                    'biorad_96_wellplate_200ul_pcr',
                    2,
                    'samples3')
                labwares[samples3] = 'plate_96'
                if sample_racks > 3:
                    samples4 = protocol.load_labware(
                        'biorad_96_wellplate_200ul_pcr',
                        1,
                        'samples4')
                    labwares[samples4] = 'plate_96'
                    if sample_racks > 4:
                        samples5 = protocol.load_labware(
                            'biorad_96_wellplate_200ul_pcr',
                            4,
                            'samples5')
                        labwares[samples5] = 'plate_96'
    
    elif sample_tube_type == 'PCR_strip':
        if simulate:
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            samples1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                6,                         
                'samples1')
            if sample_racks > 1:
                samples2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips,     
                    3,                         
                    'samples2')
                if sample_racks > 2:
                    samples3 = protocol.load_labware_from_definition( 
                        labware_def_pcrstrips,     
                        2,                         
                        'samples3')
                    if sample_racks > 3:
                        samples4 = protocol.load_labware_from_definition( 
                            labware_def_pcrstrips,     
                            1,                         
                            'samples4')
                        if sample_racks > 4:
                            samples5 = protocol.load_labware_from_definition( 
                                labware_def_pcrstrips,     
                                4,                         
                                'samples5')
        else:
            samples1 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                6,                                     
                'samples1')
            labwares[samples1] = 'pcr_strips'
            if sample_racks > 1:
                samples2 = protocol.load_labware( 
                    'pcrstrips_96_wellplate_200ul',        
                    3,                                     
                    'samples2')
                labwares[samples2] = 'pcr_strips'
                if sample_racks > 2:
                    samples3 = protocol.load_labware( 
                        'pcrstrips_96_wellplate_200ul',        
                        2,                                     
                        'samples3')
                    labwares[samples3] = 'pcr_strips'
                    if sample_racks > 3:
                        samples4 = protocol.load_labware( 
                            'pcrstrips_96_wellplate_200ul',        
                            1,                                     
                            'samples4')
                        labwares[samples4] = 'pcr_strips'
                        if sample_racks > 4:
                            samples5 = protocol.load_labware( 
                                'pcrstrips_96_wellplate_200ul',        
                                4,                                     
                                'samples5')
                            labwares[samples5] = 'pcr_strips'
        
    elif sample_tube_type == 'tube_1.5mL':
        samples1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            6,
            'samples1')
        labwares[samples1] = '1.5mL_tubes'
        if sample_racks > 1:
            samples2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                3,
                'samples2')
            labwares[samples2] = '1.5mL_tubes'
            if sample_racks > 2:
                samples3 = protocol.load_labware(
                    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                    2,
                    'samples3')
                labwares[samples3] = '1.5mL_tubes'
                if sample_racks > 3:
                    samples4 = protocol.load_labware(
                        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                        1,
                        'samples4')
                    labwares[samples4] = '1.5mL_tubes'
                    if sample_racks > 4:
                        samples5 = protocol.load_labware(
                            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                            4,
                            'samples5')
                        labwares[samples5] = '1.5mL_tubes'
    
    
            

