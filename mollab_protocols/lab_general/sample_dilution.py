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


"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# If applicable: What is the starting position of the first 20µL tip?
starting_tip_p20 = 'A1'
# If applicable: What is the starting position of the first 200µL tip?
starting_tip_p200 = 'A1'
  ## If volume-wise p20 or p200 is not applicable, this variable won't be used

# How many samples do you want to dilute? 
number_of_samples = 96
  ## sample_tubes == 'plate_96', dilution_tubes == 'plate_96'        MAX = 288
  ###   = 3 sample plates & 3 dilutions plates
  ## sample_tubes == 'plate_96', dilution_tubes == 'PCR_strips'      MAX = 192
  ###   = 2 sample plates & 4 dilution PCR strip racks
  ## sample_tubes == 'plate_96', dilution_tubes == 'tubes_1.5mL'     MAX = 96
  ###   = 1 sample plate & 4 dilution 1.5 mL tube racks
  ## sample_tubes == 'PCR_strips', diltution_tubes == 'plate_96'     MAX = 192
  ###   = 4 sample PCR strip racks & 2 dilution plates
  ## sample_tubes == 'PCR_strips', dilution_tubes == 'PCR_strips'    MAX = 144
  ###   = 3 sample PCR strip racks & 3 dilution PCR strip racks
  ## sample_tubes == 'PCR_strips', diltution_tubes == 'tubes_1.5mL'  MAX = 96
  ###   = 2 sample PCR strip racks & 4 dilution 1.5 mL tube racks
  ## sample_tubes == '1.5mL tubes', dilution_tubes == 'plate_96'     MAX = 96
  ###   = 4 sample 1.5mL tube racks & 1 dilution plate
  ## sample_tubes == '1.5mL tubes', dilution_tubes == 'PCR_strips'   MAX = 96
  ###   = 4 sample 1.5mL tube racks & 2 dilution PCR strip racks
  ## sample_tubes == '1.5mL tubes', dilution_tubes == 'tubes_1.5mL'  MAX = 72
  ###   = 3 sample 1.5mL tube racks & 3 dilution 1.5mL tube racks

# How much sample volume (µL) do you want to use for the dilution?
sample_volume = 5
  ## Can be one volume or a list of volumes
if isinstance(sample_volume, list):
# If you enter a list of volumes, also set a final_volume
    final_volume = 10
      ## If you do not have a list of sample_volumes, final_volume is not used
      ## Used to calculate how much water to add. 
      ## final_volume - sample_volume = water_volume
water_volume = [24.00403457065793, 36.61144787047444, 10.72007076254264, 25.03414160342187, 33.56898694640979, 16.209102890841336, 31.930189677752047, 14.89604341932225, 25.90358707449652, 3.227555354628393, 22.17286845732918, 17.26307811447122, 23.7360796688047, 14.595865474702599, 15.41359307946097, 1.9317420633351876, 17.79343860671441, 16.4042464546623, 8.2173670182323, 18.868538292462958, 26.3116360575913, 16.08459436085419, 17.8957190272823, 8.17293138919743, 1.4447857228363334, 7.317936747116221, 13.58298394780315, 11.205387063873669, 17.56554596657994, 8.92503696427578, 11.52116083351013, 2.768397151652355, 0.19788467286450562, 2.9381289433570714, 27.283361949233793, 3.5244429471499803, 6.689772404312841, 1.0973252600218517, 4.573394892863696, 1.4578246063541576, 9.57436707564181, 18.802421177359648, -5.025614183544055, -4.747532780923736, -5.030597072563975, -5.020148038694306, -4.844189561011117, -4.989187158533131, -4.945281698731052, 7.566995155813309, 12.321642300321471, 15.84555151758677, 3.401584730093065, 38.564368511280676, -2.36074133804091, -1.488140340801599, 0.4808445898687772, 0.469900033817952, -1.8666653816858734, 26.35995001079781, 18.6857001592819, 31.344233037299787, 17.66613476777365, 21.59085199501737, 17.720596320558315, 13.241701948132938, 6.98661873266933, 7.8410563508007805, 20.122700905354833, 20.77143277088482, 14.484704084129419, 12.96982745794297, 4.410526036573234, 7.0093935922759805, 16.15129940575227, 17.9101595825133, 16.589343462650888, 21.54472474660837, 19.40337535471382, 19.18043373792777, 9.03098295099343, 6.10491941116117, 3.593347763780372, 36.18786495861053, 24.48599858136445, 14.86494465593896, 3.5094041460829715, 2.1735801732773687, 9.032029945259122, 2.130497309010236, 1.5442305672622991, 8.50823914027279, 0.5400000000000009, 5.016676191820547, 0.9746387045122864, 1.3142876019947742]
  ## Can be one volume or a list of volumes

