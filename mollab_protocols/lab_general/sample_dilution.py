# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 210707
# Description: sample dilution protocol
# =============================================================================

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

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'sample_dilution.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('Sample dilution protocol'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Sample dilution protocol. 
    First aliquot water for diluting samples into a 96_wells plate.
    The source = 5mL tubes. Use volume tracking, which resets after every
    tube. 
    Provide samples in tube_strips
    Dilutions will be made in 96wells_plates
    """
# =============================================================================


# VARIABLES TO SET#!!!=========================================================
# =============================================================================
    number_of_samples = 143  # Maximum 192 samples
      ## How many samples do you want to dilute? 
    sample_volume = 1.5
      ## How much sample (µL) to use for the dilution?
    dilution_ratio = 100
      ## How many times to dilute?
    starting_tip_p200 = 'D8'
    starting_tip_p20 = 'C12'
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
    dilution_volume = sample_volume * dilution_ratio
      ## How much volume you will end up with
    water_volume = dilution_volume - sample_volume
      ## How much water is needed for per sample
    water_tubes = math.ceil((water_volume * number_of_samples)/5000) + 1
      ## How many tubes of 5mL water are needed (+1 to be save)
    sample_racks = math.ceil(number_of_samples / 48)
      ## How many tube_strip_racks are needed (1,2,3 or 4)
    dilution_plates = math.ceil(number_of_samples / 96)
      ## How many dilution_plates are needed (1 or 2)
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading labware
    tips_200 = protocol.load_labware(
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
    if number_of_samples > 96:
        tips_20_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  #labware definition
            8,                                  #deck position
            'tips_20_3')                        #custom name    
   
    plate_96_dil = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        #labware definition
        4,                                      #deck position
        'plate_96_dil')                         #custom name
    if dilution_plates == 2:
        plate_96_dil_2 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        #labware definition
        5,                                      #deck position
        'plate_96_dil_2')                        #custom name

    ##### !!! FOR ROBOT      
    # sample_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',         #labware definition
    #     1,                                      #deck position
    #     'sample_strips_1')                      #custom name
    # if sample_racks >= 2: 
    #     sample_strips_2 = protocol.load_labware(
    #         'pcrstrips_96_wellplate_200ul',     #labware definition
    #         2,                                  #deck position
    #         'sample_strips_2')                  #custom name
    # if sample_racks >= 3: 
    #     sample_strips_3 = protocol.load_labware(
    #         'pcrstrips_96_wellplate_200ul',     #labware definition
    #         3,                                  #deck position
    #         'sample_strips_3')                  #custom name
    # if sample_racks >= 4: 
    #     sample_strips_4 = protocol.load_labware(
    #         'pcrstrips_96_wellplate_200ul',     #labware definition
    #         6,                                  #deck position
    #         'sample_strips_4')                  #custom name    
    
    # tubes_5mL = protocol.load_labware(
    #     'eppendorfscrewcap_15_tuberack_5000ul', #labware definition
    #     9,                                      #deck position
    #     'tubes_5mL')                            #custom name    
    
    # ####    !!! FOR SIMULATOR
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
            sample_strips_1 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            1, 
            'sample_strips_1')
            if sample_racks >= 2:
                sample_strips_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, #variable derived from opening json
                    2, 
                    'sample_strips_2')
            if sample_racks >= 3:
                sample_strips_3 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                3, 
                'sample_strips_3')
            if sample_racks >= 4:
                sample_strips_4 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                6, 
                'sample_strips_4')
            
    with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
              "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
            labware_def_5mL = json.load(labware_file)
            tubes_5mL = protocol.load_labware_from_definition( 
            labware_def_5mL, #variable derived from opening json
            9, 
            '5mL_tubes')      

    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                             #instrument definition
        'right',                                        #mount position
        tip_racks=[tips_200])                           #assigned tiprack
    p20 = protocol.load_instrument(
        'p20_single_gen2',                              #instrument definition
        'left',                                         #mount position
        tip_racks=[tips_20_1, tips_20_2, tips_20_3])    #assigned tiprack
# =============================================================================


# SETTING LOCATIONS#!!!============================================================
# =============================================================================
    ##### Setting starting tip
    p300.starting_tip = tips_200.well(starting_tip_p200)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
      ## The starting_tip is the location of first pipette tip in the box   ##
      
    ##### Setting tube locations
    H2O = []
    for row in (
            [tubes_5mL.rows_by_name()[row_name] for row_name in ['B','C']]):
        for well in row:
            H2O.append(well)
    
    sample_wells = []
    columns_odd = ['1','3','5','7','9','11']
    sample_columns = (                                                           
        ([sample_strips_1.columns_by_name()[column_name] 
          for column_name in columns_odd])) 
    if sample_racks >= 2:
        sample_columns_2 = ( 
            ([sample_strips_2.columns_by_name()[column_name] 
              for column_name in columns_odd]))
        for column in sample_columns_2:
            sample_columns.append(column)
    if sample_racks >= 3:
        sample_columns_3 = ( 
            ([sample_strips_3.columns_by_name()[column_name] 
              for column_name in columns_odd]))
        for column in sample_columns_3:
            sample_columns.append(column)
    if sample_racks >= 4:
        sample_columns_4 = ( 
            ([sample_strips_4.columns_by_name()[column_name] 
              for column_name in columns_odd]))
        for column in sample_columns_4:
            sample_columns.append(column)
    
    for column in sample_columns:
        for well in column:
            sample_wells.append(well)
      ## makes a list of all wells in 1,2,3 or 4 full plates of PCR strips  ##
    sample_wells = sample_wells[:number_of_samples]
      ## cuts off the list after certain number of samples                  ##
      
    dilution_wells = []
    for well in plate_96_dil.wells():
        dilution_wells.append(well)
    if dilution_plates == 2:
        for well in plate_96_dil_2.wells():
            dilution_wells.append(well)
      ## Makes a lost of all wrells in 1 or 2 96wells plates
    dilution_wells = dilution_wells[:number_of_samples]
      ## cuts off the list after a certain number of samples                ##
# =============================================================================

# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.pause("I need "+ str(water_tubes) + " tubes with 5mL of water."
                   " Put them in rows B and C of the tube rack please.")
# =============================================================================

# ALIQUOTING WATER=============================================================    
# =============================================================================
    ##### Variables for volume tracking and aliquoting
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
            p300.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    ##
        elif i % 16 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
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

        #### The actual aliquoting of mastermix
        p300.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the       ##
          ## location specified in aspiration_location.                     ##
        p300.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the         ##
          ## location specified in well (looping through plate)             ##
        p300.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill       ##
          ## completely when using a disposal volume by dispensing some     ##
          ## of the volume after each pipetting step. (blow-out too many    ##
          ## bubbles)                                                       ##
    p300.drop_tip()
      ## when entire plate is full, drop tip                                ##
# =============================================================================

# DILUTING SAMPLES=============================================================
# =============================================================================
    for sample_well, dilution_well in zip(sample_wells, dilution_wells):
        ## Combine each sample with a dilution_well and a destination well  ##
        p20.pick_up_tip()
          ## p20 picks up tip from location of specified starting_tip       ##
          ## or following                                                   ##
        p20.aspirate(sample_volume, sample_well)
          ## aspirate sample_volume_dil = volume for dilution from sample   ##
        p20.dispense(sample_volume, dilution_well)
          ## dispense sample_volume_dil = volume for dilution into dil_well ##
        p20.mix(3, sample_volume + 3, dilution_well)
          ## pipette up&down 3x to get everything from the tip              ##
        p20.dispense(20, dilution_well)
          ## instead of blow-out
        p20.drop_tip()
          ## Drop tip in trashbin on 12.                                    ##
         
# =============================================================================

