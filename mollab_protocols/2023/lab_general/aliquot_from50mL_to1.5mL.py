# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 210715
# Description: aliquoting from a 50mL tube to 1.5mL tubes, max 144 aliquots
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
from data.user_storage.mollab_modules import volume_tracking_v1 as vt
  # Import volume_tracking module that is on the OT2                        ##
# from mollab_modules import volume_tracking_v1 as vt
#   ## Import volume_tracking module for simulator                          ##
import math
  ## To do some calculations (rounding up)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'aliquoting_from50mL_to1.5mL.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('aliquot from 50mL to 1.5mL protocol'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    aliquoting a specific volume from 50mL tubes to 1.5mL tubes
    Maximum 144 aliquots (6 racks)
    """
# =============================================================================

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
    number_of_tubes = 1 
      ## How many tubes you want to aliquot from? 
    volume = 180      ## How much volume (µL) to aliquot
    starting_tip_p200 = 'C7'
    start_volume = 48000 # How much volume is in each source tube
    # make sure all source tubes have the same volume
    number_of_aliquots = 144 # How many destination tubes you want filled
        # Max 6 racks = 144 tubes
        # If you want to aliquot the entire source:
        # number_of_aliquots = "EmptySourceTubes"
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
    total_volume = start_volume * number_of_tubes
      ## How many µL are available
    if number_of_aliquots == "EmptySourceTubes":
        number_of_aliquots = int(total_volume / volume)
      ## How many aliquots can be made
    number_of_racks = math.ceil(number_of_aliquots / 24)
      ## How many 1.5mL tube racks do you need
    if number_of_racks > 6:
        number_of_aliquots = 144
        number_of_racks = 6
      ## max number of aliquots
    number_of_full_pipettings = math.floor(volume / 200)
      ## How many times you need to pipette with p300 max volume
    rest_volume = volume - (number_of_full_pipettings * 200)
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading labware
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',         #labware definition
        10,                                         #deck position
        'tips_200')                                 #custom name
    tubes_50mL = protocol.load_labware(
        'opentrons_6_tuberack_falcon_50ml_conical', #labware definition
        7,                                          #deck position
        'tubes_50mL')                               #custom name
    tubes_1mL_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',   #labwaredef
        4,                                                          #deck pos
        'tubes_1.5mL1')                                             #cust name
    if number_of_racks > 1:
        tubes_1mL_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            5,                                                       #deck pos
            'tubes_1.5mL2')                                          #cust name
    if number_of_racks > 2:
        tubes_1mL_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            6,                                                       #deck pos
            'tubes_1.5mL3')                                          #cust name    
    if number_of_racks > 3:
        tubes_1mL_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            1,                                                       #deck pos
            'tubes_1.5mL4')                                          #cust name    
    if number_of_racks > 4:
        tubes_1mL_5 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            2,                                                       #deck pos
            'tubes_1.5mL5')                                          #cust name
    if number_of_racks > 5:
        tubes_1mL_6 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            3,                                                       #deck pos
            'tubes_1.5mL6')                                          #cust name

    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                             #instrument definition
        'right',                                        #mount position
        tip_racks=[tips_200])                           #assigned tiprack
# =============================================================================


# SETTING LOCATIONS#!!!========================================================
# =============================================================================    
    ##### Setting starting tip
    p300.starting_tip = tips_200.well(starting_tip_p200)
      ## The starting_tip is the location of first pipette tip in the box   ##
    
    ##### Setting tube locations
    reagent = []
    for well in tubes_50mL.wells():
        reagent.append(well)
    reagent = reagent[:number_of_tubes]
    
    aliquots = []
    for well in tubes_1mL_1.wells():
        aliquots.append(well)
    if number_of_racks > 1:
        for well in tubes_1mL_2.wells():
            aliquots.append(well)
    if number_of_racks > 2:
        for well in tubes_1mL_3.wells():
            aliquots.append(well)
    if number_of_racks > 3:
        for well in tubes_1mL_4.wells():
            aliquots.append(well)
    if number_of_racks > 4:
        for well in tubes_1mL_5.wells():
            aliquots.append(well)
    if number_of_racks > 5:
        for well in tubes_1mL_6.wells():
            aliquots.append(well)
      ## Add all wells of all complete racks to a list
    
    aliquots = aliquots[:number_of_aliquots]
      ## cuts off after calculated number of aliquots    
# =============================================================================


# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.pause("I need "+ str(number_of_racks) + " racks, with a total of "
                   + str(number_of_aliquots) + " 1.5mL tubes.") 
# =============================================================================      

# TURN RAIL LIGHT ON===========================================================
# =============================================================================
    protocol.set_rail_lights(True)   
# =============================================================================  
      

# ALIQUOTING ==================================================================    
# =============================================================================
##### Variables for volume tracking and aliquoting
    counter = 0 # to count how many tubes already emptied
    source = reagent[counter]
    destination = aliquots
    start_height = vt.cal_start_height('tube_50mL', start_volume)
    current_height = start_height
    container = 'tube_50mL'


    ##### Pipette a certain times 200µL
    for i, well in enumerate(destination):
      ## aliquot water in the correct wells, for each well do the following:  
       
        if i == 0: 
            p300.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    ##
        elif i % 24 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
              ## Then, after every 24th well, drop tip and pick up new      ##
        
        for i in range(number_of_full_pipettings): 
          ## Pipette 200µL for predefined number of times
            current_height, pip_height, bottom_reached = vt.volume_tracking(
                container, 200, current_height)
              ## call volume_tracking function, obtain current_height,      ##
              ## pip_height and whether bottom_reached.                     ##
        
            if bottom_reached:
                ## continue with next tube, reset vt                        ##
                current_height = start_height
                current_height, pip_height, bottom_reached = (
                    vt.volume_tracking(
                        container, 200, current_height))
                counter = counter + 1
                source = reagent[counter]
                aspiration_location = source.bottom(current_height)
                protocol.comment(
                "Continue with tube " + str(counter + 1) + " of water")
       
            else:
                aspiration_location = source.bottom(pip_height)
                  ## Set the location of where to aspirate from.            ##

            #### The actual aliquoting
            p300.aspirate(200, aspiration_location)
              ## Aspirate the amount specified in aspiration_vol from the   ##
              ## location specified in aspiration_location.                 ##
            p300.dispense(200, well.top(z = - 10))
              ## Dispense the amount specified in dispension_vol to the     ##
              ## location specified in well (looping through plate)         ##
            p300.dispense(10, aspiration_location)
              ## Alternative for blow-out, make sure the tip doesn't fill   ##
              ## completely when using a disposal volume by dispensing some ##
              ## of the volume after each pipetting step. (blow-out too many##
              ## bubbles)                                                   ##
        
        ##### Pipette rest volume
        if rest_volume > 0:
            current_height, pip_height, bottom_reached = vt.volume_tracking(
                    container, rest_volume, current_height)
                  ## call volume_tracking function, obtain current_height,  ##
                  ## pip_height and whether bottom_reached.                 ##
            
            if bottom_reached:
                ## continue with next tube, reset vt                        ##
                current_height = start_height
                current_height, pip_height, bottom_reached = (
                    vt.volume_tracking(
                        container, rest_volume, current_height))
                counter = counter + 1
                source = reagent[counter]
                aspiration_location = source.bottom(current_height)
                protocol.comment(
                "Continue with tube " + str(counter) + " of water")
       
            else:
                aspiration_location = source.bottom(pip_height)
                  ## Set the location of where to aspirate from.            ##
    
            #### The actual aliquoting of mastermix
            p300.aspirate(rest_volume, aspiration_location)
              ## Aspirate the amount specified in aspiration_vol from the   ##
              ## location specified in aspiration_location.                 ##
            p300.dispense(rest_volume, well.top(z = - 10))
              ## Dispense the amount specified in dispension_vol to the     ##
              ## location specified in well (looping through plate)         ##
            p300.dispense(10, aspiration_location)
              ## Alternative for blow-out, make sure the tip doesn't fill   ##
              ## completely when using a disposal volume by dispensing some ##
              ## of the volume after each pipetting step. (blow-out too many##
              ## bubbles)                                                   ##
      
    p300.drop_tip()
      ## when entire plate is full, drop tip                                ##
# =============================================================================


# TURN RAIL LIGHT OFF==========================================================
# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================