# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 211014
# Description: 
#   - aliquot mastermix in PCR strips or plates
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
number_of_samples = 80   # max 96 - number_of_NTCs
  ## How many samples do you want to include?                           ##
number_of_NTCs = 1
  ## How many NTCs to include                                           ##
start_vol = 5000
  ## The start_vol_m is the volume (ul) of mix that is in the source    ##
  ## labware at the start of the protocol.                              ##
dispension_vol = 42 
  ## Volume of MasterMix to be aliquoted                                ##
mastermix_source = 'C1'
  ## Where is the mastermix tube located in the rack                    ##
  ## Mastermix should be provided in a 5mL tube
PCR_tubes = 'PCR_strips'
  ## What kind of tubes will the PCR be in?
  ## Options: 'PCR_strips' or 'plate_96'
if PCR_tubes == 'PCR_strips':
    strip_positions = ['2', '5', '8','11']     
     ## optional: ['2', '7', '11'] or ['2', '5', '8','11']
     ## max 4 racks with strips!
starting_tip_p200 = 'A2'
  ## The starting_tip is the location of first pipette tip in the box   ##
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
if PCR_tubes == 'PCR_strips':
    if strip_positions == ['2', '5', '8','11']:
        PCR_tubes_per_rack = 32
    elif strip_positions == ['2', '7','11']:
        PCR_tubes_per_rack = 24
    PCR_racks = math.ceil(
        (number_of_samples + number_of_NTCs) / PCR_tubes_per_rack)
  ## How many PCR tube racks are needed
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'alliquoting_PCRmix_WALL-E',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('PCR - aliquoting mix'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix from a 5 mL tube to a 96 wells plate or tube strips.
    Followed by adding samples.
    """
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    
    # pipette tips
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        10,                                 #deck position
        '200tips')                          #custom name
    
    # Tube_racks & plates
    if PCR_tubes == 'plate_96': 
        PCR_tube = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        8,                                  #deck position
        'plate_96')                         #custom name
    if PCR_tubes == 'PCR_strips':
   ##### !!! OPTION 1: ROBOT         
        # PCR_tube_1 = protocol.load_labware(
        # 'pcrstrips_96_wellplate_200ul',    #labware definition
        # 8,                                 #deck position
        # 'PCR_tube_1')                      #custom name
        # if PCR_racks >= 2:
        #     PCR_tube_2 = protocol.load_labware(
        #         'pcrstrips_96_wellplate_200ul',    #labware definition
        #         5,                                 #deck position
        #         'PCR_tube_2')                      #custom name
        # if PCR_racks >= 3:
        #     PCR_tube_3 = protocol.load_labware(
        #         'pcrstrips_96_wellplate_200ul',    #labware definition
        #         2,                                 #deck position
        #         'PCR_tube_3')                      #custom name
        # if PCR_racks == 4:
        #     PCR_tube_4 = protocol.load_labware(
        #         'pcrstrips_96_wellplate_200ul',    #labware definition
        #         1,                                 #deck position
        #         'PCR_tube_4')                      #custom name

    ##### !!! OPTION 2: SIMULATOR         
        with open("labware/pcrstrips_96_wellplate_200ul/"
                  "pcrstrips_96_wellplate_200ul.json") as labware_file:
                labware_def_pcrstrips = json.load(labware_file)
        PCR_tube_1 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            8,                     #deck position
            'PCR_tube_1')          #custom name
        if PCR_racks >= 2:
            PCR_tube_2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                5,                     #deck position
                'PCR_tube_2')          #custom name           
        if PCR_racks >= 3:
            PCR_tube_3 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                2,                     #deck position
                'PCR_tube_3')          #custom name      
        if PCR_racks >= 4:
            PCR_tube_4 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, #variable derived from opening json
                1,                     #deck position
                'PCR_tube_4')          #custom name      
    
    
    ##### !!! OPTION 1: ROBOT
    # mastermix_tube = protocol.load_labware(
    #     'eppendorfscrewcap_15_tuberack_5000ul', #labware def
    #     4,                                      #deck position
    #     'mastermix_tube')                       #custom name 
   ##### !!! OPTION 2: SIMULATOR      
    with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
              labware_def_5mL = json.load(labware_file)
    mastermix_tube = protocol.load_labware_from_definition( 
        labware_def_5mL,   #variable derived from opening json
        4,                 #deck position
        'mastermix_tube')  #custom name 


    # Pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack
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
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    ##### Setting starting tip                                              ##
    p300.starting_tip = tips_200.well(starting_tip_p200)
      ## The starting_tip is the location of first pipette tip in the box   ##
    
    ##### Tube locations                                                    ##
    MasterMix = mastermix_tube[mastermix_source]
      ## Location of the 5mL tube with mastermix                            ##
    
    #### Where should mastermix go                                          ##
    number_of_wells = number_of_samples + number_of_NTCs
      ##How many wells do need to be filled with mastermix                  ##
    MasterMixAliquots = []
    if PCR_tubes == 'plate_96':
        MasterMixAliquots = PCR_tube.wells()

    elif PCR_tubes == 'PCR_strips':
        PCR_columns = (
            ([PCR_tube_1.columns_by_name()[column_name]
            for column_name in strip_positions]))
        if PCR_racks >= 2:
            PCR_columns_2 = (
            ([PCR_tube_2.columns_by_name()[column_name]
              for column_name in strip_positions]))
            PCR_columns = PCR_columns + PCR_columns_2
        if PCR_racks >= 3:
            PCR_columns_3 = (
            ([PCR_tube_3.columns_by_name()[column_name]
              for column_name in strip_positions]))
            PCR_columns = PCR_columns + PCR_columns_3
        if PCR_racks >= 4:
            PCR_columns_4 = (
            ([PCR_tube_4.columns_by_name()[column_name]
              for column_name in strip_positions]))
            PCR_columns = PCR_columns + PCR_columns_4
        for column in PCR_columns:
            for well in column:
                MasterMixAliquots.append(well)
            
      ## Make a list with all wells for PCR                         ##
    MasterMixAliquots = MasterMixAliquots[:number_of_wells]
      ## cuts off the list after a certain number of wells                  ##
# =============================================================================

## ALIQUOTING MASTERMIX========================================================
## ============================================================================
    for i, well in enumerate(MasterMixAliquots):
      ## aliquot mix, for each well do the following:                       ##
        if i == 0: 
            p300.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    ##
        elif i % 16 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
              ## Then, after every 16th well, drop tip and pick up new       ##
    
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

