"""
sample_dilution.py is a protocol written for EVE for the dilution of samples.
Also works for transferring samples, if you set dilution ratio to 0 or 1
Also works if you want different dilutions for every sample. Enter a list of
sample_volumes and a total_volume to add up to with water.
First water is aliquoted (if necesarry):
    From 5 mL tube(s) in a 5mL tube rack.
    To dilution destination labware (96 wells plate, PCR strips or 1.5mL tubes)
The sample is taken:
    From the sample source labware (96 wells plate, PCR strips or 1.5mL tubes)
    To dilution destination labware (96 wells plate, PCR strips or 1.5mL tubes)
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# If applicable: What is the starting position of the 200µL tips?
starting_tip_p200 = 'A1'
  ## if not applicable, you do not have to change anything
  
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
sample_volume = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
  ## can be one volume or a list of volumes
total_volume = 25
  ## If you have a list of sample_volumes,what is the total volume you want
  ## total_volume -  sample_volume = water_volume
  ## If you do not have a list, but want a dilution ratio,
  ## total_volume is not used

# How many times do you want to dilute?
dilution_ratio = 50
  ## if you do not want to dilute but only transfer samples, enter 0 or 1
  ## if all samples have a different ratio enter a list of sample_volumes and 
  ## a total volume. 

# In what kind of tubes are the samples provided?
sample_tubes = 'tubes_1.5mL'
  ## Options: 'plate_96', 'PCR_strips', 'tubes_1.5mL'
  
# In what kind of tubes should the dilutions be made?  
dilution_tubes = 'PCR_strips'
  ## Options: 'plate_96', 'PCR_strips', 'tubes_1.5mL'

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


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'sample_dilution.py',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Sample dilution protocol.'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    sample_dilution.py is a protocol written for EVE for the dilution of 
    samples.
    Also works for transferring samples, if you set dilution ratio to 0 or 1
    Also works if you want different dilutions for every sample. Enter a list 
    of sample_volumes and a total_volume to add up to with water.
    First water is aliquoted (if necesarry):
        From 5 mL tube(s) in a 5mL tube rack.
        To dilution destination labware 
        (96 wells plate, PCR strips or 1.5mL tubes)
    The sample is taken:
        From the sample source labware 
        (96 wells plate, PCR strips or 1.5mL tubes)
    """
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
    if not isinstance(sample_volume, list):
        sample_volumes = []
        water_volume = [] 
        end_volume = sample_volume * dilution_ratio
          ## How much volume you will end up with
        for i in range(number_of_samples):
            sample_volumes.append(sample_volume)
            water_volume.append(end_volume - sample_volume)
              ## make lists with water_volume and sample_volume
    else:
        water_volume = []
        for i, sample_vol in enumerate(sample_volume):
            water = total_volume - sample_vol
            water_volume.append(water)
            sample_volumes = sample_volume
              ## Make list with water_volume
    
    total_water_volume = sum(water_volume)
    water_tubes = math.ceil((total_water_volume)/4900)
      ## How many tubes of 5mL water are needed 
    
    if sample_tubes == 'tubes_1.5mL':
        sample_racks = math.ceil(number_of_samples / 24)
    elif sample_tubes == 'PCR_strips':
        sample_racks = math.ceil(number_of_samples / 48)
    elif sample_tubes == 'plate_96':
        sample_racks = math.ceil(number_of_samples / 96)
      ## How many sample_racks are needed (1,2,3 or 4)
    if dilution_tubes == 'tubes_1.5mL':
        dilution_racks = math.ceil(number_of_samples / 24)
    elif dilution_tubes == 'PCR_strips':
        dilution_racks = math.ceil(number_of_samples / 48)
    elif dilution_tubes == 'plate_96':
        dilution_racks = math.ceil(number_of_samples / 96)
      ## How many dilution_racks are needed (1 or 2)

    water_tips_20 = len([x for x in water_volume if x < 20])
    water_tips_200 = len([x for x in water_volume if x >= 20])
    sample_tips_20 = len([x for x in sample_volumes if x <= 17])
    sample_tips_200 = len([x for x in sample_volumes if x > 17])
    ## How many p20 / p200 tips do you need?
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading pipettes and tips    
    tips_20 = []
    tips_200 = []
    
    if sample_tips_20 + water_tips_20 > 0:
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',      
            11,                                     
            'tips_20_1')                            
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',      
            10,                                     
            'tips_20_2')                            
        tips_20 = [tips_20_1,tips_20_2]
        if sample_tips_200 + water_tips_200 > 0:
            tips_200_1 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',     
                7,                                      
                'tips_200_1')                           
            tips_200_2 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',     
                8,                                      
                'tips_200_2')                           
        tips_200 = [tips_200_1,tips_200_2]
    
    elif sample_tips_200 + water_tips_200 > 0:
        tips_200_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',     
            11,                                     
            'tips_200_1')                           
        tips_200_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',     
            10,                                     
            'tips_200_2')                           
        tips_200 = [tips_200_1,tips_200_2]
        if sample_tips_200 + water_tips_200 > 96:
            tips_200_3 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',     
                7,                                      
                'tips_200_3')                           
    
    
    if sample_tips_20 + water_tips_20 > 96:
        tips_20_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',      
            7,                                      
            'tips_20_3')                            
        tips_20 = tips_20.append(tips_20_3)
        if sample_tips_200 + water_tips_200 > 0:
            tips_200_1 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul', 
                8,                                  
                'tips_200_1')                       
            tips_200 = tips_200.append(tips_200_1)
    elif sample_tips_200 + water_tips_200 > 96:
        tips_200_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',     
            7,                                      
            'tips_200_3')                           
        tips_200 = tips_200.append(tips_200_3)
        
    if sample_tips_20 + water_tips_20 > 192:
        tips_20_4 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',      
            8,                                      
            'tips_20_4')                              
        tips_20 = tips_20.append(tips_20_4)
    elif sample_tips_200 + water_tips_200 > 192:
        tips_200_4 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',     
            8,                                      
            'tips_200_4')                             
        tips_200 = tips_200.append(tips_200_4)
    
    ##### Loading pipettes
    if sample_tips_20 + water_tips_20 > 0:
        p20 = protocol.load_instrument(
            'p20_single_gen2',
            'left',
            tip_racks = tips_20)
    if sample_tips_200 + water_tips_200 > 0:
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
                2,
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
                2,
                'sample_source_2')
        if sample_racks >= 3:    
            sample_source_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                4,
                'sample_source_3')
        if sample_racks >= 4:
            sample_source_4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                5,
                'sample_source_4')
         
    if dilution_tubes == 'plate_96':
        if dilution_racks >= 1:        
            dilution_dest_1 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                6,
                'dilution_dest_1')
        if dilution_racks >= 2:            
            dilution_dest_2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                3,
                'dilution_dest_2')
        if dilution_racks >= 3:             
            dilution_dest_3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                5,
                'dilution_dest_3')
    if dilution_tubes == 'tubes_1.5mL':
        if dilution_racks >= 1:
            dilution_dest_1 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                6,                                      
                'dilution_dest_1')                      
        if dilution_racks >= 2:    
            dilution_dest_2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                3,                                      
                'dilution_dest_2')                      
        if dilution_racks >= 3:    
            dilution_dest_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                5,                                      
                'dilution_dest_3')                      
        if dilution_racks >= 4:
            dilution_dest_4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                2,                                      
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
                    2,                     
                    'sample_source_3')     
            if sample_racks >= 4:
                sample_source_4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    5,                     
                    'sample_source_4')     
        if dilution_tubes == 'PCR_strips':
            if dilution_racks >= 1:
                dilution_dest_1 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    3,                     
                    'dilution_dest_1')     
            if dilution_racks >= 2:
                dilution_dest_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    6,                     
                    'dilution_dest_2')     
            if dilution_racks >= 3:
                dilution_dest_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    5,                     
                    'dilution_dest_3')     
            if dilution_racks >= 4:
                dilution_dest_4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    2,                     
                    'dilution_dest_4')       
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
                sample_source_2 = protocol.load_labwware(
                    'pcrstrips_96_wellplate_200ul',         
                    4,                                      
                    'sample_source_2')                      
            if sample_racks >= 3:   
                sample_source_3 = protocol.load_labwware(
                    'pcrstrips_96_wellplate_200ul',         
                    2,                                      
                    'sample_source_3')                      
            if sample_racks >= 4: 
                sample_source_4 = protocol.load_labwware(
                    'pcrstrips_96_wellplate_200ul',         
                    5,                                      
                    'sample_source_4')                      
        if dilution_tubes == 'PCR_strips':
            if dilution_racks >= 1:
                dilution_dest_1 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    3,                                      
                    'dilution_dest_1')                      
            if dilution_racks >= 2:
                dilution_dest_2 = protocol.load_labwware(
                    'pcrstrips_96_wellplate_200ul',         
                    6,                                      
                    'dilution_dest_2')                      
            if dilution_racks >= 3:    
                dilution_dest_3 = protocol.load_labwware(
                    'pcrstrips_96_wellplate_200ul',         
                    5,                                      
                    'dilution_dest_3')                      
            if dilution_racks >= 4:        
                dilution_dest_4 = protocol.load_labwware(
                    'pcrstrips_96_wellplate_200ul',         
                    2,                                      
                    'dilution_dest_4')                          
        tubes_5mL = protocol.load_labware(
            'eppendorfscrewcap_15_tuberack_5000ul',     
            9,                                          
            'tubes_5mL')                                    
    
          
    

    ##### MB: I think this can be removed... but not completely sure because I
        #don't know why it was her ein the first place.
    # # Setting sample_source
    # if sample_racks == 1: 
    #     sample_source_1 = sample_source_1 
    # elif sample_racks == 2:
    #     sample_source_1 = sample_source_1
    #     sample_source_2 = sample_source_2
    # elif sample_racks == 3:
    #     sample_source_1 = sample_source_1
    #     sample_source_2 = sample_source_2
    #     sample_source_3 = sample_source_3
    # elif sample_racks == 4:
    #     sample_source_1 = sample_source_1
    #     sample_source_2 = sample_source_2
    #     sample_source_3 = sample_source_3
    #     sample_source_4 = sample_source_4

    # # Setting dilution_dest
    # if dilution_racks == 1:
    #     dilution_dest_1 = dilution_dest_1   
    # elif dilution_racks == 2:
    #     dilution_dest_1 = dilution_dest_1
    #     dilution_dest_2 = dilution_dest_2
    # elif dilution_racks == 3:
    #     dilution_dest_1 = dilution_dest_1
    #     dilution_dest_2 = dilution_dest_2
    #     dilution_dest_3 = dilution_dest_3
    # elif dilution_racks == 4:
    #     dilution_dest_1 = dilution_dest_1
    #     dilution_dest_2 = dilution_dest_2
    #     dilution_dest_3 = dilution_dest_3
    #     dilution_dest_4 = dilution_dest_4
