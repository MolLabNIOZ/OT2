# =============================================================================
# Author(s): Sanne Vreugdenhil & Maartje Brouwer
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
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
  # Import volume_tracking module that is on the OT2                        ##
from mollab_modules import volume_tracking_v1 as vt
  ## Import volume_tracking module for simulator                          ##
# =============================================================================

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
number_of_samples = 82   # max 96 - NTC
  ## How many samples do you want to include?                           ##
number_of_NTCs = 0
sample_tubes = 'PCR_strips'
  ## What kind of tubes will the samples be in?
  ## Options: 'PCR_strips' or 'tubes_1.5mL'
if sample_tubes == 'PCR_strips':
    sample_strip_positions = ['2', '5', '8','11']
    ## optional: ['2', '7', '11'] or ['2', '5', '8','11']
water_tube_type = 'tubes_1.5mL'
  ## What kind of tube will the water be in?
  ## Options: 'tubes_1.5mL'or 'tubes_5mL'
PCR_tubes = 'PCR_strips'
  ## What kind of tubes will the PCR be in?
  ## Options: 'PCR_strips' or 'plate_96'
if PCR_tubes == 'PCR_strips':
    strip_positions = ['2', '5', '8','11']
    ## optional: ['2', '7', '11'] or ['2', '5', '8','11']
    ## max 2 racks with strips!
starting_tip_p20 = 'A3'
  ## The starting_tip is the location of first pipette tip in the box   ##
max_DNA_volume = 3
  ## highest DNA volume, to add up to with water if needed
DNA_µL_list = ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 2, 2, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 3, 3, 0, 0, 3, 1, 1, 1, 3, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
  ##How much DNA should be added for each sample (µL)
# =============================================================================


# CALCULATED VARIABLES=========================================================
# =============================================================================
reactions = number_of_samples + number_of_NTCs
if PCR_tubes == 'PCR_strips':
    if strip_positions == ['2', '5', '8','11']:
        PCR_tubes_per_rack = 32
    elif strip_positions == ['2', '7','11']:
        PCR_tubes_per_rack = 24
    PCR_racks = math.ceil(reactions/PCR_tubes_per_rack)
  ## How many PCR tube racks
if sample_tubes == 'tubes_1.5mL':
    sample_racks = math.ceil((number_of_samples + 1) / 24)
elif sample_tubes == 'PCR_strips':
    if sample_strip_positions == ['2', '5', '8','11']:
        sample_tubes_per_rack = 32
    elif sample_strip_positions == ['2', '7','11']:
        sample_tubes_per_rack = 24
    sample_racks = math.ceil(reactions/sample_tubes_per_rack)
  ## How many tube_racks are needed (1,2,3 or 4) +1 for water_tube
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'PCR_different_sample_volumes_EVE',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
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
        'tipone_96_tiprack_20uL',  
        3,                                  
        'tipone_20tips_1')                         #custom name       
    tips_20_2 = protocol.load_labware(
        'tipone_96_tiprack_20uL',  
        6,                                  
        'tipone_20tips_2')                         #custom name

    # Tube_racks & plates
    if sample_tubes == 'tube_1.5mL':
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
    
    elif sample_tubes == 'PCR_strips':
        sample_tubes_1 = protocol.load_labware( 
            'pcrstrips_96_wellplate_200ul',
            1,                                                       #deck position
            'sample_tubes_1')                                        #custom name
        if sample_racks >= 2:
            sample_tubes_2 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul', 
                4,                                                       #deck pos
                'sample_tubes_2')                                        #cust name
        if sample_racks >= 3:
            sample_tubes_3 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',
                7,                                                       #deck pos
                'sample_tubes_3')                                        #cust name
        if sample_racks >= 4:
            sample_tubes_4 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',
                10,                                                      #deck pos
                'sample_tubes_4')                                        #cust name
        
         
    if water_tube_type == 'tube_1.5mL':
        water_tube = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            9,
            'mastermix_tube')
    elif water_tube_type == 'tube_5mL':
        water_tube = protocol.load_labware(
            'eppendorfscrewcap_15_tuberack_5000ul',
            9,                                     
            'water_tube')
    
    if PCR_tubes == 'PCR_strips':
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
      
    if PCR_tubes == 'plate_96':
       PCR_1 = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',#labware definition
            2,                                      #deck position
            '96well_plate_NIOZholder')                    #custom name  

    
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
    if sample_tubes == 'tubes_1.5mL':
        sample_sources = sample_tubes_1.wells()
        if sample_racks >= 2:
            sample_sources = sample_sources + sample_tubes_2.wells()
        if sample_racks >= 3:
            sample_sources = sample_sources + sample_tubes_3.wells()    
        if sample_racks >= 4:
            sample_sources = sample_sources + sample_tubes_4.wells()
    
    if sample_tubes == 'PCR_strips':
        sample_columns = (
            ([sample_tubes_1.columns_by_name()[column_name]
            for column_name in sample_strip_positions]))        
        if sample_racks >= 2:
            sample_columns_2 = (
            ([sample_tubes_2.columns_by_name()[column_name]
              for column_name in sample_strip_positions]))
            sample_columns = sample_columns + sample_columns_2
        if sample_racks >= 3:
            sample_columns_3 = (
            ([sample_tubes_3.columns_by_name()[column_name]
              for column_name in sample_strip_positions]))
            sample_columns = sample_columns + sample_columns_3
        if sample_racks >= 4:
            sample_columns_4 = (
            ([sample_tubes_4.columns_by_name()[column_name]
              for column_name in sample_strip_positions]))
            sample_columns = sample_columns + sample_columns_4
        for column in sample_columns:
            for well in column:
                sample_sources.append(well)
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
        p20.pick_up_tip()
        p20.aspirate(sample_vol, sample_tube)
        p20.dispense(sample_vol, well)
        sample_mix_vol = sample_vol + 3
          ## primer_mix_vol = volume for pipetting up and down              ##
        p20.mix(3, sample_mix_vol, well)
        p20.dispense(10, well)
        p20.drop_tip()
        
        water_vol = max_DNA_volume - sample_vol
          ## volume of water needed to add a total of 5µL
        if water_vol > 0:
            p20.pick_up_tip()
            p20.aspirate(water_vol, water_tube['A1'])
            p20.dispense(water_vol, well)
            sample_mix_vol = water_vol + 3
              ## primer_mix_vol = volume for pipetting up and down              ##
            p20.mix(3, sample_mix_vol, well)
            p20.dispense(10, well)
            p20.drop_tip()
        
    ## Add water to NTC
    water_vol = max_DNA_volume
    well = sample_destinations[-1]
    p20.pick_up_tip()
    p20.aspirate(water_vol, water_tube['A1'])
    p20.dispense(water_vol, well)
    sample_mix_vol = sample_vol + 3
      ## primer_mix_vol = volume for pipetting up and down              ##
    p20.mix(3, sample_mix_vol, well)
    p20.dispense(10, well)
    p20.drop_tip()

            
# =============================================================================
    