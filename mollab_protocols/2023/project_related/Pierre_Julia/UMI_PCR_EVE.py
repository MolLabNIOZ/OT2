# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 210916
# Description: 
#   - add samples from 1.5 mL tubes to plate or strips
#   - add different volumes of DNA + add up to a max volume with water
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import math
  ## To do some calculations (rounding up)
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# =============================================================================

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
number_of_samples = 44   # max 96 
  ## How many samples do you want to include? Including PC and NTC          ##
PCR_tubes = 'PCR_strips'
  ## What kind of tubes will the PCR be in?
  ## Options: 'PCR_strips' or 'plate_96'
if PCR_tubes == 'PCR_strips':
    strip_positions = ['2', '5', '8','11']
    ## optional: ['2', '7', '11'] or ['2', '5', '8','11']
    ## max 2 racks with strips!
starting_tip_p20 = 'A5'
  ## The starting_tip is the location of first pipette tip in the box       ##
max_DNA_volume = 5
  ## highest DNA volume, to add up to with water if needed
DNA_µL_list = ([3.0, 3.0, 5.0, 5.0, 5.0, 5.0, 2.5, 3.25,
                2.0, 5.0, 3.25, 3.25, 2.5, 3.0, 2.5, 1.5,
                2.5, 2.0, 3.5, 3.25, 2.25, 3.0, 4.0, 2.75,
                3.0, 1.5, 1.25, 1.25, 2.75, 1.0, 1.5, 2.0,
                2.75, 2.25, 2.25, 1.75, 2.25, 3.0, 1.5, 1.25,
                1.0, 1.25, 5.0, 0.0])
  ##How much DNA should be added for each sample (µL)
# =============================================================================


# CALCULATED VARIABLES=========================================================
# =============================================================================
if PCR_tubes == 'PCR_strips':
    if strip_positions == ['2', '5', '8','11']:
        PCR_tubes_per_rack = 32
    elif strip_positions == ['2', '7','11']:
        PCR_tubes_per_rack = 24
    PCR_racks = math.ceil(number_of_samples/PCR_tubes_per_rack)
  ## How many PCR tube racks
sample_racks = math.ceil((number_of_samples + 1) / 24)
  ## How many tube_racks are needed (1,2,3 or 4) +1 for water_tube
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'PCR_different_sample_volumes_EVE',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('PCR - adding samples in different volumes'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Adding samples from 1.5 mL tubes to PCR_strips.
    different DNA volumes + water to add up
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    
    #pipette tips
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        3,                                  #deck position
        '20tips_1')                         #custom name       
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        6,                                 #deck position
        '20tips_2')                         #custom name

    # Tube_racks & plates
    sample_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        1,                                                       #deck position
        'sample_tubes_1')                                        #custom name
    if sample_racks >= 2:
        sample_tubes_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            4,                                                       #deck pos
            'sample_tubes_2')                                        #cust name
    if sample_racks >= 3:
        sample_tubes_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            7,                                                       #deck pos
            'sample_tubes_3')                                        #cust name
    if sample_racks >= 4:
        sample_tubes_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            10,                                                      #deck pos
            'sample_tubes_4')                                        #cust name
    
    if PCR_tubes == 'PCR_strips':
   ### !!! OPTION 1: ROBOT         
        PCR_1 = protocol.load_labware(
          'pcrstrips_96_wellplate_200ul',    #labware definition
          2,                                 #deck position
          'PCR_tube_1')                      #custom name
        if PCR_racks >= 2:
            PCR_2 = protocol.load_labware(
                  'pcrstrips_96_wellplate_200ul',    #labware definition
                  5,                                 #deck position
                  'PCR_tube_2')                      #custom name
        if PCR_racks >= 3:
            PCR_3 = protocol.load_labware(
                  'pcrstrips_96_wellplate_200ul',    #labware definition
                  8,                                 #deck position
                  'PCR_tube_3')                      #custom name
        if PCR_racks == 4:
            PCR_4 = protocol.load_labware(
                  'pcrstrips_96_wellplate_200ul',    #labware definition
                  11,                                #deck position
                  'PCR_tube_3')                      #custom name        
    
    ##### !!! OPTION 2: SIMULATOR         
        # with open("labware/pcrstrips_96_wellplate_200ul/"
        #             "pcrstrips_96_wellplate_200ul.json") as labware_file:
        #           labware_def_pcrstrips = json.load(labware_file)
        # PCR_1 = protocol.load_labware_from_definition( 
        #       labware_def_pcrstrips, #variable derived from opening json
        #       2,                     #deck position
        #       'PCR_tube_1')          #custom name
        # if PCR_racks >= 2:
        #     PCR_2 = protocol.load_labware_from_definition( 
        #           labware_def_pcrstrips, #variable derived from opening json
        #           5,                     #deck position
        #           'PCR_tube_2')          #custom name
        # if PCR_racks >= 3:
        #     PCR_3 = protocol.load_labware_from_definition( 
        #           labware_def_pcrstrips, #variable derived from opening json
        #           8,                     #deck position
        #           'PCR_tube_2')          #custom name
        # if PCR_racks == 4:
        #     PCR_4 = protocol.load_labware_from_definition( 
        #           labware_def_pcrstrips, #variable derived from opening json
        #           11,                    #deck position
        #           'PCR_tube_4')          #custom name
    
    if PCR_tubes == 'plate_96':
       #### !!! OPTION 1: ROBOT 
        PCR_1 = protocol.load_labware(
            'biorad_qpcr_plate_eppendorf_cool_rack',#labware definition
            2,                                      #deck position
            '96well_plate_rack')                    #custom name  
       ##### !!! OPTION 2: SIMULATOR
        # with open("labware/biorad_qpcr_plate_eppendorf_cool_rack/"
        #             "biorad_qpcr_plate_eppendorf_cool_rack.json") as labware_file:
        #           labware_def_cool_rack = json.load(labware_file)
        # PCR_1 = protocol.load_labware_from_definition( 
        #     labware_def_cool_rack,   #variable derived from opening json
        #     2,                       #deck position
        #     '96well_plate_rack')     #custom name 
    
    # Pipettes
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1, tips_20_2])   #assigned tiprack
    
