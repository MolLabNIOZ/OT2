"""
Version: Jan 2023
aliquot_tube_to96plates.py is a protocol to aliquot something from a single 
tube into (up to 8) 96wells plates.

You have to provide:
    number_of _plates you want to be filled
        max 8
    volume you want to be aliquoted
    source_tube_type type of tube the source is in
        'tubes_1.5mL', 'tubes_5mL', 'tubes_15mL', 'tubes_50mL'
        Can be multiple tubes of the same type
    starting_volume of the source
        Must be the exact same for all tubes

Robot does:
    aliquot the specified amount into the desired amount of plates
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the first pipette tip?
starting_tip = 'A1'
  ## for volumes <= 20, p20 tips, otherwise p300/p200 tips

# How many plates you want filled?
number_of_plates = 5  
  ## (max 6 for now)

# How much volume (µL) do you want in each well?
volume = 10

# What kind of tube will the reagent be in?
source_tube_type = 'tube_5mL'
  ## Options:
      #sample_tubes = 'tube_1.5mL'
      #sample_tubes = 'tube_5mL'
      #sample_tubes = 'tube_15mL'
      #sample_tubes = 'tube_50mL'

# How much volume (µL) is in the source tubes
starting_volume = 3000
  ## Must all contain the same volume
  
# Are you simulating the protocol, or running it on the OT2?
simulate = True
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
#### Import opentrons protocol API v2.
from opentrons import protocol_api
                                        
##### Import volume_tracking module 
if simulate:
    import json
    from mollab_modules import volume_tracking_v1 as vt
else: 
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
                
# Import other modules                        
import math
  ## math to do some calculations (rounding up)
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
# How much water is needed in total
necessary_volume = volume * (number_of_plates * 96)
# How many tubes are needed (5% extra)  
number_of_tubes = math.ceil(
    (necessary_volume + (necessary_volume*0.05)) / starting_volume) 
# Adjust starting_volume for vt, so it starts well below the surface
adjusted_starting_volume = starting_volume * 0.9
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'aliquot_tube_to96plates.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('aliquot from a tube to plates protocol'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    aliquoting a specific volume from a specific type of tubes to a certain
    amount of 96 wells plates
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading pipette tips
    if volume <= 20:
        if simulate:
            with open("labware/tipone_96_tiprack_20ul/"
                 "tipone_96_tiprack_20ul.json") as labware_file:
                      labware_def_tipone_20ul = json.load(labware_file)
            tips_1 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
                11,                         
                'tipone_20tips_1')
            tips_2 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
                10,                         
                'tipone_20tips_2')
        else:    
            tips_1 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                11,                                  
                'tipone_20tips_1')
            tips_2 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                10,                                  
                'tipone_20tips_2')
        
    else:
        # if simulate:
            # with open("labware/tipone_96_tiprack_300ul/"
            #      "tipone_96_tiprack_300ul.json") as labware_file:
            #           labware_def_tipone_300ul = json.load(labware_file)
            # tips_1= protocol.load_labware_from_definition( 
            #     labware_def_tipone_300ul,           
            #     11,                         
            #     'tipone_300tips_1')
            # tips_2 = protocol.load_labware_from_definition( 
            #     labware_def_tipone_300ul,           
            #     10,                         
            #     'tipone_300tips_2')
        # else:     
            # tips_1 = protocol.load_labware(
            #     'tipone_96_tiprack_300ul',  
            #     11,                                  
            #     'tipone_300tips_1')
            # tips_2 = protocol.load_labware(
            #     'tipone_96_tiprack_300ul',  
            #     10,                                  
            #     'tipone_300tips_2'))
        tips_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  
            11,                                  
            '200tips_1')
        tips_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  
            10,                                  
            '200tips_2')
    
    ##### Loading labware
    ## Tube with the reagent to be aliquoted
    if source_tube_type == 'tube_1.5mL':
        source_tubes = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            7,
            'source_tubes_1.5mL')
    elif source_tube_type == 'tube_5mL':
        if simulate:
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                      "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                    labware_def_5mL = json.load(labware_file)
            source_tubes = protocol.load_labware_from_definition( 
                labware_def_5mL, 
                7, 
                'source_tubes_5mL')
        else:
            source_tubes = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                7,
                'source_tubes_5mL')
    elif source_tube_type == 'tube_15mL':
        source_tubes = protocol.load_labware(
            'opentrons_15_tuberack_falcon_15ml_conical',
            7,
            'source_tubes_15mL') 
    elif source_tube_type == 'tube_50mL':
        source_tubes = protocol.load_labware(
            'opentrons_6_tuberack_falcon_50ml_conical',
            7,
            'source_tubes_50mL')
    
    ## Plates to aliquot in
    plate_96_1 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',
        8,
        'plate_96_1')
    if number_of_plates >= 2:
        plate_96_2 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            9,
            'plate_96_2')
    if number_of_plates >= 3:
        plate_96_3 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            4,
            'plate_96_3')
    if number_of_plates >= 4:
        plate_96_4 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            5,
            'plate_96_4')
    if number_of_plates >= 5:
        plate_96_5 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            6,
            'plate_96_5')
    if number_of_plates >= 6:
        plate_96_6 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            1,
            'plate_96_6')
    if number_of_plates >= 7:
        plate_96_7 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            2,
            'plate_96_7')
    if number_of_plates >= 8:
        plate_96_8 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            3,
            'plate_96_8')
        
    ##### Loading pipettes
    if volume <= 20:
        pipette = protocol.load_instrument(
            'p20_single_gen2',
            'left',
            tip_racks=[tips_1,tips_2])
    else:
        pipette = protocol.load_instrument(
            'p300_single_gen2',
            'right',
            tip_racks=[tips_1,tips_2])
# =============================================================================

# SETTING LOCATIONS#!!!========================================================
# =============================================================================    
    ##### Setting starting tip
    pipette.starting_tip = tips_1.well(starting_tip)
      ## The starting_tip is the location of first pipette tip in the box   
    
    ##### Setting tube locations
    reagent = []
    for well in source_tubes.wells():
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
    if number_of_plates > 3:
        for well in plate_96_4.wells():
            aliquots.append(well)
    if number_of_plates > 4:
        for well in plate_96_5.wells():
            aliquots.append(well)
    if number_of_plates > 5:
        for well in plate_96_6.wells():
            aliquots.append(well)
    if number_of_plates > 6:
        for well in plate_96_7.wells():
            aliquots.append(well)
    if number_of_plates > 7:
        for well in plate_96_8.wells():
            aliquots.append(well)  
      ## Add all wells of all plates to a list                              
# =============================================================================

# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.comment("I need "+ str(number_of_tubes) + " " + source_tube_type + 
                     " Filled to " + str(starting_volume) + " µL with reagent.") 
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
    start_height = vt.cal_start_height(
        source_tube_type, adjusted_starting_volume)
    current_height = start_height
    container = source_tube_type
    
    ##### Loop through all destination wells
    for i, well in enumerate(destination):
      ## for each well do the following:  
        
        # Check if you need to pick up or change tips
        if i == 0: 
            pipette.pick_up_tip()
          ## If we are at the first well, start by picking up a tip.
        elif i % 24 == 0:
            pipette.drop_tip()
            pipette.pick_up_tip()
          ## Then, after every 24th well, drop tip and pick up a new one
              
        # Use volume tracking to determine the current height to pipette from
        current_height, pip_height, bottom_reached = vt.volume_tracking(
            container, volume, current_height)
              ## call volume_tracking function, obtain current_height,      
              ## pip_height and whether bottom_reached.                     
        
        # If the bottom of a source_tube is reached, continue with the next one
        if bottom_reached:
            ## continue with next tube and reset vt                            
            current_height = start_height
            current_height, pip_height, bottom_reached = (
                vt.volume_tracking(
                    container, volume, current_height))
            counter = counter + 1
            source = reagent[counter]
            aspiration_location = source.bottom(current_height)
            protocol.comment(
            "Continue with tube " + str(counter + 1) + " of reagent")
       
        # If the bottom is not reached, aspirate at the current pip_height
        else:
            aspiration_location = source.bottom(pip_height)
              ## Set the location of where to aspirate from.                
        
        ##### The actual aliquoting
        pipette.aspirate(volume, aspiration_location)
          ## Aspirate the set volume from the source                        
        pipette.dispense(volume + 10, well)
          ## dispense the set volume + extra to avoid drops in the well     
        pipette.dispense(10, aspiration_location)
          ## Alternative for blow-out                                       
    
    # When completely finished, drop the last tip
    pipette.drop_tip()
      ## when entire plate is full, drop tip                                
# =============================================================================

# TURN RAIL LIGHT OFF==========================================================
# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================        