"""
Version: July22

sample_dilution.py is a protocol written for diluting/transferring samples.
Dilutes a certain number of samples to a fixed dilution ratio, or varying 
dilution rates for every sample.

You have to provide:
    number_of_samples you want to dilute/transfer.
        max number of samples depends on type of tubes the samples are in
        and/or type of tubes you want the dilutions in
    
    sample_volume
        If you want every sample diluted in the same ratio or transfer a fixed 
            amount of sample, without diluting, provide a single integer or 
            float for how many µL of sample and water you want the robot to use.
        If you want to dilute every sample differently, provide a list of 
            sample_volumes or water_volumes and set the other one to a fixed
            volume.
            final_volume
        If you provide a list of sample_volumes, you can either provide a list
        of water_volumes or a final_volume. If you do not have a water_volume 
        list, Water will be added to reach the final_volume.
   
    sample_tubes and dilution_tubes
        Samples are provied in: plate_96', 'PCR_strips' or 'tubes_1.5mL'
        You want the dilutions/transfered samples in: plate_96', 'PCR_strips'
        or 'tubes_1.5mL'
    
Robot does:
    1. If necesarry, water will be aliquoted.
        water_volume is based on a fixed volume, a list or a final_volume
        Water is taken from 5mL tube(s).
        Aliquoted in dilution labware of choice
    2. Sample is added:
        The chosen sample_volume is taken from the sample source labware of 
        choice. Transferred to dilution labware of choice
        If there was water already, sample will be mixed by pipetting 
        up and down.

Updates:
MB 220803: Changed some deck positions.
MB 221103: Made it possible to choose varying water volumes
MB 221118: Added mixing after adding sample + changed strip positions 
           + changed some deck positions
SV 221201: Added all types of plates (plate_96, cool_rack_plate_96, 
                                      NIOZ_plate_96, non_skirted_plate_96)
           and tested those in the simulator
MB 221219: Made it possible to add a list of both DNA and water
           Changed 20 uL tips to tipome tips
           Only 96 samples max, to make loading pipette tips doable
MB 230208: Changed pipetting with p20 and p300 simultaneuosly to pipetting
           first all p20 and then all p300 water_volumes. Otherwise while 
           switching pipettes the tubes side gets hit :|
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# If applicable: What is the starting position of the first 20µL tip?
starting_tip_p20 = 'A9'
# If applicable: What is the starting position of the first 200µL tip?
starting_tip_p200 = 'C5'
  ## If volume-wise p20 or p200 is not applicable, this variable won't be used

# How many samples do you want to dilute? 
number_of_samples = 96
  ## max 96

# How much sample volume (µL) do you want to use for the dilution?
sample_volume = [10.0, 10.0, 11.34, 11.13, 10.0, 34.21, 10.0, 11.53, 12.38, 17.58, 12.1, 12.8, 10.0, 10.0, 10.0, 10.0, 12.65, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 11.19, 10.0, 10.0, 11.73, 10.0, 25.82, 10.0, 10.0, 11.05, 10.0, 13.83, 32.73, 15.29, 24.49, 10.0, 10.0, 10.0, 10.0, 14.59, 10.0, 10.0, 15.08, 10.0, 11.08, 10.0, 10.0, 10.0, 11.96, 21.11, 16.58, 10.0, 10.0, 10.0, 10.0, 10.0, 11.44, 27.24, 14.02, 16.02, 10.0, 13.92, 11.03, 10.0, 10.0, 21.83, 60.0, 17.19, 12.2, 10.0, 11.05, 11.31, 10.0, 20.82, 10.0, 32.94, 60.0, 60.0, 25.06, 33.04, 60.0, 60.0, 51.49, 47.88, 27.3, 17.25, 12.17, 59.5, 28.25, 13.41, 60.0]
#sample_volume = [7.9, 24.7, 0.0, 3.9, 0.0, 3.1, 0.0, 0.0, 4.6, 9.5, 0.0, 0.0, 0.0, 11.5, 0.0, 3.1, 8.7, 12.4, 13.6, 1.3, 18.5, 9.7, 0.0, 1.4, 0.0, 13.0, 0.0, 13.7, 25.4, 20.0, 0.0, 13.3, 2.1, 2.2, 3.5, 15.2, 27.0, 0.0, 17.8, 22.0, 0.0, 7.4, 0.0, 7.9, 8.2, 16.9, 19.6, 23.8, 10.7, 6.5, 22.4, 0.6, 8.1, 11.6, 15.3, 8.5, 9.9, 7.3, 0.0, 0.0, 0.0, 0.0, 4.4, 13.2, 9.6, 19.2, 3.7, 28.2, 20.8, 18.0, 14.6, 17.5, 0.0, 19.5, 13.4, 29.1, 21.2, 0.0, 9.6, 23.9, 2.4, 28.3, 23.8, 26.7, 12.1, 26.5, 16.8, 0.0, 10.5, 25.8, 34.8, 6.9, 32.8, 0.0]
  ## Can be one volume or a list of volumes
water_volume = [25.1, 15.7, 0.0, 0.0, 5.2, 0.0, 29.1, 0.0, 0.0, 0.0, 0.0, 0.0, 28.4, 5.2, 19.8, 19.8, 0.0, 5.9, 15.3, 17.9, 11.9, 23.0, 28.8, 18.6, 28.0, 1.0, 0.0, 8.5, 10.0, 0.0, 15.6, 0.0, 38.6, 14.9, 0.0, 15.5, 0.0, 0.0, 0.0, 0.0, 9.5, 2.1, 13.9, 12.0, 0.0, 17.4, 1.7, 0.0, 9.5, 0.0, 22.2, 25.3, 16.1, 0.0, 0.0, 0.0, 7.1, 30.2, 35.4, 11.7, 4.8, 0.0, 0.0, 0.0, 0.0, 16.6, 0.0, 0.0, 3.9, 13.6, 0.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0, 6.3, 0.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# water_volume = [7.9, 24.7, 0.0, 3.9, 0.0, 3.1, 0.0, 0.0, 4.6, 9.5, 0.0, 0.0, 0.0, 
#                 11.5, 0.0, 3.1, 8.7, 12.4, 13.6, 1.3, 18.5, 9.7, 0.0, 1.4, 0.0,
#                 13.0, 0.0, 13.7, 25.4, 20.0, 0.0, 13.3, 2.1, 2.2, 3.5, 15.2,
#                 27.0, 0.0, 17.8, 22.0, 0.0, 7.4, 0.0, 7.9, 8.2, 16.9, 19.6,
#                 23.8, 10.7, 6.5, 22.4, 0.6, 8.1, 11.6, 15.3, 8.5, 9.9, 7.3,
#                 0.0, 0.0, 0.0, 0.0, 4.4, 13.2, 9.6, 19.2, 3.7, 28.2, 20.8,
#                 18.0, 14.6, 17.5, 0.0, 19.5, 13.4, 29.1, 21.2, 0.0, 9.6, 23.9,
#                 2.4, 28.3, 23.8, 26.7, 12.1, 26.5, 16.8, 0.0, 10.5, 25.8, 34.8,
#                 6.9, 32.8, 0.0]
  ## Can be one volume or a list of volumes.
# Do you want a fixed final volume? If True, set the desired final_volume
fixed_final_volume = False
final_volume = 10
## If fixed_final_volume == True, water_volume is not used
## Used to calculate how much water to add. 
## final_volume - sample_volume = water_volume


# In what kind of tubes are the samples provided?
sample_tubes = 'non_skirted_plate_96'
  ## Options: 
      #sample_tubes = 'plate_96' (BioRad skirted plate)
      #sample_tubes = 'cool_rack_plate_96' (BioRad skirted plate in Eppendorf cooler)
      #sample_tubes = 'NIOZ_plate_96' (BioRad skirted plate in NIOZ plate holder)
      #sample_tubes = 'non_skirted_plate_96' (Thermo non-skirted plate in BioRad skirted plate)
      #sample_tubes = 'PCR_strips' (strips in BioRad skirted plate)
      #sample_tubes = 'tubes_1.5mL'
if sample_tubes == 'PCR_strips':
    # In which columns are the strips in the plate (ignore if not using strips)?
    sample_strip_columns = ['2', '5', '8', '11'] 
# In what kind of tubes should the dilutions be made?  
dilution_tubes = 'plate_96'
  ## Options: 
      #sample_tubes = 'plate_96' (BioRad skirted plate)
      #sample_tubes = 'cool_rack_plate_96' (BioRad skirted plate in Eppendorf cooler)
      #sample_tubes = 'NIOZ_plate_96' (BioRad skirted plate in NIOZ plate holder)
      #sample_tubes = 'non_skirted_plate_96' (Thermo non-skirted plate in BioRad skirted plate)
      #sample_tubes = 'PCR_strips' (strips in BioRad skirted plate)
      #sample_tubes = 'tubes_1.5mL'
if dilution_tubes == 'PCR_strips':
    # In which columns are the strips in the plate (ignore if not using strips)?
    dilution_strip_columns = ['2', '5', '8', '11'] 
# Are you simulating the protocol, or running it on the OT2?
simulate = True
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
                                      
##### Import volume_tracking module 
if simulate:
    import json
    from mollab_modules import volume_tracking_v1 as vt
else: 
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
                                          
# Import other modules
import math
  ## math to do some calculations (rounding up)  
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
if not isinstance(sample_volume, list):
    # if sample_volume is only one volume and not a list of
    # volumes we need to create a list of volumes
    sample_volumes = []
    for i in range(number_of_samples):
        sample_volumes.append(sample_volume)
else:
    sample_volumes = sample_volume        

if not isinstance(water_volume, list):
    water_volumes = []
    for i in range(number_of_samples):
        water_volumes.append(water_volume)
# If sample_volume is only one volume and there is no list of water_volumes
# we need to create a list of water_volumes
else:
    water_volumes = water_volume
# If there is a list of water_volumes use that list

if fixed_final_volume:    
    water_volumes = []
    for i, sample_vol in enumerate(sample_volumes):
        water = final_volume - sample_vol
        water_volumes.append(water)
    # If sample_volume is a list, and there is no list of water_volumes, the 
    # final_volume will be used to calculate the water_volumes
else:
    water_volumes = water_volume
    # If sample_volumes is a list and water_volumes is a list, use both

stock_vol = 4800
  ## If diluting samples stock_vol == 4800 (full water tube)
  ## Actual tubes need to be filled to 5mL
  ## If more than 1 water tube all tubes need to be filled with same volume
  ## If using protocol for PCR, stock volume can be adjusted
total_water_volume = sum(water_volumes)
water_tubes = math.ceil((total_water_volume)/stock_vol)
  ## How many tubes of 5mL water are needed 

if sample_tubes == 'tubes_1.5mL':
    sample_racks = math.ceil(number_of_samples / 24)
elif sample_tubes == 'PCR_strips':
    samples_per_rack = len(sample_strip_columns) * 8
    sample_racks = math.ceil(number_of_samples / samples_per_rack)
elif (sample_tubes == 'plate_96' or 
      sample_tubes == 'cool_rack_plate_96' or 
      sample_tubes == 'NIOZ_plate_96' or 
      sample_tubes == 'non_skirted_plate_96'):
    sample_racks = math.ceil(number_of_samples / 96)
  ## How many sample_racks are needed (1,2,3 or 4)
if dilution_tubes == 'tubes_1.5mL':
    dilution_racks = math.ceil(number_of_samples / 24)
elif dilution_tubes == 'PCR_strips':
    dilutions_per_rack = len(dilution_strip_columns) * 8
    dilution_racks = math.ceil(number_of_samples / dilutions_per_rack)
elif (dilution_tubes == 'plate_96' or 
      dilution_tubes == 'cool_rack_plate_96' or 
      dilution_tubes == 'NIOZ_plate_96' or 
      dilution_tubes == 'non_skirted_plate_96'):
    dilution_racks = math.ceil(number_of_samples / 96)
  ## How many dilution_racks are needed (1 or 2)

tips_20_needed = (len([x for x in water_volumes if 0 < x < 20]) +
                  len([x for x in sample_volumes if 0 < x <= 17]))
tips_200_needed = (len([x for x in water_volumes if x >= 20]) +
                   len([x for x in sample_volumes if x > 17]))
## How many p20 / p200 tips do you need?


# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'sample_dilution.py',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Sample dilution or tranfer protocol.'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Dilute samples in a fixed or varying rates 
    or transfer samples to different tubes.
    """
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading pipettes and tips    
    tips_20 = []
    tips_200 = []
    if simulate:
        with open("labware/tipone_96_tiprack_20ul/"
                  "tipone_96_tiprack_20ul.json") as labware_file:
                labware_def_tipone_96_tiprack_20ul = json.load(labware_file)
            
        tips_20_1 = protocol.load_labware_from_definition(
            labware_def_tipone_96_tiprack_20ul,
            11,                                  
            'tipone_20tips_1')
        tips_20.append(tips_20_1)
        tips_20_2 = protocol.load_labware_from_definition(
            labware_def_tipone_96_tiprack_20ul,
            10,                                  
            'tipone_20tips_2')
        tips_20.append(tips_20_2)
        tips_200_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      
            8,                                     
            'tips_200_1')
        tips_200.append(tips_200_1) 
        tips_200_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      
            7,                                     
            'tips_200_2')
        tips_200.append(tips_200_2)
    else:    
        tips_20_1 = protocol.load_labware(
            'tipone_96_tiprack_20uL',  
            11,                                  
            'tipone_20tips_1')  
        tips_20.append(tips_20_1)
        tips_20_2 = protocol.load_labware(
            'tipone_96_tiprack_20uL',  
            10,                                  
            'tipone_20tips_2')
        tips_20.append(tips_20_2)
        tips_200_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      
            8,                                     
            'tips_200_1')
        tips_200.append(tips_200_1)
        tips_200_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      
            7,                                     
            'tips_200_2')
        tips_200.append(tips_200_2)
    
    
    
    ##### Loading pipettes
    p20 = protocol.load_instrument(
        'p20_single_gen2',
        'left',
        tip_racks = tips_20)
    p300 = protocol.load_instrument(
        'p300_single_gen2',
        'right',
        tip_racks = tips_200)

    ##### Loading labware 
    if sample_tubes == 'plate_96':
        if sample_racks >= 1:            
            sample_source_1 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                1,
                'sample_source_1_plate_96')
        if sample_racks >= 2:          
            sample_source_2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                4,
                'sample_source_2_plate_96')
        if sample_racks >= 3:
            sample_source_3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                3,
                'sample_source_3_plate_96')
    if sample_tubes == 'cool_rack_plate_96':
        if simulate:
            with open("labware/biorad_qpcr_plate_eppendorf_cool_rack/"
                      "biorad_qpcr_plate_eppendorf_cool_rack.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            if sample_racks >= 1:
                sample_source_1 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    1,                         
                    'sample_source_1_cool_rack_plate_96')   
            if sample_racks >= 2:
                sample_source_2 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    4,                         
                    'sample_source_2_cool_rack_plate_96')   
            if sample_racks >= 3:
                sample_source_3 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    3,                         
                    'sample_source_3_cool_rack_plate_96')   
        else:
            if sample_racks >= 1:            
                sample_source_1 = protocol.load_labware(
                    'biorad_qpcr_plate_eppendorf_cool_rack',
                    1,
                    'sample_source_1_cool_rack_plate_96')
            if sample_racks >= 2:          
                sample_source_2 = protocol.load_labware(
                    'biorad_qpcr_plate_eppendorf_cool_rack',
                    4,
                    'sample_source_2_cool_rack_plate_96')
            if sample_racks >= 3:
                sample_source_3 = protocol.load_labware(
                    'biorad_qpcr_plate_eppendorf_cool_rack',
                    3,
                    'sample_source_3_cool_rack_plate_96')
    if sample_tubes == 'NIOZ_plate_96':
        if simulate:
            with open("labware/biorad_qpcr_plate_nioz_plateholder/"
                      "biorad_qpcr_plate_nioz_plateholder.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            if sample_racks >= 1:
                sample_source_1 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    1,                         
                    'sample_source_1_NIOZ_plate_96')   
            if sample_racks >= 2:
                sample_source_2 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    4,                         
                    'sample_source_2_NIOZ_plate_96')   
            if sample_racks >= 3:
                sample_source_3 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    3,                         
                    'sample_source_3_NIOZ_plate_96')   
        else:
            if sample_racks >= 1:            
                sample_source_1 = protocol.load_labware(
                    'biorad_qpcr_plate_nioz_plateholder',
                    1,
                    'sample_source_1_NIOZ_plate_96')
            if sample_racks >= 2:          
                sample_source_2 = protocol.load_labware(
                    'biorad_qpcr_plate_nioz_plateholder',
                    4,
                    'sample_source_2_NIOZ_plate_96')
            if sample_racks >= 3:
                sample_source_3 = protocol.load_labware(
                    'biorad_qpcr_plate_nioz_plateholder',
                    3,
                    'sample_source_3_NIOZ_plate_96')
    if sample_tubes == 'non_skirted_plate_96':
        if simulate:
            with open("labware/thermononskirtedinbioradskirted_96_wellplate_200ul/"
                      "thermononskirtedinbioradskirted_96_wellplate_200ul.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            if sample_racks >= 1:
                sample_source_1 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    1,                         
                    'sample_source_1_non_skirted_plate_96')   
            if sample_racks >= 2:
                sample_source_2 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    4,                         
                    'sample_source_2_non_skirted_plate_96')   
            if sample_racks >= 3:
                sample_source_3 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    3,                         
                    'sample_source_3_non_skirted_plate_96')   
        else:
            if sample_racks >= 1:            
                sample_source_1 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',
                    1,
                    'sample_source_1_non_skirted_plate_96')
            if sample_racks >= 2:          
                sample_source_2 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',
                    4,
                    'sample_source_2_non_skirted_plate_96')
            if sample_racks >= 3:
                sample_source_3 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',
                    3,
                    'sample_source_3_non_skirted_plate_96')               
    if sample_tubes == 'tubes_1.5mL':
        if sample_racks >= 1:
            sample_source_1 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                1,
                'sample_source_1_tubes_1.5mL')
        if sample_racks >= 2:    
            sample_source_2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                4,
                'sample_source_2_tubes_1.5mL')
        if sample_racks >= 3:    
            sample_source_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                3,
                'sample_source_3_tubes_1.5mL')
        if sample_racks >= 4:
            sample_source_4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                6,
                'sample_source_4_tubes_1.5mL')
    if sample_tubes == 'PCR_strips':
        if simulate:
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            if sample_racks >= 1:
                sample_source_1 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    1,                     
                    'sample_source_1_PCR_strips')     
            if sample_racks >= 2:
                sample_source_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    4,                     
                    'sample_source_2_PCR_strips')     
            if sample_racks >= 3:
                sample_source_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    3,                     
                    'sample_source_3_PCR_strips')     
            if sample_racks >= 4:
                sample_source_4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    6,                     
                    'sample_source_4_PCR_strips') 
        else:
            if sample_tubes == 'PCR_strips':
                if sample_racks >= 1:
                    sample_source_1 = protocol.load_labware(
                        'pcrstrips_96_wellplate_200ul',         
                        1,                                      
                        'sample_source_1_PCR_strips')                      
                if sample_racks >= 2:
                    sample_source_2 = protocol.load_labware(
                        'pcrstrips_96_wellplate_200ul',         
                        4,                                      
                        'sample_source_2_PCR_strips')                      
                if sample_racks >= 3:   
                    sample_source_3 = protocol.load_labware(
                        'pcrstrips_96_wellplate_200ul',         
                        3,                                      
                        'sample_source_3_PCR_strips')                      
                if sample_racks >= 4: 
                    sample_source_4 = protocol.load_labware(
                        'pcrstrips_96_wellplate_200ul',         
                        6,                                      
                        'sample_source_4')     
         
    if dilution_tubes == 'plate_96':
        if dilution_racks >= 1:        
            dilution_dest_1 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                2,
                'dilution_dest_1_plate_96')
        if dilution_racks >= 2:            
            dilution_dest_2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                5,
                'dilution_dest_2_plate_96')
        if dilution_racks >= 3:             
            dilution_dest_3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                9,
                'dilution_dest_3_plate_96')
    if dilution_tubes == 'cool_rack_plate_96':
        if simulate:
            with open("labware/biorad_qpcr_plate_eppendorf_cool_rack/"
                      "biorad_qpcr_plate_eppendorf_cool_rack.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            if dilution_racks >= 1:
                dilution_dest_1 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    2,                         
                    'dilution_dest_1_cool_rack_plate_96')   
            if dilution_racks >= 2:
                dilution_dest_2 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    5,                         
                    'dilution_dest_2_cool_rack_plate_96')   
            if dilution_racks >= 3:
                dilution_dest_3 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    9,                         
                    'dilution_dest_3_cool_rack_plate_96')   
        else:
            if dilution_racks >= 1:            
                dilution_dest_1 = protocol.load_labware(
                    'biorad_qpcr_plate_eppendorf_cool_rack',
                    2,
                    'dilution_dest_1_cool_rack_plate_96')
            if dilution_racks >= 2:          
                dilution_dest_2 = protocol.load_labware(
                    'biorad_qpcr_plate_eppendorf_cool_rack',
                    5,
                    'dilution_dest_2_cool_rack_plate_96')
            if dilution_racks >= 3:
                dilution_dest_3 = protocol.load_labware(
                    'biorad_qpcr_plate_eppendorf_cool_rack',
                    9,
                    'dilution_dest_3_cool_rack_plate_96')
    if dilution_tubes == 'NIOZ_plate_96':
        if simulate:
            with open("labware/biorad_qpcr_plate_nioz_plateholder/"
                      "biorad_qpcr_plate_nioz_plateholder.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            if dilution_racks >= 1:
                dilution_dest_1 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    2,                         
                    'dilution_dest_1_NIOZ_plate_96')   
            if dilution_racks >= 2:
                dilution_dest_2 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    5,                         
                    'dilution_dest_2_NIOZ_plate_96')   
            if dilution_racks >= 3:
                dilution_dest_3 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    9,                         
                    'dilution_dest_3_NIOZ_plate_96')   
        else:
            if dilution_racks >= 1:            
                dilution_dest_1 = protocol.load_labware(
                    'biorad_qpcr_plate_nioz_plateholder',
                    2,
                    'dilution_dest_1_NIOZ_plate_96')
            if dilution_racks >= 2:          
                dilution_dest_2 = protocol.load_labware(
                    'biorad_qpcr_plate_nioz_plateholder',
                    5,
                    'dilution_dest_2_NIOZ_plate_96')
            if dilution_racks >= 3:
                dilution_dest_3 = protocol.load_labware(
                    'biorad_qpcr_plate_nioz_plateholder',
                    9,
                    'dilution_dest_3_NIOZ_plate_96')
    if dilution_tubes == 'non_skirted_plate_96':
        if simulate:
            with open("labware/thermononskirtedinbioradskirted_96_wellplate_200ul/"
                      "thermononskirtedinbioradskirted_96_wellplate_200ul.json") as labware_file:
                    labware_def_plate_holder = json.load(labware_file)
            if dilution_racks >= 1:
                dilution_dest_1 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    2,                         
                    'dilution_dest_1_non_skirted_plate_96')   
            if dilution_racks >= 2:
                dilution_dest_2 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    5,                         
                    'dilution_dest_2_non_skirted_plate_96')   
            if dilution_racks >= 3:
                dilution_dest_3 = protocol.load_labware_from_definition( 
                    labware_def_plate_holder,     
                    9,                         
                    'dilution_dest_3_non_skirted_plate_96')   
        else:
            if dilution_racks >= 1:            
                dilution_dest_1 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',
                    2,
                    'dilution_dest_1_non_skirted_plate_96')
            if dilution_racks >= 2:          
                dilution_dest_2 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',
                    5,
                    'dilution_dest_2_non_skirted_plate_96')
            if dilution_racks >= 3:
                dilution_dest_3 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',
                    9,
                    'dilution_dest_3_non_skirted_plate_96')  
    if dilution_tubes == 'tubes_1.5mL':
        if dilution_racks >= 1:
            dilution_dest_1 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                2,                                      
                'dilution_dest_1_tubes_1.5mL')                      
        if dilution_racks >= 2:    
            dilution_dest_2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                5,                                      
                'dilution_dest_2_tubes_1.5mL')                      
        if dilution_racks >= 3:    
            dilution_dest_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                9,                                      
                'dilution_dest_3_tubes_1.5mL')                      
        if dilution_racks >= 4:
            dilution_dest_4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                8,                                      
                'dilution_dest_4_tubes_1.5mL')                      
    if dilution_tubes == 'PCR_strips':
        if simulate:
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            if dilution_racks >= 1:
                dilution_dest_1 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    2,                     
                    'dilution_dest_1_PCR_strips')     
            if dilution_racks >= 2:
                dilution_dest_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    5,                     
                    'dilution_dest_2_PCR_strips')     
            if dilution_racks >= 3:
                dilution_dest_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    9,                     
                    'dilution_dest_3_PCR_strips')     
            if dilution_racks >= 4:
                dilution_dest_4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    8,                     
                    'dilution_dest_4_PCR_strips')   
        else: 
            if dilution_racks >= 1:
                dilution_dest_1 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    2,                                      
                    'dilution_dest_1_PCR_strips')                      
            if dilution_racks >= 2:
                dilution_dest_2 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    5,                                      
                    'dilution_dest_2_PCR_strips')                      
            if dilution_racks >= 3:    
                dilution_dest_3 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    9,                                      
                    'dilution_dest_3_PCR_strips')                      
            if dilution_racks >= 4:        
                dilution_dest_4 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    8,                                      
                    'dilution_dest_4_PCR_strips')   
   
    if water_tubes > 0: 
        if simulate:
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                      "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                    labware_def_5mL = json.load(labware_file)
            tubes_5mL = protocol.load_labware_from_definition( 
                labware_def_5mL, 
                9, 
                'tubes_5mL')    
        else:
            if water_tubes > 0:
                tubes_5mL = protocol.load_labware(
                    'eppendorfscrewcap_15_tuberack_5000ul',     
                    9,                                          
                    'tubes_5mL')                                    
