# =============================================================================
# Protocol for digestion or ligation on EVE
# 
# Description: 
#   - Sample is already in the strips/plate
#   - EVE will add mastermix to samples in PCR strips or a plate (max 96)
#   - mix in 'tube_1.5mL' or 'tube_5mL'
#   - mix by pipetting
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

#### !!! OPTION 1: ROBOT
from data.user_storage.mollab_modules import volume_tracking_v1 as vt
##### !!! OPTION 2: SIMULATOR
# from mollab_modules import volume_tracking_v1 as vt
# =============================================================================


# VARIABLES TO SET#!!!=========================================================
# =============================================================================
number_of_samples = 96   # max 96 including controls
  ## How many samples do you want to include?                               ##
sample_tubes = 'PCR_strips'
  ## What kind of tubes are the samples in?                                 ##
  ## Options: 'PCR_strips' or 'plate_96'                                    ##
if sample_tubes == 'PCR_strips':
    strip_positions = ['2', '5', '8','11']     
     ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                  ##
     ## max 3 racks with strips!                                            ##
     
MM_start_vol = 148.32
  ## The MM_start_vol is the volume (ul) of mastermix that is in the source ##
  ## labware at the start of the protocol.                                  ##
MM_dispension_vol = 1.475
  ## The volume (ul) of mastermix that is aliquoted                         ##
MM_tube = 'tube_1.5mL'
  ## In what kind of tube is your mastermix?                                ##
  ## Options: 'tube_1.5mL' or 'tube_5mL'                                    ##
MM_well = 'D1'  
  ## Where is the mastermix tube located in the rack                        ##

starting_tip = 'A1'
  ## The starting_tip is the location of first pipette tip in the box       ##
  ## Either for p20 tips (with MM_dispension_vol =< 17µL)                   ##
  ## Or for p200 tips (with MM_dispension_vol > 17µL)                       ##
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
if sample_tubes == 'PCR_strips':
    if strip_positions == ['2', '5', '8','11']:
        sample_tubes_per_rack = 32
    elif strip_positions == ['2', '7','11']:
        sample_tubes_per_rack = 24    
    sample_racks = math.ceil(number_of_samples / sample_tubes_per_rack)