# =============================================================================

# SETTING LOCATIONS#!!!========================================================
# =============================================================================
    ##### Setting starting tip
    if p20:
        p20.starting_tip = tips_20_1.well(starting_tip_p20)
    if p300:
        p300.starting_tip = tips_200_1.well(starting_tip_p200)
      ## The starting_tip is the location of first pipette tip in the box   ##
      
    ##### Setting tube locations
   
    sample_wells = []
    if sample_tubes == 'PCR_strips':
        columns_odd = ['1','3','5','7','9','11']
        sample_columns = []
        if sample_racks >= 1:
            sample_columns_1 = (                                                           
                ([sample_source_1.columns_by_name()[column_name] 
                  for column_name in columns_odd])) 
            for column in sample_columns_1:
                sample_columns.append(column)
        if sample_racks >= 2:
            sample_columns_2 = ( 
                ([sample_source_2.columns_by_name()[column_name] 
                  for column_name in columns_odd]))
            for column in sample_columns_2:
                sample_columns.append(column)
        if sample_racks >= 3:
            sample_columns_3 = ( 
                ([sample_source_3.columns_by_name()[column_name] 
                  for column_name in columns_odd]))
            for column in sample_columns_3:
                sample_columns.append(column)
        if sample_racks >= 4:
            sample_columns_4 = ( 
                ([sample_source_4.columns_by_name()[column_name] 
                  for column_name in columns_odd]))
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
        columns_odd = ['1','3','5','7','9','11']
        dilution_columns = []
        if dilution_racks >= 1:
            dilution_columns_1 = (                                                           
                ([dilution_dest_1.columns_by_name()[column_name] 
                  for column_name in columns_odd])) 
            for column in dilution_columns_1:
                dilution_columns.append(column)
        if dilution_racks >= 2:
            dilution_columns_2 = ( 
                ([dilution_dest_2.columns_by_name()[column_name] 
                  for column_name in columns_odd]))
            for column in dilution_columns_2:
                dilution_columns.append(column)
        if dilution_racks >= 3:
            dilution_columns_3 = ( 
                ([dilution_dest_3.columns_by_name()[column_name] 
                  for column_name in columns_odd]))
            for column in dilution_columns_3:
                dilution_columns.append(column)
        if dilution_racks >= 4:
            dilution_columns_4 = ( 
                ([dilution_dest_4.columns_by_name()[column_name] 
                  for column_name in columns_odd]))
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
    if len([x for x in water_volume if x > 0]) > 0:
        protocol.pause("I need "+ str(water_tubes) + " tube(s) with 5mL of water.")
