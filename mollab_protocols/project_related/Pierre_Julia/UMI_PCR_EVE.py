# =============================================================================
# Author(s): Sanne Vreugdenhil & Maartje Brouwer
# Creation date: 210916
# Description: 
#   - add samples from 1.5 mL tubes to 96 wells plate
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
from data.user_storage.mollab_modules import volume_tracking_v1 as vt
  # Import volume_tracking module that is on the OT2                        ##
# from mollab_modules import volume_tracking_v1 as vt
  ## Import volume_tracking module for simulator                          ##
# =============================================================================

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
number_of_samples = 48   # max 96 - NTC
  ## How many samples do you want to include?                           ##
number_of_NTCs = 1
PCR_tubes = 'PCR_strips'
  ## What kind of tubes will the PCR be in?
  ## Options: 'PCR_strips' or 'plate_96'
if PCR_tubes == 'PCR_strips':
    strip_positions = ['2', '5', '8','11']
    ## max 2 racks with strips!  
starting_tip_p20 = 'A3'
  ## The starting_tip is the location of first pipette tip in the box   ##
DNA_µL_list = ([5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.5, 5.0, 2.5, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 5.0, 2.5, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 4.0, 5.0, 5.0, 5.0, 5.0, 3.5, 5.0, 3.0, 5.0, 4.0, 4.0, 3.5, 4.0, 3.5, 2.0, 3.5, 3.0, 5.0, 5.0, 3.5, 4.0, 5.0, 4.0, 4.0, 1.5, 1.0, 1.0, 4.0, 0.75, 2.0, 3.5, 4.0, 3.5, 3.5, 3.0, 3.5, 4.0, 2.5, 1.0, 1.0, 1.0, 3.5, 5.0, 4.0, 5.0, 5.0, 5.0, 5.0, 3.5, 3.5, 5.0, 3.5, 5.0, 5.0, 4.0, 4.0, 4.0, 2.5, 4.0, 2.5, 3.0, 3.5, 4.0, 4.0, 5.0, 4.0, 4.0, 5.0, 5.0, 5.0, 3.5, 4.0, 1.5, 2.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 4.0, 3.5, 4.0, 2.0, 0.75, 1.0, 2.5, 2.5, 3.5, 1.0, 4.0, 4.0, 3.0, 4.0, 2.5, 3.0, 0.75, 0.75, 0.75, 3.5, 3.0, 3.5, 2.5, 3.5, 3.5, 3.0, 3.0, 3.0, 1.0, 1.0, 2.0, 2.0, 4.0, 5.0, 3.5, 3.0, 2.0, 2.5, 3.5, 3.0, 3.0, 0.5, 0.75, 1.5, 1.0, 2.0, 2.5, 3.5, 1.5, 3.5, 3.5, 2.5, 2.5, 2.0, 2.5, 5.0, 2.5])
  ##How much DNA should be added for each sample (µL)
# =============================================================================


# CALCULATED VARIABLES=========================================================
# =============================================================================
if PCR_tubes == 'PCR_strips':
    PCR_racks = math.ceil((number_of_samples + number_of_NTCs)/32)
  ## How many PCR tube racks / plate are needed
sample_racks = math.ceil((number_of_samples + 1) / 24)
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
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    
    #pipette tips
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        7,                                  #deck position
        '20tips_1')                         #custom name       
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                 #deck position
        '20tips_2')                         #custom name

    # Tube_racks & plates
    sample_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        4,                                                       #deck position
        'sample_tubes_1')                                        #custom name
    if sample_racks >= 2:
        sample_tubes_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            1,                                                       #deck pos
            'sample_tubes_2')                                        #cust name
    if sample_racks >= 3:
        sample_tubes_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            3,                                                       #deck pos
            'sample_tubes_3')                                        #cust name
    if sample_racks >= 4:
        sample_tubes_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            11,                                                      #deck pos
            'sample_tubes_4')                                        #cust name
    
    if PCR_tubes == 'PCR_strips':
   ### !!! OPTION 1: ROBOT         
        PCR_1 = protocol.load_labware(
         'pcrstrips_96_wellplate_200ul',    #labware definition
         8,                                 #deck position
         'PCR_tube_1')                       #custom name
        if PCR_racks >= 2:
           PCR_2 = protocol.load_labware(
                 'pcrstrips_96_wellplate_200ul',    #labware definition
                 9,                                 #deck position
                 'PCR_tube_2')                       #custom name
    
    ##### !!! OPTION 2: SIMULATOR         
        # with open("labware/pcrstrips_96_wellplate_200ul/"
        #            "pcrstrips_96_wellplate_200ul.json") as labware_file:
        #          labware_def_pcrstrips = json.load(labware_file)
        # PCR_1 = protocol.load_labware_from_definition( 
        #      labware_def_pcrstrips, #variable derived from opening json
        #      8,                     #deck position
        #      'PCR_tube_1')          #custom name
        # if PCR_racks >= 2:
        #     with open("labware/pcrstrips_96_wellplate_200ul/"
        #                "pcrstrips_96_wellplate_200ul.json") as labware_file:
        #              labware_def_pcrstrips = json.load(labware_file)
        #     PCR_2 = protocol.load_labware_from_definition( 
        #          labware_def_pcrstrips, #variable derived from opening json
        #          9,                     #deck position
        #          'PCR_tube_2')          #custom name
    
    if PCR_tubes == 'plate_96':
        #### !!! OPTION 1: ROBOT 
        PCR_1 = protocol.load_labware(
            'biorad_qpcr_plate_eppendorf_cool_rack',#labware definition
            8,                                      #deck position
            '96well_plate_rack')                    #custom name  
       ##### !!! OPTION 2: SIMULATOR
        # with open("labware/biorad_qpcr_plate_eppendorf_cool_rack/"
        #             "biorad_qpcr_plate_eppendorf_cool_rack.json") as labware_file:
        #           labware_def_cool_rack = json.load(labware_file)
        # PCR_1 = protocol.load_labware_from_definition( 
        #     labware_def_cool_rack,   #variable derived from opening json
        #     8,                       #deck position
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
        
        water_vol = 5 - sample_vol
          ## volume of water needed to add a total of 5µL
        if water_vol > 0:
            p20.pick_up_tip()
            p20.aspirate(water_vol, water_tube)
            p20.dispense(water_vol, well)
            sample_mix_vol = sample_vol + 3
              ## primer_mix_vol = volume for pipetting up and down              ##
            p20.mix(3, sample_mix_vol, well)
            p20.dispense(10, well)
            p20.drop_tip()
        
    ## Add water to NTC
    water_vol = 5
    well = sample_destinations[-1]
    p20.pick_up_tip()
    p20.aspirate(water_vol, water_tube)
    p20.dispense(water_vol, well)
    sample_mix_vol = sample_vol + 3
      ## primer_mix_vol = volume for pipetting up and down              ##
    p20.mix(3, sample_mix_vol, well)
    p20.dispense(10, well)
    p20.drop_tip()

            
# =============================================================================
    