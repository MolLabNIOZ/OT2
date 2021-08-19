# =============================================================================
# Author(s): Sanne Vreugdenhil
# Creation date: 210819
# Description: 
#   Testing whether the 300uL pipette tips from TipOne work well with the 
#   300uL pipette.
#   -> pipette 30uL of water from a 5mL tube to 12 PCR strips, using a
#      a new tip every time so that we can check if there are no big
#      differences in volume between pipettip locations 
#      due to bending of the rack
# =============================================================================


# ==========================IMPORT STATEMENTS==================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
  
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##

#### !!! OPTION 1: ROBOT
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
##### !!! OPTION 2: SIMULATOR
from mollab_modules import volume_tracking_v1 as vt
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': 'tip_one_300_test',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Testing TipOne 300uL tips'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Pipette 30uL of water from a 5mL tube to 12 PCR strips.
    Using a new tip for every step so that we can check if there is no big
    difference between volumes from different pipette tip locations.
    """
# =============================================================================


# ======================LOADING LABWARE AND PIPETTES===========================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    # Pipette tips
   ##### !!! OPTION 1: ROBOT        
    # tip_one_300 = protocol.load_labware(
    #     'tipone_96_tiprack_300ul',          #labware definition
    #     1,                                  #deck position
    #     '300tips')                          #custom name     
   ##### !!! OPTION 2: SIMULATOR      
    with open("labware/tipone_96_tiprack_300ul/"
                "tipone_96_tiprack_300ul.json") as labware_file:
              labware_def_tips = json.load(labware_file)
    tip_one_300 = protocol.load_labware_from_definition( 
        labware_def_tips,   #variable derived from opening json
        1,                  #deck position
        '300tips')          #custom name 
    
    # Tube_racks & plates  
   ##### !!! OPTION 1: ROBOT      
    # source_tube = protocol.load_labware(
    #     'eppendorfscrewcap_15_tuberack_5000ul',   #labware def
    #     2,                                        #deck position
    #     'source_tube')                            #custom name          
    # strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',           #labware definition
    #     7,                                        #deck position
    #     'strips_1')                               #custom name
    # strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',          #labware definition
    #     4,                                       #deck position
    #     'strips_2')                              #custom name  
    # strips_3 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',          #labware definition
    #     8,                                       #deck position
    #     'strips_3')                              #custom name 
    # strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',          #labware definition
    #     5,                                       #deck position
    #     'strips_4')                              #custom name                 
   ##### !!! OPTION 2: SIMULATOR      
    with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
              labware_def_5mL = json.load(labware_file)
    source_tube = protocol.load_labware_from_definition( 
        labware_def_5mL,          #variable derived from opening json
        2,                        #deck position
        'source_tube')            #custom name 
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
    strips_1 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips,    #variable derived from opening json
        7,                        #deck position
        'strips_1')               #custom name  
    strips_2 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips,    #variable derived from opening json
        4,                        #deck position
        'strips_2')               #custom name          
    strips_3 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips,    #variable derived from opening json
        8,                        #deck position
        'strips_3')               #custom name  
    strips_4 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips,    #variable derived from opening json
        5,                        #deck position
        'strips_4')               #custom name                    
    
    # Pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tip_one_300])               #assigned tiprack
# =============================================================================


# ==========================VARIABLES TO SET#!!!===============================
# =============================================================================
    start_vol = 3000 
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##
    dispension_vol = 30 
      ## The dispension_vol is the volume (ul) that needs to be aliquoted   ##
      ## into the destination wells/tubes.                                  ##
    p300.starting_tip = tip_one_300.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##
    container = 'tube_5mL'
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
      ## There are several options to choose from:                          ##
      ## 'tube_1.5ml', 'tube_2mL', 'tube_5mL', 'tube_15mL', 'tube_50mL'   	##
    source = source_tube['C1']
# Destination wells============================================================
    destinations = []
      ## Create an empty list to append wells to                            ##
    destination_columns = (
        [strips_1.columns_by_name()[column_name] for column_name in
         ['2', '7', '11']] +
        [strips_2.columns_by_name()[column_name] for column_name in
         ['2', '7', '11']] +
        [strips_3.columns_by_name()[column_name] for column_name in
         ['2', '7', '11']] +
        [strips_4.columns_by_name()[column_name] for column_name in
         ['2', '7', '11']] 
        )
      ## Make a list of columns, this is a list of lists!                   ##
    for column in destination_columns:
        for well in column:
            destinations.append(well)
# =============================================================================


# ==========================PREDIFINED VARIABLES===============================
# =============================================================================
    aspiration_vol = dispension_vol
      ## The aspiration_vol is the volume (ul) that is aspirated from the   ##
      ## container.                                                         ##
    ##### Variables for volume tracking
    start_height = vt.cal_start_height(container, start_vol)
      ## Call start height calculation function from volume tracking module.##
    current_height = start_height
      ## Set the current height to start height at the beginning of the     ##
      ## protocol.                                                          ##
# =============================================================================


# =================================ALIQUOTING==================================
# =============================================================================
    ## For each column in destination_wells, pick up a tip, than for each   ##
    ## well in these columns pipette mix, and after the+ column drop the tip##
    ## Repeat untill all columns in the list are done.                      ##      
    for well in destinations:
    ## Name all the wells in the plate 'well', for all these do:            ## 
        p300.pick_up_tip()
        current_height, pip_height, bottom_reached = vt.volume_tracking(
            container, dispension_vol, current_height)  
          ## The volume_tracking function needs the arguments container,    ##
          ## dispension_vol, and the current_height which we have set in    ##
          ## this protocol. With those variables, the function updates      ##
          ## the current_height, the pip_height and calculates the          ##
          ## delta_height of the liquid after the next aspiration step.     ##
        if bottom_reached: 
            aspiration_location = source.bottom(z=1) #!!!
            protocol.comment("You've reached the bottom!")
        else:
            aspiration_location = source.bottom(pip_height) #!!!
          ## If the level of the liquid in the next run of the loop will    ## 
          ## be smaller than 1 we have reached the bottom of the tube.      ##
          ## To prevent the pipette from crashing into the bottom, we       ##
          ## tell it to go home and pause the protocol so that this can     ##
          ## never happen. Set the location of where to aspirate from.      ##
          ## Because we put this in the loop, the location will change      ##
          ## to the newly calculated height after each pipetting step.      ##
        p300.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the       ##
          ## location specified in aspiration_location.                     ##
        p300.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the         ##
          ## location specified in well (so a new well every time the       ##
          ## loop restarts)                                                 ##
        p300.drop_tip()      
# =============================================================================