# =============================================================================

# ALIQUOTING WATER=============================================================    
# =============================================================================
    ##### Variables for volume tracking and aliquoting
    if len([x for x in water_volume if x > 0]) > 0:
        counter = 0 # to count how many tubes already emptied
        source = tubes_5mL.wells()[counter]
        destination = dilution_wells
        start_height = vt.cal_start_height('tube_5mL', 5000)
        current_height = start_height
        container = 'tube_5mL'

        
        for i, (well, water_vol) in enumerate(zip(destination, water_volume)):
          ## aliquot water in the correct wells, for each well do the following:  
            
            if water_vol > 0:
              
                dispension_vol = water_vol
                aspiration_vol = dispension_vol + (dispension_vol/100*2)
    
    
                if i == 0:
                    if len([x for x in water_volume[i:i+15] if x < 20]) > 0:
                        p20.pick_up_tip()
                    if len([x for x in water_volume[i:i+15] if x >= 20]) > 0:
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
                    
                    if len([x for x in water_volume[i:i+15] if x < 20]) > 0:
                        p20.pick_up_tip()
                    if len([x for x in water_volume[i:i+15] if x >= 20]) > 0:
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
            sample_wells, dilution_wells, sample_volumes, water_volume):
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
        sample_pipette.dispense(sample_vol, dilution_well)
          ## dispense sample_volume_dil = volume for dilution into dil_well ##
        if water_vol > 0:
            sample_pipette.mix(3, sample_vol + 3, dilution_well)
          ## pipette up&down 3x to get everything from the tip              ##
        sample_pipette.dispense(20, dilution_well)
          ## instead of blow-out
        sample_pipette.drop_tip()
          ## Drop tip in trashbin on 12.                                    ##
         
# =============================================================================