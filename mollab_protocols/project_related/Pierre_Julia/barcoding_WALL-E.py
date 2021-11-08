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
  ## Import json to import custom labware with labware_from_definition,      ##
  ## so that we can use the simulate_protocol with custom labware.           ##

#### !!! OPTION 1: ROBOT
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
##### !!! OPTION 2: SIMULATOR
from mollab_modules import volume_tracking_v1 as vt
# =============================================================================

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
#### Samples
number_of_samples = 96 # max 96  
  ## How many samples do you want to include? Including PC and NTC           ##
#### MasterMix
MastermixWater_tube = 'tube_1.5mL'
  ## What kind of tube will the mastermix be in?                             ##
  ## Options: 'tube_1.5mL' or 'tube_5mL'
mastermix_source = 'D1'
  ## Where is the mastermix tube located in the rack                         ##
MM_start_vol = 2080
  ## The start_vol is the volume (µl) of mastermix that is in the tube       ##
MM_dispension_vol = 20 
  ## Volume of MasterMix to be aliquoted                                     ##

#### Water
water_source = 'D2'
w_start_vol = 1200
  ## The start_vol is the volume (µl) of water that is in the tube           ##
water_µL_list = ([2.5, 3.75, 3.25, 3.25, 5.0, 4.0, 3.75, 2.25,
                2.25, 4.0, 2.25, 5.0, 4.0, 2.5, 3.25, 3.0,
                1.75, 3.25, 1.75, 2.0, 2.25, 3.0, 3.0, 5.0,
                2.5, 2.75, 4.0, 3.75, 5.0, 2.25, 3.0, 1.5,
                1.5, 2.5, 2.5, 3.25, 3.5, 2.75, 2.5, 2.5,
                2.0, 3.0, 1.5, 1.0, 1.25, 1.75, 1.75, 2.5, 
                2.0, 3.0, 1.5, 1.0, 1.25, 1.75, 1.75, 2.5,
                1.75, 3.25, 1.75, 2.0, 2.25, 3.0, 3.0, 5.0,
                1.5, 2.5, 2.5, 3.25, 3.5, 2.75, 2.5, 2.5,
                2.5, 3.75, 3.25, 3.25, 5.0, 4.0, 3.75, 2.25,
                2.0, 3.0, 1.5, 1.0, 1.25, 1.75, 1.75, 2.5,
                1.75, 3.25, 1.75, 2.0, 2.25, 3.0, 3.0, 5.0,
                ])

#### Barcodes
barcode_tube = 'PCR_strips'
  ## What kind of tubes will the barcodes be in?                             ##
  ## Options: 'PCR_strips', 'plate_96' or 'tube_1.5mL'                       ##
if barcode_tube == 'PCR_strips':
    barcode_loc = ['2', '5', '8','11']
     ## optional: ['2', '7', '11'], ['2','5','8','11'] 
     ## or ['2','3','5','7','9','11']
     ## max 3 racks with strips!    
barcode_vol = 5
  ## Volume of the barcode to be used

PCR_tube = 'PCR_strips'
  ## What kind of tubes will the PCR be in?
  ## Options: 'PCR_strips' or 'plate_96'
if PCR_tube == 'PCR_strips':
    strip_positions = ['2', '5', '8','11']     
     ## optional: ['2', '7', '11'], ['2','5','8','11'] 
     ## or ['2','3','5','7','9','11']
     ## max 3 racks with strips!

#### pipette tips
starting_tip_p20 = 'A1'
starting_tip_p200 = 'A1'
  ## The starting_tip is the location of first pipette tip in the box        ##
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
if barcode_tube == 'PCR_strips':
    if barcode_loc == ['2', '7', '11']:
        tubes_per_rack = 24
    elif barcode_loc == ['2','5','8','11']:
        tubes_per_rack = 32
    elif barcode_loc == ['2','3','5','7','9','11']:
        tubes_per_rack = 48
elif barcode_tube == 'plate_96':
    tubes_per_rack = 96
