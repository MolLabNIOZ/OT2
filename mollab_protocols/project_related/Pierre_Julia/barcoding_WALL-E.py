# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 211028
# Description: Barcoding samples for ONT MININON sequencing
#   - aliquot mastermix in a 96 wells plate 
#   - add barcodes from PCR strips to the 96 wells plate
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
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
##### !!! OPTION 2: SIMULATOR
from mollab_modules import volume_tracking_v1 as vt
# =============================================================================

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
number_of_samples = 50 # max 96 - NTC 
  ## How many samples do you want to include?                           ##
number_of_NTCs = 1
  ## How many NTCs to include                                           ##
mastermix_tube = '1.5mL tube'
start_vol = 462.5
  ## The start_vol_m is the volume (ul) of mix that is in the source    ##
  ## labware at the start of the protocol.                              ##
dispension_vol = 9.25 
  ## Volume of MasterMix to be aliquoted                                ##
mastermix_source = 'D1'
  ## Where is the mastermix tube located in the rack                    ##
barcode_loc = ['2', '5', '8','11']
barcode_vol = 5
  ## Volume of the barcode to be used
starting_tip_p20 = 'B4'
  ## The starting_tip is the location of first pipette tip in the box   ##
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
number_of_barcodes = (number_of_samples + number_of_NTCs)
barcode_racks = math.ceil(number_of_barcodes / 32)
  ## How many tube_strip_racks are needed (1,2 or 3)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'barcoding_WALL-E',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('barcoding_WALL-E - aliquoting mix and barcodes '),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix from a 1.5 mL tube to a 96 wells plate;
    Adding barcodes from PCR strips to the 96 wells plate.
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    
    # pipette tips
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                  #deck position
        '20tips_1')                         #custom name       
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        11,                                 #deck position
        '20tips_2')                         #custom name           
    
    # Tube_racks & plates
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        8,                                  #deck position
        'plate_96')                         #custom name     
    
    mastermix_tube = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', #labw def
        7,                                                        #deck pos
        'MasterMix')                                              #cust name 
    
   ##### !!! OPTION 1: ROBOT      
    # barcode_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     4,                                 #deck position
    #     'barcode_strips_1')                 #custom name
    # if barcode_racks >=2:
    #     barcode_strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     5,                                 #deck position
    #     'barcode_strips_2')                 #custom name   
    # if barcode_racks >=3:
    #     barcode_strips_3 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     6,                                #deck position
    #     'barcode_strips_3')                 #custom name               
   ##### !!! OPTION 2: SIMULATOR      
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
    barcode_strips_1 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        4,                     #deck position
        'barcode_strips_1')     #custom name  
    if barcode_racks >=2:
        barcode_strips_2 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            5,                     #deck position
            'barcode_strips_2')     #custom name
    if barcode_racks >=3:
        barcode_strips_3 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            6,                    #deck position
            'barcode_strips_3')     #custom name                            
    
    # Pipettes
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1, tips_20_2])   #assigned tiprack
# =============================================================================