# =============================================================================

# SETTING LOCATIONS#!!!========================================================
# =============================================================================
    ##### Setting starting tip
    if tips_20_needed > 0:
        p20.starting_tip = tips_20_1.well(starting_tip_p20)
    if tips_200_needed > 0:
        p300.starting_tip = tips_200_1.well(starting_tip_p200)
      ## The starting_tip is the location of first pipette tip in the box   ##
      
    ##### Setting tube locations
   
    sample_wells = []
    if sample_tubes == 'PCR_strips':
        sample_columns = []
        if sample_racks >= 1:
            sample_columns_1 = (                                                           
                ([sample_source_1.columns_by_name()[column_name] 
                  for column_name in sample_strip_columns])) 
            for column in sample_columns_1:
                sample_columns.append(column)
        if sample_racks >= 2:
            sample_columns_2 = ( 
                ([sample_source_2.columns_by_name()[column_name] 
                  for column_name in sample_strip_columns]))
            for column in sample_columns_2:
                sample_columns.append(column)
        if sample_racks >= 3:
            sample_columns_3 = ( 
                ([sample_source_3.columns_by_name()[column_name] 
                  for column_name in sample_strip_columns]))
            for column in sample_columns_3:
                sample_columns.append(column)
        if sample_racks >= 4:
            sample_columns_4 = ( 
                ([sample_source_4.columns_by_name()[column_name] 
                  for column_name in sample_strip_columns]))
            for column in sample_columns_4:
                sample_columns.append(column)
        for column in sample_columns:
            for well in column:
                sample_wells.append(well)
         ##makes a list of all wells in 1,2,3 or 4 full plates of PCR strips##
    else:
        if sample_racks == 1: 
            for well in sample_source_1.wells():
                sample_wells.append(well)
        if sample_racks == 2:
            for well in sample_source_1.wells():
                sample_wells.append(well)
            for well in sample_source_2.wells():
                sample_wells.append(well)
        if sample_racks == 3:
            for well in sample_source_1.wells():
                sample_wells.append(well)
            for well in sample_source_2.wells():
                sample_wells.append(well)
            for well in sample_source_3.wells():
                sample_wells.append(well)
        if sample_racks == 4:
            for well in sample_source_1.wells():
                sample_wells.append(well)
            for well in sample_source_2.wells():
                sample_wells.append(well)
            for well in sample_source_3.wells():
                sample_wells.append(well)
            for well in sample_source_4.wells():
                sample_wells.append(well)
              
    dilution_wells = []
    if dilution_tubes == 'PCR_strips':
        dilution_columns = []
        if dilution_racks >= 1:
            dilution_columns_1 = (
                ([dilution_dest_1.columns_by_name()[column_name] 
                  for column_name in dilution_strip_columns])) 
            for column in dilution_columns_1:
                dilution_columns.append(column)
        if dilution_racks >= 2:
            dilution_columns_2 = (
                ([dilution_dest_2.columns_by_name()[column_name] 
                  for column_name in dilution_strip_columns]))
            for column in dilution_columns_2:
                dilution_columns.append(column)
        if dilution_racks >= 3:
            dilution_columns_3 = ( 
                ([dilution_dest_3.columns_by_name()[column_name] 
                  for column_name in dilution_strip_columns]))
            for column in dilution_columns_3:
                dilution_columns.append(column)
        if dilution_racks >= 4:
            dilution_columns_4 = ( 
                ([dilution_dest_4.columns_by_name()[column_name] 
                  for column_name in dilution_strip_columns]))
            for column in dilution_columns_4:
                dilution_columns.append(column)
        for column in dilution_columns:
            for well in column:
                dilution_wells.append(well)
         ##makes a list of all wells in 1,2,3 or 4 full plates of PCR strips## 
    else:
        if dilution_racks == 1: 
            for well in dilution_dest_1.wells():
                dilution_wells.append(well)
        if dilution_racks == 2:
            for well in dilution_dest_1.wells():
                dilution_wells.append(well)
            for well in dilution_dest_2.wells():
                dilution_wells.append(well)
        if dilution_racks == 3:
            for well in dilution_dest_1.wells():
                dilution_wells.append(well)
            for well in dilution_dest_2.wells():
                dilution_wells.append(well)
            for well in dilution_dest_3.wells():
                dilution_wells.append(well)
        if dilution_racks == 4:
            for well in dilution_dest_1.wells():
                dilution_wells.append(well)
            for well in dilution_dest_2.wells():
                dilution_wells.append(well)
            for well in dilution_dest_3.wells():
                dilution_wells.append(well)
            for well in dilution_dest_4.wells():
                dilution_wells.append(well)
            
    sample_wells = sample_wells[:number_of_samples]
    dilution_wells = dilution_wells[:number_of_samples]
    ## cuts off the list after certain number of samples                    ##