elif barcode_tube == 'tube_1.5mL':
    tubes_per_rack = 24
barcode_racks = math.ceil(number_of_samples / tubes_per_rack)
  ## How many tube_strip_racks are needed (1,2 or 3)

if PCR_tube == 'PCR_strips':
    if strip_positions == ['2', '7', '11']:
        tubes_per_rack = 24
    elif strip_positions == ['2','5','8','11']:
        tubes_per_rack = 32
    elif strip_positions == ['2','3','5','7','9','11']:
        tubes_per_rack = 48
elif PCR_tube == 'plate_96':
    tubes_per_rack = 96
PCR_racks = math.ceil(number_of_samples / tubes_per_rack)
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
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',  #labware definition
        10,                                  #deck position
        '200tips')                          #custom name  
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        8,                                  #deck position
        '20tips_1')                         #custom name       
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        11,                                 #deck position
        '20tips_2')                         #custom name           
    
    # Tube_racks & plates
    if PCR_tube == 'plate_96':
        PCR_1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    #labware definition
            4,                                  #deck position
            'PCR_plate_96')                         #custom name
    elif PCR_tube == 'PCR_strips':
    #### !!! OPTION 1: ROBOT         
        # PCR_1 = protocol.load_labware(
        #   'pcrstrips_96_wellplate_200ul',    #labware definition
        #   4,                                 #deck position
        #   'PCR_strips_1')                      #custom name
        # if PCR_racks >= 2:
        #     PCR_2 = protocol.load_labware(
        #           'pcrstrips_96_wellplate_200ul',    #labware definition
        #           5,                                 #deck position
        #           'PCR_strips_2')                      #custom name
        # if PCR_racks >= 3:
        #     PCR_3 = protocol.load_labware(
        #           'pcrstrips_96_wellplate_200ul',    #labware definition
        #           6,                                 #deck position
        #           'PCR_strips_3')                      #custom name
    #### !!! OPTION 2: SIMULATOR         
        with open("labware/pcrstrips_96_wellplate_200ul/"
                    "pcrstrips_96_wellplate_200ul.json") as labware_file:
                  labware_def_pcrstrips = json.load(labware_file)
        PCR_1 = protocol.load_labware_from_definition( 
              labware_def_pcrstrips, #variable derived from opening json
              4,                     #deck position
              'PCR_strips_1')        #custom name
        if PCR_racks >= 2:
            PCR_2 = protocol.load_labware_from_definition( 
                  labware_def_pcrstrips, #variable derived from opening json
                  5,                     #deck position
                  'PCR_strips_2')        #custom name
        if PCR_racks >= 3:
            PCR_3 = protocol.load_labware_from_definition( 
                  labware_def_pcrstrips, #variable derived from opening json
                  6,                     #deck position
                  'PCR_strips_3')        #custom name
        
    if MastermixWater_tube == 'tube_1.5mL':
        MastermixWater = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            7,                                                       #deck pos
            'MastermixWater')                                        #cust name 
    elif MastermixWater_tube == 'tube_5mL':
       MastermixWater = protocol.load_labware(
            'eppendorfscrewcap_15_tuberack_5000ul', #labware def
            7,                                     #deck position
            'MastermixWater')                            #custom name 
       ##### !!! OPTION 2: SIMULATOR      
        # with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
        #             "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
        #           labware_def_5mL = json.load(labware_file)
        # MastermixWater = protocol.load_labware_from_definition( 
        #     labware_def_5mL,   #variable derived from opening json
        #     7,                 #deck position
        #     'MastermixWater')  #custom name
    
    if barcode_tube == 'plate_96':
        barcode_1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    #labware definition
            4,                                  #deck position
            'barcode_plate_96')                         #custom name        
    elif barcode_tube == 'PCR_strips':
       ##### !!! OPTION 1: ROBOT      
        # barcode_1 = protocol.load_labware(
        #     'pcrstrips_96_wellplate_200ul',    #labware definition
        #     1,                                 #deck position
        #     'barcode_strips_1')                 #custom name
        # if barcode_racks >=2:
        #     barcode_2 = protocol.load_labware(
        #     'pcrstrips_96_wellplate_200ul',    #labware definition
        #     2,                                 #deck position
        #     'barcode_strips_2')                 #custom name   
        # if barcode_racks >=3:
        #     barcode_3 = protocol.load_labware(
        #     'pcrstrips_96_wellplate_200ul',    #labware definition
        #     3,                                #deck position
        #     'barcode_strips_3')                 #custom name               
       ##### !!! OPTION 2: SIMULATOR      
        with open("labware/pcrstrips_96_wellplate_200ul/"
                  "pcrstrips_96_wellplate_200ul.json") as labware_file:
                labware_def_pcrstrips = json.load(labware_file)
        barcode_1 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            1,                     #deck position
            'barcode_strips_1')    #custom name  
        if barcode_racks >=2:
            barcode_2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                2,                     #deck position
                'barcode_strips_2')    #custom name
        if barcode_racks >=3:
            barcode_3 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                3,                     #deck position
                'barcode_strips_3')    #custom name
    
    elif barcode_tube == 'tube_1.5mL':              
        barcode_1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            1,                                                       #deck pos
            'barcode_rack_1')                                        #cust name
        if barcode_racks >=2:
            barcode_2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#l def
                2,                                                       #d pos
                'barcode_rack_2')                                        #name
        if barcode_racks >=3:
            barcode_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#l def
                3,                                                       #d pos
                'barcode_rack_3')                                        #name            
    
    # Pipettes
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1, tips_20_2])   #assigned tiprack
    p300 = protocol.load_instrument(
        'p300_single_gen2',                  #instrument definition
        'right',                             #mount position
        tip_racks=[tips_200])   #assigned tiprack