# In what kind of tubes are the samples provided?
sample_tubes = 'PCR_strips'
  ## Options: 'plate_96', 'PCR_strips', 'tubes_1.5mL'
if sample_tubes == 'PCR_strips':
    # In which columns are the strips in the plate (ignore if not using strips)?
    sample_strip_columns = ['2', '5', '7', '11'] 
# In what kind of tubes should the dilutions be made?  
dilution_tubes = 'plate_96'
  ## Options: 'plate_96', 'PCR_strips', 'tubes_1.5mL'
if dilution_tubes == 'PCR_strips':
    # In which columns are the strips in the plate (ignore if not using strips)?
    dilution_strip_columns = ['2', '7', '11'] 
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

    if not isinstance(water_volume, list):
        water_volumes = []
        for i in range(number_of_samples):
            water_volumes.append(water_volume)
    # If sample_volume is only one volume and there is no list of water_volumes
    # we need to create a list of water_volumes
    else:
        water_volumes = water_volume
    # If sample_volume is only one volume and there is a list of water_volumes
    # Use that list

else:
    sample_volumes = sample_volume
    
    if not isinstance(water_volume, list):
        water_volumes = []
        for i, sample_vol in enumerate(sample_volume):
            water = final_volume - sample_vol
            water_volumes.append(water)
    # If sample_volume is a list, and there is no list of water_volumes, the 
    # final_volume will be used to calculate the water_volumes
    else:
        water_volumes = water_volume
    # If sample_volumes is a list and water_volumes is a list, use both

total_water_volume = sum(water_volumes)
water_tubes = math.ceil((total_water_volume)/4800)
  ## How many tubes of 5mL water are needed 

if sample_tubes == 'tubes_1.5mL':
    sample_racks = math.ceil(number_of_samples / 24)
elif sample_tubes == 'PCR_strips':
    samples_per_rack = len(sample_strip_columns) * 8
    sample_racks = math.ceil(number_of_samples / samples_per_rack)
elif sample_tubes == 'plate_96':
    sample_racks = math.ceil(number_of_samples / 96)
  ## How many sample_racks are needed (1,2,3 or 4)
if dilution_tubes == 'tubes_1.5mL':
    dilution_racks = math.ceil(number_of_samples / 24)
elif dilution_tubes == 'PCR_strips':
    dilutions_per_rack = len(dilution_strip_columns) * 8
    dilution_racks = math.ceil(number_of_samples / dilutions_per_rack)