# =============================================================================

# MESSAGE AT THE START=========================================================
# =============================================================================
    if len([x for x in water_volumes if x > 0]) > 0:
        protocol.pause("I need " + str(water_tubes) + " tube(s) with " 
                       + str(stock_vol) + " of water.")
# =============================================================================

# ALIQUOTING WATER=============================================================    
# =============================================================================
    ##### Variables for volume tracking and aliquoting
    if len([x for x in water_volumes if x > 0]) > 0:
        counter = 0 # to count how many tubes already emptied
        source = tubes_5mL.wells()[counter]
        destination = dilution_wells
        container = 'tube_5mL'
        start_height = vt.cal_start_height(container, stock_vol)
        current_height = start_height
        
        well_counter = 0 # to keep track of pipette_tip use
        
        ### All water with p20
        for i, (well, water_vol) in enumerate(zip(destination, water_volumes)):
          ## aliquot water in the correct wells, for each well do the following:  
            
              dispension_vol = water_vol
              aspiration_vol = dispension_vol + (dispension_vol/100*2)
              
              if 0 < aspiration_vol <= 20:
                      
                if well_counter == 0:
                    p20.pick_up_tip()
                    ## If we are at the first well, start by picking up a tip

                elif well_counter % 16 == 0:
                    p20.drop_tip()
                      ## Then, after every 16th well drop tip                   
                    p20.pick_up_tip()
                    ## Pick up new tip
                        
                current_height, pip_height, bottom_reached = vt.volume_tracking(
                    container, dispension_vol, current_height)
                      ## call volume_tracking function, obtain current_height,     
                      ## pip_height and whether bottom_reached.                    
                if bottom_reached:
                  ## continue with next tube, reset vt                            
                    current_height = start_height
                    current_height, pip_height, bottom_reached = (
                        vt.volume_tracking(
                            container, dispension_vol, current_height))
                    counter = counter + 1
                    source = tubes_5mL.wells()[counter]
                    aspiration_location = source.bottom(current_height)
                    protocol.comment(
                        "Continue with tube " + str(counter + 1) + " of water")
                else:
                    aspiration_location = source.bottom(pip_height)
                      ## Set the location of where to aspirate from.
    
                water_pipette = p20
                  ## What pipette to use
        
                #### The actual aliquoting of water
                water_pipette.aspirate(aspiration_vol, aspiration_location)
                  ## Aspirate the amount specified in aspiration_vol from the
                  ## location specified in aspiration_location.
                water_pipette.dispense(dispension_vol, well)
                  ## Dispense the amount specified in dispension_vol to the
                  ## location specified in well (looping through plate)
                water_pipette.dispense(10, aspiration_location)
                  ## Alternative for blow-out, make sure the tip doesn't fill
                  ## completely when using a disposal volume by dispensing some
                  ## of the volume after each pipetting step. (blow-out too many
                  ## bubbles)
                well_counter = well_counter + 1
         
        try:
            p20.drop_tip()
        except:
            pass
        
        ### All water with p300
        well_counter = 0
        for i, (well, water_vol) in enumerate(zip(destination, water_volumes)):
          ## aliquot water in the correct wells, for each well do the following:  
            
              dispension_vol = water_vol
              aspiration_vol = dispension_vol + (dispension_vol/100*2)
              
              if aspiration_vol > 20:
                      
                if well_counter == 0:
                    p300.pick_up_tip()
                    ## If we are at the first well, start by picking up a tip

                elif well_counter % 16 == 0:
                    p300.drop_tip()
                      ## Then, after every 16th well drop tip                   
                    p300.pick_up_tip()
                    ## Pick up new tip
                        
                current_height, pip_height, bottom_reached = vt.volume_tracking(
                    container, dispension_vol, current_height)
                      ## call volume_tracking function, obtain current_height,     
                      ## pip_height and whether bottom_reached.                    
                if bottom_reached:
                  ## continue with next tube, reset vt                            
                    current_height = start_height
                    current_height, pip_height, bottom_reached = (
                        vt.volume_tracking(
                            container, dispension_vol, current_height))
                    counter = counter + 1
                    source = tubes_5mL.wells()[counter]
                    aspiration_location = source.bottom(current_height)
                    protocol.comment(
                        "Continue with tube " + str(counter + 1) + " of water")
                else:
                    aspiration_location = source.bottom(pip_height)
                      ## Set the location of where to aspirate from.
    
                water_pipette = p300
                  ## What pipette to use
        
                #### The actual aliquoting of water
                water_pipette.aspirate(aspiration_vol, aspiration_location)
                  ## Aspirate the amount specified in aspiration_vol from the
                  ## location specified in aspiration_location.
                water_pipette.dispense(dispension_vol, well)
                  ## Dispense the amount specified in dispension_vol to the
                  ## location specified in well (looping through plate)
                water_pipette.dispense(10, aspiration_location)
                  ## Alternative for blow-out, make sure the tip doesn't fill
                  ## completely when using a disposal volume by dispensing some
                  ## of the volume after each pipetting step. (blow-out too many
                  ## bubbles)
                well_counter = well_counter + 1
        try: 
            p300.drop_tip()
        except:
            pass
               

