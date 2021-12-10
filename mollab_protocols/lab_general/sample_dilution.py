"""
sample_dilution.py is a protocol written for EVE for the dilution of samples.
Also works for transferring samples, if you set dilution ratio to 0 or 1
First water is aliquoted:
    From a 5 mL tube in a 5mL tube rack.
    To dilution destination labware (96 wells plate, PCR strips or 1.5mL tubes)
The sample is taken:
    From the sample source labware (96 wells plate, PCR strips or 1.5mL tubes)
    To dilution destination labware (96 wells plate, PCR strips or 1.5mL tubes)
"""

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
  # Import volume_tracking module that is on the OT2                        ##
from mollab_modules import volume_tracking_v1 as vt
#   ## Import volume_tracking module for simulator                          ##
import math
  ## To do some calculations (rounding up)
# =============================================================================


# VARIABLES TO SET#!!!=========================================================
# =============================================================================
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
sample_volume = 50

# How many times do you want to dilute?
dilution_ratio = 0

# In what kind of tubes are the samples provided?
sample_tubes = 'PCR_strips'
  ## Options: 'plate_96', 'PCR_strips', 'tubes_1.5mL'
  
# In what kind of tubes should the dilutions be made?  
dilution_tubes = 'plate_96'
  ## Options: 'plate_96', 'PCR_strips', 'tubes_1.5mL'

# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# If applicable: What is the starting position of the 200µL tips?
starting_tip_p200 = 'A1'
  ## if not applicable, you do not have to change anything
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
    sample_dilution.py is a protocol written for EVE for the dilution of samples.
    First water is aliquoted:
        From a 5 mL tube in a 5mL tube rack.
        To dilution destination labware (96 wells plate, PCR strips 
                                         or 1.5mL tubes)
    The sample is taken:
        From the sample source labware (96 wells plate, PCR strips 
                                        or 1.5mL tubes)
        To dilution destination labware (96 wells plate, PCR strips 
                                         or 1.5mL tubes)
    """
# =============================================================================


# CALCULATED VARIABLES=========================================================
# =============================================================================
    dilution_volume = sample_volume * dilution_ratio
      ## How much volume you will end up with
    water_volume = dilution_volume - sample_volume
      ## How much water is needed for per sample
    water_tubes = math.ceil((water_volume * number_of_samples)/5000) + 1
      ## How many tubes of 5mL water are needed (+1 to be save)
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
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading pipettes and tips    
    
    if sample_volume <= 17 and water_volume <= 20 :
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  #labware definition
            11,                                 #deck position
            'tips_20_1')                        #custom name
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  #labware definition
            10,                                 #deck position
            'tips_20_2')                        #custom name    
        tips_20_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  #labware definition
            7,                                  #deck position
            'tips_20_3')                        #custom name    
        tips_20_4 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  #labware definition
            8,                                  #deck position
            'tips_20_4')                        #custom name  
        p20 = protocol.load_instrument(
            'p20_single_gen2',                  #instrument definition
            'left',                             #mount position
            tip_racks=[                         #assigned tiprack
                tips_20_1, tips_20_2, tips_20_3, tips_20_4])
        sample_pipette = p20
        water_pipette = p20
        
    elif sample_volume <= 17 and water_volume > 20 :
        tips_200_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',     #labware definition
            11,                                     #deck position
            'tips_200')                             #custom name
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',      #labware definition
            10,                                     #deck position
            'tips_20_1')                            #custom name
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',      #labware definition
            7,                                      #deck position
            'tips_20_2')                            #custom name    
        tips_20_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',      #labware definition
            8,                                      #deck position
            'tips_20_3')                            #custom name    
        p300 = protocol.load_instrument(
            'p300_single_gen2',                     #instrument definition
            'right',                                #mount position
            tip_racks=[tips_200_1])                   #assigned tiprack
        p20 = protocol.load_instrument(
            'p20_single_gen2',                          #instrument definition
            'left',                                     #mount position
            tip_racks=[tips_20_1, tips_20_2, tips_20_3])#assigned tiprack
        sample_pipette = p20
        water_pipette = p300
        
    elif sample_volume > 17 and water_volume > 20 :
        tips_200_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  #labware definition
            11,                                  #deck position
            'tips_200_1')                        #custom name
        tips_200_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  #labware definition
            10,                                  #deck position
            'tips_200_2')                        #custom name    
        tips_200_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  #labware definition
            7,                                   #deck position
            'tips_200_3')                        #custom name    
        tips_200_4 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  #labware definition
            8,                                   #deck position
            'tips_200_4')                        #custom name   
        p300 = protocol.load_instrument(
            'p300_single_gen2',                     #instrument definition
            'right',                                #mount position
            tip_racks=[tips_200_1, tips_200_2, tips_200_3, tips_200_4])                   #assigned tiprack
        sample_pipette = p300
        water_pipette = p300
        
    elif sample_volume > 17 and water_volume < 20 :
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',     #labware definition
            11,                                     #deck position
            'tips_20')                             #custom name
        tips_200_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      #labware definition
            10,                                     #deck position
            'tips_200_1')                            #custom name
        tips_200_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      #labware definition
            7,                                      #deck position
            'tips_200_2')                            #custom name    
        tips_200_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      #labware definition
            8,                                      #deck position
            'tips_200_3')                            #custom name    
        p300 = protocol.load_instrument(
            'p300_single_gen2',                     #instrument definition
            'right',                                #mount position
            tip_racks=[tips_200_1, tips_200_2, tips_200_3])#assigned tiprack
        p20 = protocol.load_instrument(
            'p20_single_gen2',                          #instrument definition
            'left',                                     #mount position
            tip_racks=[tips_20_1])#assigned tiprack
        sample_pipette = p300
        water_pipette = p20
    
    elif sample_volume <= 17 and water_volume > 20 :
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',       #labware definition
            11,                                      #deck position
            'tips_20')                               #custom name
        tips_200_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      #labware definition
            10,                                      #deck position
            'tips_200_1')                            #custom name
        tips_200_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      #labware definition
            7,                                       #deck position
            'tips_200_2')                            #custom name    
        tips_200_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',      #labware definition
            8,                                       #deck position
            'tips_200_3')                            #custom name    
        p300 = protocol.load_instrument(
            'p300_single_gen2',                            #instrument deftion
            'right',                                       #mount position
            tip_racks=[tips_200_1, tips_200_2, tips_200_3])#assigned tiprack
        p20 = protocol.load_instrument(
            'p20_single_gen2',                          #instrument definition
            'left',                                     #mount position
            tip_racks=[tips_20_1])                        #assigned tiprack
        sample_pipette = p300
        water_pipette = p20
    
    
    ##### Loading labware 
    if sample_tubes == 'plate_96':
        if sample_racks >= 1:            
            sample_source_1 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',        #labware definition
                1,                                      #deck position
                'sample_source_1')                      #custom name
        if sample_racks >= 2:          
            sample_source_2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',        #labware definition
                4,                                      #deck position
                'sample_source_2')                      #custom name
        if sample_racks >= 3:
            sample_source_3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',        #labware definition
                2,                                      #deck position
                'sample_source_3')                      #custom name
    if sample_tubes == 'tubes_1.5mL':
        if sample_racks >= 1:
            sample_source_1 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware definition
                1,                                      #deck position
                'sample_source_1')                      #custom name
        if sample_racks >= 2:    
            sample_source_2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware definition
                2,                                      #deck position
                'sample_source_2')                      #custom name
        if sample_racks >= 3:    
            sample_source_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware definition
                4,                                      #deck position
                'sample_source_3')                      #custom name
        if sample_racks >= 4:
            sample_source_4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware definition
                5,                                      #deck position
                'sample_source_4')                      #custom name
         
    if dilution_tubes == 'plate_96':
        if dilution_racks >= 1:        
            dilution_dest_1 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',        #labware definition
                6,                                      #deck position
                'dilution_dest_1')                      #custom name
        if dilution_racks >= 2:            
            dilution_dest_2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',        #labware definition
                3,                                      #deck position
                'dilution_dest_2')                      #custom name
        if dilution_racks >= 3:             
            dilution_dest_3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',        #labware definition
                5,                                      #deck position
                'dilution_dest_3')                      #custom name
    if dilution_tubes == 'tubes_1.5mL':
        if dilution_racks >= 1:
            dilution_dest_1 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware definition
                6,                                      #deck position
                'dilution_dest_1')                      #custom name
        if dilution_racks >= 2:    
            dilution_dest_2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware definition
                3,                                      #deck position
                'dilution_dest_2')                      #custom name
        if dilution_racks >= 3:    
            dilution_dest_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware definition
                5,                                      #deck position
                'dilution_dest_3')                      #custom name
        if dilution_racks >= 4:
            dilution_dest_4 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware definition
                2,                                      #deck position
                'dilution_dest_4')                      #custom name

    ##### !!! FOR ROBOT
    # if sample_tubes == 'PCR_strips':
    #     if sample_racks >= 1:
    #         sample_source_1 = protocol.load_labware(
    #             'pcrstrips_96_wellplate_200ul',         #labware definition
    #             1,                                      #deck position
    #             'sample_source_1')                      #custom name
    #     if sample_racks >= 2:
    #         sample_source_2 = protocol.load_labwware(
    #             'pcrstrips_96_wellplate_200ul',         #labware definition
    #             4,                                      #deck position
    #             'sample_source_2')                      #custom name
    #     if sample_racks >= 3:   
    #         sample_source_3 = protocol.load_labwware(
    #             'pcrstrips_96_wellplate_200ul',         #labware definition
    #             2,                                      #deck position
    #             'sample_source_3')                      #custom name
    #     if sample_racks >= 4: 
    #         sample_source_4 = protocol.load_labwware(
    #             'pcrstrips_96_wellplate_200ul',         #labware definition
    #             5,                                      #deck position
    #             'sample_source_4')                      #custom name
    # if dilution_tubes == 'PCR_strips':
    #     if dilution_racks >= 1:
    #         dilution_dest_1 = protocol.load_labware(
    #             'pcrstrips_96_wellplate_200ul',         #labware definition
    #             3,                                      #deck position
    #             'dilution_dest_1')                      #custom name
    #     if dilution_racks >= 2:
    #         dilution_dest_2 = protocol.load_labwware(
    #             'pcrstrips_96_wellplate_200ul',         #labware definition
    #             6,                                      #deck position
    #             'dilution_dest_2')                      #custom name
    #     if dilution_racks >= 3:    
    #         dilution_dest_3 = protocol.load_labwware(
    #             'pcrstrips_96_wellplate_200ul',         #labware definition
    #             5,                                      #deck position
    #             'dilution_dest_3')                      #custom name
    #     if dilution_racks >= 4:        
    #         dilution_dest_4 = protocol.load_labwware(
    #             'pcrstrips_96_wellplate_200ul',         #labware definition
    #             2,                                      #deck position
    #             'dilution_dest_4')                      #custom name    
    # tubes_5mL = protocol.load_labware(
    #     'eppendorfscrewcap_15_tuberack_5000ul',     #labware definition
    #     9,                                          #deck position
    #     'tubes_5mL')                                #custom name    
    
    ##### !!! FOR SIMULATOR
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
    if sample_tubes == 'PCR_strips':
        if sample_racks >= 1:
            sample_source_1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                1,                     #deck position
                'sample_source_1')     #custom name
        if sample_racks >= 2:
            sample_source_2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                4,                     #deck position
                'sample_source_2')     #custom name
        if sample_racks >= 3:
            sample_source_3 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                2,                     #deck position
                'sample_source_3')     #custom name
        if sample_racks >= 4:
            sample_source_4 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                5,                     #deck position
                'sample_source_4')     #custom name
    if dilution_tubes == 'PCR_strips':
        if dilution_racks >= 1:
            dilution_dest_1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                3,                     #deck position
                'dilution_dest_1')     #custom name
        if dilution_racks >= 2:
            dilution_dest_2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                6,                     #deck position
                'dilution_dest_2')     #custom name
        if dilution_racks >= 3:
            dilution_dest_3 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                5,                     #deck position
                'dilution_dest_3')     #custom name
        if dilution_racks >= 4:
            dilution_dest_4 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                2,                     #deck position
                'dilution_dest_4')     #custom name  
    with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
              "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
            labware_def_5mL = json.load(labware_file)
    tubes_5mL = protocol.load_labware_from_definition( 
        labware_def_5mL, #variable derived from opening json
        9, 
        '5mL_tubes')              
     
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
    H2O = []
    for row in (
            [tubes_5mL.rows_by_name()[row_name] for row_name in ['B','C']]):
        for well in row:
            H2O.append(well)
    
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
    if dilution_ratio > 1:
        protocol.pause("I need "+ str(water_tubes) + " tubes with 5mL of water."
                       " Put them in rows B and C of the tube rack please.")
# =============================================================================

# ALIQUOTING WATER=============================================================    
# =============================================================================
    ##### Variables for volume tracking and aliquoting
    if dilution_ratio > 1:
        counter = 0 # to count how many tubes already emptied
        source = H2O[counter]
        destination = dilution_wells
        start_height = vt.cal_start_height('tube_5mL', 5000)
        current_height = start_height
        container = 'tube_5mL'
        dispension_vol = water_volume
        aspiration_vol = dispension_vol + (dispension_vol/100*2)
        
        for i, well in enumerate(destination):
          ## aliquot water in the correct wells, for each well do the following:  
           
            if i == 0: 
                water_pipette.pick_up_tip()
                  ## If we are at the first well, start by picking up a tip.    ##
            elif i % 16 == 0:
                water_pipette.drop_tip()
                water_pipette.pick_up_tip()
                  ## Then, after every 16th well, drop tip and pick up new      ##
            
            current_height, pip_height, bottom_reached = vt.volume_tracking(
                container, dispension_vol, current_height)
                  ## call volume_tracking function, obtain current_height,      ##
                  ## pip_height and whether bottom_reached.                     ##
            
            if bottom_reached:
              ## continue with next tube, reset vt                              ##
                current_height = start_height
                current_height, pip_height, bottom_reached = (
                    vt.volume_tracking(
                        container, dispension_vol, current_height))
                counter = counter + 1
                source = H2O[counter]
                aspiration_location = source.bottom(current_height)
                protocol.comment(
                    "Continue with tube " + str(counter) + " of water")
           
            else:
                aspiration_location = source.bottom(pip_height)
                  ## Set the location of where to aspirate from.                ##
    
            #### The actual aliquoting of water
            water_pipette.aspirate(aspiration_vol, aspiration_location)
              ## Aspirate the amount specified in aspiration_vol from the       ##
              ## location specified in aspiration_location.                     ##
            water_pipette.dispense(dispension_vol, well)
              ## Dispense the amount specified in dispension_vol to the         ##
              ## location specified in well (looping through plate)             ##
            water_pipette.dispense(10, aspiration_location)
              ## Alternative for blow-out, make sure the tip doesn't fill       ##
              ## completely when using a disposal volume by dispensing some     ##
              ## of the volume after each pipetting step. (blow-out too many    ##
              ## bubbles)                                                       ##
        water_pipette.drop_tip()
          ## when entire plate is full, drop tip                                ##
# =============================================================================

# DILUTING SAMPLES=============================================================
# =============================================================================
    for sample_well, dilution_well in zip(sample_wells, dilution_wells):
        ## Combine each sample with a dilution_well and a destination well  ##
        sample_pipette.pick_up_tip()
          ## p20 picks up tip from location of specified starting_tip       ##
          ## or following                                                   ##
        sample_pipette.aspirate(sample_volume, sample_well)
          ## aspirate sample_volume_dil = volume for dilution from sample   ##
        sample_pipette.dispense(sample_volume, dilution_well)
          ## dispense sample_volume_dil = volume for dilution into dil_well ##
        if water_volume > 0:
            sample_pipette.mix(3, sample_volume + 3, dilution_well)
          ## pipette up&down 3x to get everything from the tip              ##
        sample_pipette.dispense(20, dilution_well)
          ## instead of blow-out
        sample_pipette.drop_tip()
          ## Drop tip in trashbin on 12.                                    ##
         
# =============================================================================