# PREDIFINED VARIABLES=========================================================
# =============================================================================
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
      ## The aspiration_vol is the volume (ul) that is aspirated from the   ##
      ## container.                                                         ##
    ##### Variables for volume tracking
    start_height = vt.cal_start_height('tube_5mL', start_vol)
      ## Call start height calculation function from volume tracking module.##
    current_height = start_height
      ## Set the current height to start height at the beginning of the     ##
      ## protocol.                                                          ##
    barcode_mix_vol = barcode_vol + 3
      ## barcode_mix_vol = volume for pipetting up and down                  ##
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    ##### Setting starting tip                                              ##
    p300.starting_tip = tips_200.well(starting_tip_p200)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
      ## The starting_tip is the location of first pipette tip in the box   ##
    
    ##### Tube locations                                                    ##
    MasterMix = mastermix_tube[mastermix_source]
      ## Location of the 5mL tube with mastermix                            ##
    
    #### Where should mastermix go                                          ##
    number_of_wells = number_of_barcodes
      ##How many wells do need to be filled with mastermix                  ##
    sample_wells = []
    for well in plate_96.wells():
        sample_wells.append(well)
      ## Make a list with all 96 wells of the plate                         ##
    sample_wells = sample_wells[:number_of_wells]
      ## cuts off the list after a certain number of wells                  ##
    standard_wells = [] 
    if number_std_series > 0:
        std_series_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in
         ['12', '11', '10']])
        std_series_columns = std_series_columns[:number_std_series]
        ## reserve a column at the end of the plate for every std_series
        for column in std_series_columns:
            column = column[:length_std_series]
            for well in column:
                standard_wells.append(well)
          ## cut off the columns after a certain std_series length
    MasterMixAliquots = sample_wells + standard_wells
    
    #### Where are the barcodes located
    barcode_wells = []
      ## Create an empty list to append wells to                            ##
    barcode_columns = (
        ([barcode_strips_1.columns_by_name()[column_name] 
          for column_name in barcode_loc])) 
    if barcode_racks >= 2:
        barcode_columns2 = (
            ([barcode_strips_2.columns_by_name()[column_name] 
              for column_name in barcode_loc]))
        for column in barcode_columns2:
            barcode_columns.append(column)
    if barcode_racks >= 3:
        barcode_columns3 = (
            ([barcode_strips_3.columns_by_name()[column_name] 
              for column_name in barcode_loc]))
        for column in barcode_columns3:
            barcode_columns.append(column)
        ## Make a list of columns, this is a list of lists!                 ##
    
    for column in barcode_columns:
        for well in column:
            barcode_wells.append(well)
    barcode_wells = barcode_wells[:number_of_barcodes]
      ## Separate the columns into wells and append them to list            ##
# =============================================================================

## ALIQUOTING MASTERMIX========================================================
## ============================================================================
    for i, well in enumerate(MasterMixAliquots):
      ## aliquot mix, for each well do the following:                       ##
        if i == 0: 
            p300.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    ##
        elif i % 8 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
              ## Then, after every 8th well, drop tip and pick up new       ##
    
        current_height, pip_height, bottom_reached = vt.volume_tracking(
                'tube_5mL', dispension_vol, current_height)
                  ## call volume_tracking function, obtain current_height,  ##
                  ## pip_height and whether bottom_reached.                 ##
        
        if bottom_reached:
            aspiration_location = MasterMix.bottom(z=1)
            protocol.comment("You've reached the bottom of the tube!")
              ## If bottom is reached keep pipetting from bottom + 1        ##
        else:
            aspiration_location = MasterMix.bottom(pip_height)
              ## Set the location of where to aspirate from.                ##

        #### The actual aliquoting of mastermix                             ##
        p300.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the       ##
          ## location specified in aspiration_location.                     ##
        p300.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the         ##
          ## location specified in well (so a new well every time the       ##
          ## loop restarts)                                                 ##
        p300.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill       ##
          ## completely when using a disposal volume by dispensing some     ##
          ## of the volume after each pipetting step. (blow-out to many     ##
          ## bubbles)                                                       ##
    p300.drop_tip()      
# =============================================================================        

## ADDING barcodeS FOR SAMPLES TO THE MIX=======================================
## ============================================================================
    for barcode_well, sample_well in zip(barcode_wells, sample_wells):
      ## Loop trough barcode_wells and sample_wells                          ##
        p20.pick_up_tip()
        p20.aspirate(barcode_vol, barcode_well)
        p20.dispense(barcode_vol, sample_well)
        p20.mix(3, barcode_mix_vol, sample_well)
        p20.dispense(10, sample_well)
        p20.drop_tip()
# =============================================================================    
    
## ADDING barcodeS FOR STD SERIES TO THE MIX====================================
## ============================================================================   
    for well in standard_wells:
        p20.pick_up_tip()
        p20.aspirate(barcode_vol, barcode_wells[-1])
          ## use last barcode pair for NTC and std series
        p20.dispense(barcode_vol, well)
        p20.mix(3, barcode_mix_vol, well)
        p20.dispense(10, well)
        p20.drop_tip()
# =============================================================================        
