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
number_of_samples = 50 # max 96  
  ## How many samples do you want to include? Including PC and NTC           ##

#### MasterMix
mastermix_tube = 'tube_1.5mL'
  ## What kind of tube will the mastermix be in?                             ##
  ## Options: 'tube_1.5mL' or 'tube_5mL'
mastermix_source = 'D1'
  ## Where is the mastermix tube located in the rack                         ##
MM_start_vol = 1040
  ## The start_vol is the volume (µl) of mastermix that is in the tube       ##
MM_dispension_vol = 20 
  ## Volume of MasterMix to be aliquoted                                     ##

#### Water
water_tube = mastermix_tube
water_source = 'D2'
w_start_vol = 1200
  ## The start_vol is the volume (µl) of water that is in the tube           ##

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
        18,                                  #deck position
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
                  'PCR_strips_2')        #custom name
        
    if mastermix_tube == 'tube_1.5mL':
        mastermix = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            7,                                                       #deck pos
            'MasterMix')                                             #cust name 
    elif mastermix_tube == 'tube_5mL':
        mastermix = protocol.load_labware(
            'eppendorfscrewcap_15_tuberack_5000ul', #labware def
            7,                                     #deck position
            'tubes_5mL')                            #custom name 
       ##### !!! OPTION 2: SIMULATOR      
        # with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
        #             "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
        #           labware_def_5mL = json.load(labware_file)
        # mastermix = protocol.load_labware_from_definition( 
        #     labware_def_5mL,   #variable derived from opening json
        #     7,                 #deck position
        #     'tubes_5mL')  #custom name
    
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
# =============================================================================

# PREDIFINED VARIABLES=========================================================
# =============================================================================
    #### MasterMix
    MM_aspiration_vol = MM_dispension_vol + (MM_dispension_vol/100*2)
      ## The aspiration_vol is the volume (ul) that is aspirated from the    ##
      ## container.                                                          ##
    ##### Variables for volume tracking
    MM_start_height = vt.cal_start_height(mastermix_tube, MM_start_vol)
      ## Call start height calculation function from volume tracking module. ##
    MM_current_height = MM_start_height
      ## protocol.                                                           ##
    barcode_mix_vol = barcode_vol + 3
      ## barcode_mix_vol = volume for pipetting up and down                  ##

    #### Water
    ##### Variables for volume tracking
    w_start_height = vt.cal_start_height(water_tube, w_start_vol)
      ## Call start height calculation function from volume tracking module. ##
    w_current_height = w_start_height
      ## Set the current height to start height at the beginning of the      ##
      ## protocol.                                                           ##    
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