# =============================================================================

# PREDIFINED VARIABLES=========================================================
# =============================================================================
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
      ## The starting_tip is the location of first pipette tip in the box   ##

    # Sample source wells
    sample_sources = []
      ## Create an empty list to append wells to.                           ##
    sample_sources = sample_tubes_1.wells()
    if sample_racks >= 2:
        sample_sources = sample_sources + sample_tubes_2.wells()
    if sample_racks >= 3:
        sample_sources = sample_sources + sample_tubes_3.wells()    
    if sample_racks >= 4:
        sample_sources = sample_sources + sample_tubes_4.wells()
    water_tube = sample_sources[-1]
    sample_sources = sample_sources[:number_of_samples]
    
    # Destination wells
    sample_destinations = []
      ## Create an empty list to append wells to.                           ##
    if PCR_tubes == 'plate_96':
        sample_destinations = PCR_1.wells()
    elif PCR_tubes == 'PCR_strips':
        PCR_columns = (
            ([PCR_1.columns_by_name()[column_name]
            for column_name in strip_positions]))        
        if PCR_racks >= 2:
            PCR_columns_2 = (
            ([PCR_2.columns_by_name()[column_name]
              for column_name in strip_positions]))
            PCR_columns = PCR_columns + PCR_columns_2
        if PCR_racks >= 3:
            PCR_columns_3 = (
            ([PCR_3.columns_by_name()[column_name]
              for column_name in strip_positions]))
            PCR_columns = PCR_columns + PCR_columns_3
        if PCR_racks >= 4:
            PCR_columns_4 = (
            ([PCR_4.columns_by_name()[column_name]
              for column_name in strip_positions]))
            PCR_columns = PCR_columns + PCR_columns_4
        for column in PCR_columns:
            for well in column:
                sample_destinations.append(well)       
    
    sample_destinations = sample_destinations[:number_of_samples + 1]
        
    
# ADDING SAMPLES AND WATER=====================================================
# =============================================================================
    ## Loop through source and destination wells
    for sample_tube, well, sample_vol in zip(
            sample_sources, sample_destinations, DNA_µL_list
            ):
        if sample_vol > 0:
            p20.pick_up_tip()
            p20.aspirate(sample_vol, sample_tube)
            p20.dispense(sample_vol, well)
            sample_mix_vol = sample_vol + 3
              ## mix_vol = volume for pipetting up and down              ##
            p20.mix(3, sample_mix_vol, well)
            p20.dispense(10, well)
            p20.drop_tip()
        
        water_vol = max_DNA_volume - sample_vol
          ## volume of water needed to add a total of max_DNA_volume
        if water_vol > 0:
            p20.pick_up_tip()
            p20.aspirate(water_vol, water_tube)
            p20.dispense(water_vol, well)
            mix_vol = water_vol + 3
              ## mix_vol = volume for pipetting up and down              ##
            p20.mix(3, mix_vol, well)
            p20.dispense(10, well)
            p20.drop_tip()
        
        
# =============================================================================
    