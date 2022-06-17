""""
VERSION: V_June22
aliquots a specific volume from 15mL tubes to 96 wells plates

This version works with api2.12 and includes labware offsets


"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# How many plates you want filled? (max 6 for now)
number_of_plates = 1

# How much volume (µL) to aliquot?
volume = 100

# How much volume (µL) in 15mL tubes (all the same volume)
reagent_volume = 15000

# What is the starting position of the tips?
starting_tip_p20 = 'A1'
starting_tip_p200 = 'A1'

# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol 
# =============================================================================

# IMPORT STATEMENTS AND FILES==================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.
import pandas as pd
  ## For accessing offset .csv file
import math
  ## To do some calculations 

# If not simulated, import the .csv from the robot with robot_specific 
# labware off_set values
if not simulate: #Robot
    offsets = pd.read_csv(
        "data/user_storage/mollab_modules/labware_offset.csv", sep=';'
        )
      ## import .csv
    offsets = offsets.set_index('labware')
      ## remove index column
    from data.user_storage.mollab_modules import volume_tracking_v2 as vt
      ## Volume_tracking module for robot

if simulate: #Simulator
    from mollab_modules import volume_tracking_v2 as vt
      ## Volume_tracking module for simulator
    import json
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.     
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
necessary_volume = volume * (number_of_plates * 96)
  ## How much water is needed for per sample
number_of_tubes = math.ceil((necessary_volume + 2000) / reagent_volume) 
  ## How many tubes of 15mL are needed (2mL extra)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'aliquoting_from15mL_to96plate.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('aliquot from 15mL to plate protocol'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    aliquoting a specific volume from 15mL tubes to 96 wells plates
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    labwares = {}
      ## empty dict to add labware and labware_names to, to loop through
      
    ##### Loading labware
    tips_200_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',         
        10,                                         
        'tips_200_1')                                 
    labwares[tips_200_1] = 'filtertips_200'
    tips_200_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',         
        11,                                         
        'tips_200_2')                               
    labwares[tips_200_2] = 'filtertips_200'
    
    tubes_15mL = protocol.load_labware(
        'opentrons_15_tuberack_falcon_15ml_conical',
        7,                                          
        'tubes_15mL')                               
    labwares[tubes_15mL] = '15mL_tubes'
    
    plate_96_1 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',            
        1,                                          
        'plate_96_1')                               
    labwares[plate_96_1] = 'plate_96'
    
    if number_of_plates >= 2:
        plate_96_2 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',        
            2,                                      
            'plate_96_2')                           
        labwares[plate_96_2] = 'plate_96'
        if number_of_plates >= 3:
            plate_96_3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',        
                3,                                      
                'plate_96_3')                           
            labwares[plate_96_3] = 'plate_96'
            if number_of_plates >= 4:
                plate_96_4 = protocol.load_labware(
                    'biorad_96_wellplate_200ul_pcr',        
                    4,                                      
                    'plate_96_4')                           
                labwares[plate_96_4] = 'plate_96'
                if number_of_plates >= 5:
                    plate_96_5 = protocol.load_labware(
                        'biorad_96_wellplate_200ul_pcr',        
                        5,                                      
                        'plate_96_5')                           
                    labwares[plate_96_5] = 'plate_96'
                    if number_of_plates >= 6:
                        plate_96_6 = protocol.load_labware(
                            'biorad_96_wellplate_200ul_pcr',        
                            6,                                      
                            'plate_96_6')                           
                        labwares[plate_96_6] = 'plate_96'
            
    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                         #instrument definition
        'right',                                    #mount position
        tip_racks=[tips_200_1,tips_200_2])          #assigned tiprack
# =============================================================================

# LABWARE OFFSET===============================================================    
# =============================================================================
    if not simulate:
        for labware in labwares:
            offset_x = offsets.at[labwares[labware],'x_offset']
            offset_y = offsets.at[labwares[labware],'y_offset']
            offset_z = offsets.at[labwares[labware],'z_offset']
            labware.set_offset(
                x = offset_x, 
                y = offset_y, 
                z = offset_z)
# =============================================================================

# SETTING LOCATIONS#!!!========================================================
# =============================================================================    
    ##### Setting starting tip
    p300.starting_tip = tips_200_1.well(starting_tip_p200)
      ## The starting_tip is the location of first pipette tip in the box   
    
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
    if number_of_plates > 3:
        for well in plate_96_4.wells():
            aliquots.append(well)
    if number_of_plates > 4:
        for well in plate_96_5.wells():
            aliquots.append(well)
    if number_of_plates > 5:
        for well in plate_96_6.wells():
            aliquots.append(well)
      ## Add all wells of all plates to a list                              


# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.pause("I need "+ str(number_of_tubes) + " 15mL tubes. Filled to "
                   + str(reagent_volume/1000) + " mL with reagent.") 
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
    start_height = vt.cal_start_height('tube_15mL', reagent_volume)
    current_height = start_height
    container = 'tube_15mL'
    
    ##### aliquoting
    for i, well in enumerate(destination):
      ## aliquot in the correct wells, for each well do the following:  
       
        if i == 0: 
            p300.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    
        elif i % 24 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
              ## Then, after every 24th well, drop tip and pick up new      
        
        current_height, pip_height, bottom_reached = vt.volume_tracking(
            container, volume, current_height, 'emptying')
              ## call volume_tracking function, obtain current_height,      
              ## pip_height and whether bottom_reached.                     
        
        if bottom_reached:
            ## continue with next tube, reset vt                            
            current_height = start_height
            current_height, pip_height, bottom_reached = (
                vt.volume_tracking(
                    container, volume, current_height, 'emptying'))
            counter = counter + 1
            source = reagent[counter]
            aspiration_location = source.bottom(current_height)
            protocol.comment(
            "Continue with tube " + str(counter + 1) + " of reagent")
       
        else:
            aspiration_location = source.bottom(pip_height)
              ## Set the location of where to aspirate from.                
        
        #### The actual aliquoting
        p300.aspirate(volume, aspiration_location)
          ## Aspirate the set volume from the source                        
        p300.dispense(volume + 10, well)
          ## dispense the set volume + extra to avoid drops in the well     
        p300.dispense(10, aspiration_location)
          ## Alternative for blow-out                                       
    
    
    p300.drop_tip()
      ## when entire plate is full, drop tip                               
# =============================================================================

# TURN RAIL LIGHT OFF==========================================================
# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================        