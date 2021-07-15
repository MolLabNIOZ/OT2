# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 2107014
# Description: aliquot from a 15mL tube into 96wells plates
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
#   # Import volume_tracking module that is on the OT2                        ##
from mollab_modules import volume_tracking_v1 as vt
  ## Import volume_tracking module for simulator                          ##
import math
  ## To do some calculations (rounding up)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'aliquoting_from15mL_to96plate.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('aliquot from 15mL to plate protocol'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    aliquoting a specific volume from 15mL tubes to 96 wells plates
    """
# =============================================================================

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
    number_of_plates = 3  
      ## How many plates you want filled? 
    volume = 50
      ## How much volume (µL) to aliquot?
    starting_tip_p200 = 'A1'
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
    necessary_volume = volume * (number_of_plates * 96)
      ## How much water is needed for per sample
    number_of_tubes = math.ceil(necessary_volume / 15000) + 1
      ## How many tubes of 15mL are needed 
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading labware
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',         #labware definition
        10,                                         #deck position
        'tips_200')                                 #custom name
    
    tubes_15mL = protocol.load_labware(
        'opentrons_15_tuberack_falcon_15ml_conical',#labware definition
        7,                                          #deck position
        'tubes_15mL')                               #custom name    
    
    plate_96_1 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',            #labware definition
        1,                                          #deck position
        'plate_96_1')                               #custom name
    if number_of_plates >= 2:
        plate_96_2 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',        #labware definition
            2,                                      #deck position
            'plate_96_2')                           #custom name
    if number_of_plates >= 3:
        plate_96_3 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',        #labware definition
            3,                                      #deck position
            'plate_96_3')                           #custom name

    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                         #instrument definition
        'right',                                    #mount position
        tip_racks=[tips_200])                       #assigned tiprack
# =============================================================================

# SETTING LOCATIONS#!!!========================================================
# =============================================================================    
    ##### Setting starting tip
    p300.starting_tip = tips_200.well(starting_tip_p200)
      ## The starting_tip is the location of first pipette tip in the box   ##
    
    ##### Setting tube locations
    reagent = []
    for well in tubes_15mL.wells():
        reagent.append(well)
    reagent = reagent[:number_of_tubes]
    
    aliquots = []
    for well in plate_96_1.wells():
        aliquots.append(well)
    if number_of_plates > 1:
        for well in plate_96_2.wells():
            aliquots.append(well)
    if number_of_plates > 2:
        for well in plate_96_3.wells():
            aliquots.append(well)
      ## Add all wells of all plates to a list                              ##


# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.pause("I need "+ str(number_of_tubes) + " 15mL tubes.") 
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
    start_height = vt.cal_start_height('tube_15mL', 15000)
    current_height = start_height
    container = 'tube_15mL'
    
    ##### aliquoting
    for i, well in enumerate(destination):
      ## aliquot in the correct wells, for each well do the following:  
       
        if i == 0: 
            p300.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    ##
        elif i % 24 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
              ## Then, after every 24th well, drop tip and pick up new      ##
        
        current_height, pip_height, bottom_reached = vt.volume_tracking(
            container, volume, current_height)
              ## call volume_tracking function, obtain current_height,      ##
              ## pip_height and whether bottom_reached.                     ##
        
        if bottom_reached:
            ## continue with next tube, reset vt                            ##
            current_height = start_height
            current_height, pip_height, bottom_reached = (
                vt.volume_tracking(
                    container, volume, current_height))
            counter = counter + 1
            source = reagent[counter]
            aspiration_location = source.bottom(current_height)
            protocol.comment(
            "Continue with tube " + str(counter + 1) + " of reagent")
       
        else:
            aspiration_location = source.bottom(pip_height)
              ## Set the location of where to aspirate from.                ##
        
        #### The actual aliquoting
        p300.aspirate(volume, aspiration_location)
          ## Aspirate the set volume from the source                        ##
        p300.dispense(volume + 10, well)
          ## dispense the set volume + extra to avoid drops in the well     ##
        p300.dispense(10, aspiration_location)
          ## Alternative for blow-out                                       ##
    
    
    p300.drop_tip()
      ## when entire plate is full, drop tip                                ##
# =============================================================================


# TURN RAIL LIGHT OFF==========================================================
# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================        