elif dilution_tubes == 'plate_96':
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
    
    if tips_20_needed > 0:
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',      
            11,                                     
            'tips_20_1')
        tips_20.append(tips_20_1)
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',      
            10,                                     
            'tips_20_2')
        tips_20.append(tips_20_2)
        if tips_20_needed > 96:
            tips_20_3 = protocol.load_labware(
                'opentrons_96_filtertiprack_20ul',      
                7,                                      
                'tips_20_3')
            tips_20.append(tips_20_3)
            if tips_20_needed > 192:
                tips_20_4 = protocol.load_labware(
                'opentrons_96_filtertiprack_20ul',      
                8,                                      
                'tips_20_4')
                tips_20.append(tips_20_4)
            elif tips_200_needed > 0:
                tips_200_1 = protocol.load_labware(
                    'opentrons_96_filtertiprack_200ul',      
                    8,                                     
                    'tips_200_1')
                tips_200.append(tips_200_1)
        elif tips_200_needed > 0:
            tips_200_1 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',      
                7,                                     
                'tips_200_1')
            tips_200.append(tips_200_1)
            tips_200_2 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',      
                8,                                     
                'tips_200_2')
            tips_200.append(tips_200_2)
            
    
    else:
        tips_200_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      
            11,                                     
            'tips_200_1')
        tips_200.append(tips_200_1)
        tips_200_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      
            10,                                     
            'tips_200_2')
        tips_200.append(tips_200_2)
        if tips_200_needed > 96:
            tips_200_3 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',      
                7,                                      
                'tips_200_3')
            tips_200.append(tips_200_3)
            if tips_200_needed > 192:
                tips_200_4 = protocol.load_labware(
                    'opentrons_96_filtertiprack_200ul',      
                    8,                                      
                    'tips_200_4')
                tips_200.append(tips_200_4)
    
    
    
    ##### Loading pipettes
    if tips_20_needed > 0:
        p20 = protocol.load_instrument(
            'p20_single_gen2',
            'left',
            tip_racks = tips_20)
    if tips_200_needed > 0:
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
                'sample_source_1')
        if sample_racks >= 2:          
            sample_source_2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                4,
                'sample_source_2')
        if sample_racks >= 3:
            sample_source_3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                7,
                'sample_source_3')
    if sample_tubes == 'tubes_1.5mL':
        if sample_racks >= 1:
            sample_source_1 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                1,
                'sample_source_1')
        if sample_racks >= 2:    
            sample_source_2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                4,
                'sample_source_2')
        if sample_racks >= 3:    
            sample_source_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                3,
                'sample_source_3')
        if sample_racks >= 4:
            sample_source_4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                6,
                'sample_source_4')
         
    if dilution_tubes == 'plate_96':
        if dilution_racks >= 1:        
            dilution_dest_1 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                2,
                'dilution_dest_1')
        if dilution_racks >= 2:            
            dilution_dest_2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                5,
                'dilution_dest_2')
        if dilution_racks >= 3:             
            dilution_dest_3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                8,
                'dilution_dest_3')
    if dilution_tubes == 'tubes_1.5mL':
        if dilution_racks >= 1:
            dilution_dest_1 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                2,                                      
                'dilution_dest_1')                      
        if dilution_racks >= 2:    
            dilution_dest_2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                5,                                      
                'dilution_dest_2')                      
        if dilution_racks >= 3:    
            dilution_dest_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                8,                                      
                'dilution_dest_3')                      
        if dilution_racks >= 4:
            dilution_dest_4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                9,                                      
                'dilution_dest_4')                      

    if simulate:
        with open("labware/pcrstrips_96_wellplate_200ul/"
                  "pcrstrips_96_wellplate_200ul.json") as labware_file:
                labware_def_pcrstrips = json.load(labware_file)
        if sample_tubes == 'PCR_strips':
            if sample_racks >= 1:
                sample_source_1 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    1,                     
                    'sample_source_1')     
            if sample_racks >= 2:
                sample_source_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    4,                     
                    'sample_source_2')     
            if sample_racks >= 3:
                sample_source_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    3,                     
                    'sample_source_3')     
            if sample_racks >= 4:
                sample_source_4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    6,                     
                    'sample_source_4')     
        if dilution_tubes == 'PCR_strips':
            if dilution_racks >= 1:
                dilution_dest_1 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    2,                     
                    'dilution_dest_1')     
            if dilution_racks >= 2:
                dilution_dest_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    5,                     
                    'dilution_dest_2')     
            if dilution_racks >= 3:
                dilution_dest_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    8,                     
                    'dilution_dest_3')     
            if dilution_racks >= 4:
                dilution_dest_4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    9,                     
                    'dilution_dest_4')       
        if water_tubes > 0: 
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                      "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                    labware_def_5mL = json.load(labware_file)
            tubes_5mL = protocol.load_labware_from_definition( 
                labware_def_5mL, 
                9, 
                '5mL_tubes')    
    else:
        if sample_tubes == 'PCR_strips':
            if sample_racks >= 1:
                sample_source_1 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    1,                                      
                    'sample_source_1')                      
            if sample_racks >= 2:
                sample_source_2 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    4,                                      
                    'sample_source_2')                      
            if sample_racks >= 3:   
                sample_source_3 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    3,                                      
                    'sample_source_3')                      
            if sample_racks >= 4: 
                sample_source_4 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    6,                                      
                    'sample_source_4')                      
        if dilution_tubes == 'PCR_strips':
            if dilution_racks >= 1:
                dilution_dest_1 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    2,                                      
                    'dilution_dest_1')                      
            if dilution_racks >= 2:
                dilution_dest_2 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    5,                                      
                    'dilution_dest_2')                      
            if dilution_racks >= 3:    
                dilution_dest_3 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    8,                                      
                    'dilution_dest_3')                      
            if dilution_racks >= 4:        
                dilution_dest_4 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    9,                                      
                    'dilution_dest_4')                          
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
        protocol.pause("I need "+ str(water_tubes) + " tube(s) with 5mL of water.")