# =============================================================================

# DILUTING SAMPLES=============================================================
# =============================================================================
    for sample_well, dilution_well, sample_vol, water_vol in zip(
            sample_wells, dilution_wells, sample_volumes, water_volumes):
        ## Combine each sample with a dilution_well and a destination well
        if sample_vol > 0:
            if sample_vol > 17:
                sample_pipette = p300
            else:
                sample_pipette = p20
            sample_pipette.pick_up_tip()
              ## picks up tip from location of specified starting_tip     
              ## or following 
            sample_pipette.aspirate(sample_vol, sample_well)
              ## aspirate sample_volume_dil = volume for dilution from sample
            if sample_pipette == p300:
                sample_pipette.air_gap(20)
                dispense_vol = sample_vol + 30
            else:
                sample_pipette.air_gap(2)
                dispense_vol = sample_vol + 3
              ## airgap
            sample_pipette.dispense(dispense_vol , dilution_well)
              ## dispense sample_volume_dil = volume for dilution into dil_well
            if water_vol > 0:
                sample_pipette.mix(3, dispense_vol, dilution_well)
                sample_pipette.dispense(dispense_vol + 5, dilution_well)
              ## instead of blow-out
            sample_pipette.drop_tip()
              ## Drop tip in trashbin on 12
         
# =============================================================================