# =============================================================================

# PREDIFINED VARIABLES=========================================================
# =============================================================================
    #### MasterMix
    MM_aspiration_vol = MM_dispension_vol + (MM_dispension_vol/100*2)
      ## The aspiration_vol is the volume (ul) that is aspirated from the    ##
      ## container.                                                          ##
    ##### Variables for volume tracking
    MM_start_height = vt.cal_start_height(MastermixWater_tube, MM_start_vol)
      ## Call start height calculation function from volume tracking module. ##
    MM_current_height = MM_start_height
      ## Set the current height to start height at the beginning of the      ##
      ## protocol.                                                           ##
    barcode_mix_vol = barcode_vol + 3
      ## barcode_mix_vol = volume for pipetting up and down                  ##

    #### Water
    ##### Variables for volume tracking
    w_start_height = vt.cal_start_height(MastermixWater_tube, w_start_vol)
      ## Call start height calculation function from volume tracking module. ##
    w_current_height = w_start_height
      ## Set the current height to start height at the beginning of the      ##
      ## protocol.                                                           ##
    
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    ##### Setting starting tip                                               ##
    p300.starting_tip = tips_200.well(starting_tip_p200)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
      ## The starting_tip is the location of first pipette tip in the box    ##
    
    ##### Tube locations                                                     ##
    MasterMix = MastermixWater[mastermix_source]
      ## Location of the tube with mastermix                                 ##
    water = MastermixWater[water_source]
      ## Location of the tube with water                                     ##
      
    #### Where should mastermix go                                           ##
    destination_wells = []
    if PCR_tube == 'plate_96':
        destination_wells = PCR_1.wells()
    elif PCR_tube == 'PCR_strips':
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
        for column in PCR_columns:
            for well in column:
                destination_wells.append(well)
      ## Make a list with all 96 wells of the plate                          ##
    destination_wells =  destination_wells[:number_of_samples]
      ## cuts off the list after a certain number of wells                   ##
      
    #### Where are the barcodes located
    barcode_wells = []
      ## Create an empty list to append wells to                             ##
    barcode_columns = (
        ([barcode_1.columns_by_name()[column_name] 
          for column_name in barcode_loc])) 
    if barcode_racks >= 2:
        barcode_columns2 = (
            ([barcode_2.columns_by_name()[column_name] 
              for column_name in barcode_loc]))
        for column in barcode_columns2:
            barcode_columns.append(column)
    if barcode_racks >= 3:
        barcode_columns3 = (
            ([barcode_3.columns_by_name()[column_name] 
              for column_name in barcode_loc]))
        for column in barcode_columns3:
            barcode_columns.append(column)
        ## Make a list of columns, this is a list of lists!                  ##
    for column in barcode_columns:
        for well in column:
            barcode_wells.append(well)
      ## Separate the columns into wells and append them to list             ##
    barcode_wells = barcode_wells[:number_of_samples]
      ## cuts off the list after a certain number of wells                   ##    