mix_vol = MM_dispension_vol + 3
# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'digestion_ligation',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('aliquoting mix to samples and mixing'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix from a 1.5 or 5 mL tube to a 96 wells plate or 
    tube strips that already contain sample.
    Mix by pipetting up and down.
    """
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================

    # pipette tips
    if MM_dispension_vol > 17:
        tips_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',     #labware definition
        7,                                      #deck position
        '200tips_1')                            #custom name
        tips_2 = protocol.load_labware(
         'opentrons_96_filtertiprack_200ul',    #labware definition
        11,                                     #deck position
        '200tips_2')                            #custom name
    
    else:
        tips_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  #labware definition
            7,                                  #deck position
            '20tips_1')                         #custom name
        tips_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  #labware definition
            11,                                 #deck position
            '20tips_2')                         #custom name
    
    # tube racks
    if sample_tubes == 'plate_96':
        samples_1 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        #labware definition
        4,                                      #deck position
        'samples_plate')                        #custom name
    
    if sample_tubes == 'PCR_strips':
    ##### !!! OPTION 1: ROBOT         
        samples_1 = protocol.load_labware(
        'pcrstrips_96_wellplate_200ul',         #labware definition
        4,                                      #deck position
        'sample_strips_1')                      #custom name
        if sample_racks >= 2:
            samples_2 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul', #labware definition
                5,                              #deck position
                'sample_strips_2')              #custom name
        if sample_racks >= 3:
            samples_3 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul', #labware definition
                6,                              #deck position
                'sample_strips_3')              #custom name
    ##### !!! OPTION 2: SIMULATOR         
        # with open("labware/pcrstrips_96_wellplate_200ul/"
        #           "pcrstrips_96_wellplate_200ul.json") as labware_file:
        #         labware_def_pcrstrips = json.load(labware_file)
        # samples_1 = protocol.load_labware_from_definition( 
        #     labware_def_pcrstrips,              #variable derived from json
        #     4,                                  #deck position
        #     'sample_strips_1')                  #custom name
        # if sample_racks >= 2:
        #     samples_2 = protocol.load_labware_from_definition( 
        #         labware_def_pcrstrips,          #variable derived from json
        #         5,                              #deck position
        #         'sample_strips_2')              #custom name           
        # if sample_racks >= 3:
        #     samples_3 = protocol.load_labware_from_definition( 
        #         labware_def_pcrstrips,          #variable derived from json
        #         6,                              #deck position
        #         'sample_strips_3')              #custom name
    
    if MM_tube == 'tube_1.5mL':
        MM = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', #labw def
            8,                                                        #deck pos
            'MM_1.5mL')                                               #custname
    if MM_tube == 'tube_5mL':
    ##### !!! OPTION 1: ROBOT
        MM = protocol.load_labware(
            'eppendorfscrewcap_15_tuberack_5000ul',     #labware def
            8,                                          #deck position
            'mastermix_tube')                           #custom name 
   ##### !!! OPTION 2: SIMULATOR      
        # with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
        #             "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
        #           labware_def_5mL = json.load(labware_file)
        # MM = protocol.load_labware_from_definition( 
        #     labware_def_5mL,                    #variable derived from json
        #     8,                                  #deck position
        #     'mastermix_tube')                   #custom name

    # Pipettes
    if MM_dispension_vol > 17:
        pipette = protocol.load_instrument(
            'p300_single_gen2',                 #instrument definition
            'right',                            #mount position
            tip_racks=[tips_1, tips_2])         #assigned tiprack
    else:
        pipette = protocol.load_instrument(
            'p20_single_gen2',                  #instrument definition
            'left',                             #mount position
            tip_racks=[tips_1, tips_2])         #assigned tiprack         
# =============================================================================


# SETTING LOCATIONS============================================================
# =============================================================================
    ##### Setting starting tip                                              ##
    pipette.starting_tip = tips_1.well(starting_tip)
    ## The starting_tip is the location of first pipettetip in the first box##
    
    ##### Tube locations                                                    ##
    MasterMix = MM[MM_well]
      ## Location of the tube with mastermix                                ##
    
    destination_wells = []
      ## Where should mastermix go                                          ##
    if sample_tubes == 'plate_96':
        destination_wells = samples_1.wells()
    
    elif sample_tubes == 'PCR_strips':
        sample_columns = (
            ([samples_1.columns_by_name()[column_name]
            for column_name in strip_positions]))
        if sample_racks >= 2:
            sample_columns_2 = (
            ([samples_2.columns_by_name()[column_name]
              for column_name in strip_positions]))
            sample_columns = sample_columns + sample_columns_2
        if sample_racks >= 3:
            sample_columns_3 = (
            ([samples_3.columns_by_name()[column_name]
              for column_name in strip_positions]))
            sample_columns = sample_columns + sample_columns_3
        for column in sample_columns:
            for well in column:
                destination_wells.append(well)
    
    destination_wells = destination_wells[:number_of_samples]
      ## cuts off the list after a certain number of wells                  ##
# =============================================================================


# VARIABLES FOR VOLUME TRACKING================================================
# =============================================================================
    start_height = vt.cal_start_height(MM_tube, MM_start_vol)
      ## Call start height calculation function from volume tracking module.##
    if MM_start_vol < 500:
          start_height = start_height - 6
      ## start_height is not so good for small amounts
    current_height = start_height
      ## Set the current height to start height at the beginning of the     ##
      ## protocol.                                                          ##

# =============================================================================


## ALIQUOTING MASTERMIX========================================================
## ============================================================================
    for i, well in enumerate(destination_wells):
      ## For each destination_well do the following:                        ##
      
        ##### volume tracking                                               ##
        current_height, pip_height, bottom_reached = vt.volume_tracking(
          MM_tube, MM_dispension_vol, current_height)
            ## call volume_tracking function, obtain current_height,        ##
            ## pip_height and whether bottom_reached.                       ##
        
        
        
        # What to do if bottom_reached                                      ##
        if bottom_reached:
            aspiration_location = MasterMix.bottom()
            protocol.comment("You've reached the bottom of the tube!")
              ## If bottom is reached keep pipetting from bottom            ##
        else:
            aspiration_location = MasterMix.bottom(pip_height)
              ## Set the location of where to aspirate from.                ##
        
        ##### The actual aliquoting of mastermix                            ##
        pipette.pick_up_tip()
          ## Pick up a new tip for every sample
        pipette.aspirate(MM_dispension_vol, aspiration_location)
          ## Aspirate the specified volume, from the specified location     ##
        pipette.dispense(MM_dispension_vol, well)
          ## Dispense the specified volume to the location specified in     ##
          ## well (so a new well every time the loop restarts)              ##
        pipette.mix(3, mix_vol, well)
          ## Mix by pipetting up and down 3x with the specified volume + 3  ##
        pipette.dispense(10,well)
          ## Alternative for blow_out                                       ##
        pipette.drop_tip()
          ## Drop tip in trash                                              ##
# =============================================================================