# =============================================================================
# Author(s): Sanne Vreugdenhil
# Creation date: 210713
# Description: 
#   Protocol for aliquoting 1mL of water/Tris/TE from 50mL tubes to 1.5mL 
#   tubes - one 50mL tube per 48 x 1.5mL tubes. 
# =============================================================================


# ==========================IMPORT STATEMENTS==================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##

#### !!! OPTION 1: ROBOT
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
##### !!! OPTION 2: SIMULATOR
from mollab_modules import volume_tracking_v1 as vt
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': 'aliquot_50_to_1.5',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Aliquoting from 50mL tubes to 1.5mL tubes'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Pick up 200µL filter tip. Aspirate 200µL from 50mL tube and transfer
    5x to 1x 1.5mL tube (1mL aliquots) - repeat for 24x 1.5mL tubes.
    Drop tip, pick up new tip and repeat.
    1x 50mL tube for 48x 1.5mL tubes.
    """
# =============================================================================


# =====================LOADING LABWARE AND PIPETTES============================
# =============================================================================
    # Pipette tips
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',                      #labware def
        10,                                                      #deck position
        '200tips')                                               #custom name
    
    # Tube racks
    stock_tubes = protocol.load_labware(
        'opentrons_6_tuberack_falcon_50ml_conical',              #labware def
        7,                                                       #deck position
        '50mL_tubes')                                            #custom name   
    aliquot_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        4,                                                       #deck position
        'aliquot_tubes_1')                                       #custom name
    aliquot_tubes_2 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        1,                                                       #deck position
        'aliquot_tubes_2')                                       #custom name
    aliquot_tubes_3 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        11,                                                       #deck position
        'aliquot_tubes_3')                                       #custom name
    aliquot_tubes_4 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        8,                                                      #deck position
        'aliquot_tubes_4')                                       #custom name
    aliquot_tubes_5 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        5,                                                       #deck position
        'aliquot_tubes_5')                                       #custom name
    aliquot_tubes_6 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        2,                                                       #deck position
        'aliquot_tubes_6')                                       #custom name
    aliquot_tubes_7 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        6,                                                       #deck position
        'aliquot_tubes_7')                                       #custom name
    aliquot_tubes_8 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        3,                                                      #deck position
        'aliquot_tubes_8')                                       #custom name
    
    # Pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                              #instrument definition
        'right',                                         #mount position
        tip_racks=[tips_200])                            #assigned tiprack
# =============================================================================


# ==========================VARIABLES TO SET#!!!===============================
# =============================================================================
    start_vol = 50000 
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##
    dispension_vol = 200 
      ## The dispension_vol is the volume (ul) that needs to be aliquoted   ##
      ## into the destination wells/tubes.                                  ##
    p300.starting_tip = tips_200.well('E6')
      ## The starting_tip is the location of first pipette tip in the box   ##
    container = 'tube_50mL'
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
      ## There are several options to choose from:                          ##
      ## 'tube_1.5ml', 'tube_2mL', 'tube_5mL', 'tube_15mL', 'tube_50mL'   	##
    number_of_source_wells = 3
# source and destination wells=================================================
    source_wells = []
    destination_wells = []
    if number_of_source_wells == 1:     
        source_well_1 = stock_tubes['A1']
        source_wells.append(
            source_well_1)
        destinations = (
            aliquot_tubes_1.wells() + aliquot_tubes_2.wells())
        for well in destinations:
            destination_wells.append(well)
    elif number_of_source_wells == 2:
        source_well_1 = stock_tubes['A1']
        source_well_2 = stock_tubes['A2']
        sources = (source_well_1, source_well_2)
        source_wells.append(sources)
        destinations = (
            aliquot_tubes_1.wells() + aliquot_tubes_2.wells() + 
            aliquot_tubes_3.wells() + aliquot_tubes_4.wells())
        for well in destinations:
            destination_wells.append(well)
    elif number_of_source_wells == 3:
        source_well_1 = stock_tubes['A1']
        source_well_2 = stock_tubes['A2']
        source_well_3 = stock_tubes['B1']
        sources = (source_well_1, source_well_2, source_well_3)
        source_wells.append(sources)
        destinations = (
            aliquot_tubes_1.wells() + aliquot_tubes_2.wells() +
            aliquot_tubes_3.wells() + aliquot_tubes_4.wells() + 
            aliquot_tubes_5.wells() + aliquot_tubes_6.wells())   
        for well in destinations:
            destination_wells.append(well)
    elif number_of_source_wells == 4: 
        source_well_1 = stock_tubes['A1']
        source_well_2 = stock_tubes['A2']
        source_well_3 = stock_tubes['B1']
        source_well_4 = stock_tubes['B2']  
        sources = (source_well_1, source_well_2, source_well_3, source_well_4)
        source_wells.append(sources)
        destinations = (
            aliquot_tubes_1.wells() + aliquot_tubes_2.wells() +
            aliquot_tubes_3.wells() + aliquot_tubes_4.wells() + 
            aliquot_tubes_5.wells() + aliquot_tubes_6.wells() +
            aliquot_tubes_7.wells() + aliquot_tubes_8.wells())   
        for well in destinations:
            destination_wells.append(well)
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
    for i, well in enumerate(destination_wells):
    ## Name all the wells in the plate 'well', for all these do:            ## 
        if i == 0:
            p300.pick_up_tip()
          ## If we are at the first well, start by picking up a tip.        ##
        elif i % 24 == 0:
            p300.drop_tip()
            p300.pick_up_tip() 
          ## Then, after every 8th well, drop tip and pick up a new one.    ##
        current_height, pip_height, bottom_reached = vt.volume_tracking(
            container, dispension_vol, current_height)  
          ## The volume_tracking function needs the arguments container,    ##
          ## dispension_vol, and the current_height which we have set in    ##
          ## this protocol. With those variables, the function updates      ##
          ## the current_height, the pip_height and calculates the          ##
          ## delta_height of the liquid after the next aspiration step.     ##
        if bottom_reached: 
            aspiration_location = source_wells.bottom(z=1) #!!!
            protocol.comment("You've reached the bottom!")
        else:
            aspiration_location = source_wells.bottom(pip_height) #!!!
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