# =============================================================================

# ALIQUOTING WATER=============================================================    
# =============================================================================
    ##### Variables for volume tracking and aliquoting
    if len([x for x in water_volumes if x > 0]) > 0:
        counter = 0 # to count how many tubes already emptied
        source = tubes_5mL.wells()[counter]
        destination = dilution_wells
        container = 'tube_5mL'
        start_height = vt.cal_start_height(container, 4800)
        current_height = start_height
              
        for i, (well, water_vol) in enumerate(zip(destination, water_volumes)):
          ## aliquot water in the correct wells, for each well do the following:  
            
            if water_vol > 0:
                dispension_vol = water_vol
                aspiration_vol = dispension_vol + (dispension_vol/100*2)
    
                if i == 0:
                    if len([x for x in water_volumes[i:i+15] if x < 20]) > 0:
                        p20.pick_up_tip()
                    if len([x for x in water_volumes[i:i+15] if x >= 20]) > 0:
                        p300.pick_up_tip()
                      ## If we are at the first well, start by picking up a tip
                elif i % 16 == 0:
                    try:
                        p20.drop_tip()
                    except:
                        pass
                    try:
                        p300.drop_tip()
                    except:
                        pass
                      ## Then, after every 16th well, try to drop tip
                    
                    if len([x for x in water_volumes[i:i+15] if x < 20]) > 0:
                        p20.pick_up_tip()
                    if len([x for x in water_volumes[i:i+15] if x >= 20]) > 0:
                        p300.pick_up_tip()                    
                      ## Pick up new tip if needed in next 16                    
                        
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
    
                if aspiration_vol > 20:
                    water_pipette = p300
                else:
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
        try: 
            p20.drop_tip()
        except:
            pass
        try:
            p300.drop_tip()
        except:
            pass
          ## when entire plate is full, try to drop tip  
# =============================================================================

# DILUTING SAMPLES=============================================================
# =============================================================================
    for sample_well, dilution_well, sample_vol, water_vol in zip(
            sample_wells, dilution_wells, sample_volumes, water_volumes):
        ## Combine each sample with a dilution_well and a destination well  ##
        if sample_vol > 17:
            sample_pipette = p300
        else:
            sample_pipette = p20
        sample_pipette.pick_up_tip()
          ## p20 picks up tip from location of specified starting_tip       ##
          ## or following                                                   ##
        sample_pipette.aspirate(sample_vol, sample_well)
          ## aspirate sample_volume_dil = volume for dilution from sample   ##
        if sample_pipette == p300:
            sample_pipette.air_gap(sample_vol)
        else:
            sample_pipette.air_gap(3)
          ## airgap
        sample_pipette.dispense(sample_vol, dilution_well)
          ## dispense sample_volume_dil = volume for dilution into dil_well ##
        sample_pipette.dispense(sample_vol * 2, dilution_well)
          ## instead of blow-out
        sample_pipette.drop_tip()
          ## Drop tip in trashbin on 12.                                    ##
         
# =============================================================================