# =============================================================================

## ALIQUOTING MASTERMIX========================================================
## ============================================================================
    for i, well in enumerate(destination_wells):
      ## aliquot mix, for each well do the following:                        ##
        if i == 0: 
            p300.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.     ##
        elif i % 16 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
              ## Then, after every 8th well, drop tip and pick up new        ##
    
        current_height, pip_height, bottom_reached = vt.volume_tracking(
                MastermixWater_tube, MM_dispension_vol, MM_current_height)
                  ## call volume_tracking function, obtain current_height,   ##
                  ## pip_height and whether bottom_reached.                  ##
        
        if bottom_reached:
            aspiration_location = MasterMix.bottom(z=1)
            protocol.comment("You've reached the bottom of the tube!")
              ## If bottom is reached keep pipetting from bottom + 1        ##
        else:
            aspiration_location = MasterMix.bottom(pip_height)
              ## Set the location of where to aspirate from.                ##

        #### The actual aliquoting of mastermix                             ##
        p300.aspirate(MM_aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the       ##
          ## location specified in aspiration_location.                     ##
        p300.dispense(MM_dispension_vol, well)
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

## ADDING BARCODES FOR SAMPLES TO THE MIX=======================================
## ============================================================================
    for barcode_well, destination_well in zip(barcode_wells,destination_wells):
      ## Loop trough barcode_wells and destination_wells                          ##
        p20.pick_up_tip()
        p20.aspirate(barcode_vol, barcode_well)
        p20.dispense(barcode_vol, destination_well)
        p20.mix(3, barcode_mix_vol, destination_well)
        p20.dispense(10, destination_well)
        p20.drop_tip()
# =============================================================================    
    
## ADDING VARIABLE VOLUME OF WATER=============================================
## ============================================================================   
    for water_volume, destination_well in zip(water_µL_list,destination_wells):
      ## Loop through water_volumes and destination_well

        current_height, pip_height, bottom_reached = vt.volume_tracking(
                MastermixWater_tube, water_volume, w_current_height)
                  ## call volume_tracking function, obtain current_height,   ##
                  ## pip_height and whether bottom_reached.                  ##
        if bottom_reached:
            aspiration_location = water.bottom(z=1)
            protocol.comment("You've reached the bottom of the tube!")
              ## If bottom is reached keep pipetting from bottom + 1         ##
        else:
            aspiration_location = water.bottom(pip_height)
              ## Set the location of where to aspirate from.                 ##
    
        p20.pick_up_tip()
        p20.aspirate(water_volume, aspiration_location)
          ## Aspirate the amount specified in water_volume from the location ##
          ## specified in aspiration_location. (so a new volume every time   ##
          ## the loop restarts)                                              ##
        p20.dispense(water_volume, destination_well)
          ## Dispense the amount specified in water_volume to the            ##
          ## location specified in well (so a new well and volume every time ##
          ## the loop restarts)                                              ##
        water_mix_volume = water_volume + 3
        p20.mix(3, water_mix_volume, destination_well)
          ## After dispension, mix 3 times with water_volume +3              ##
        p20.dispense(10, destination_well)
        p20.drop_tip()
# =============================================================================        
