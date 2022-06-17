"""
VERSION: V_June22
equimolar_dilutions.py is a protocol for diluting samples in equimolar amounts.
This protocol is designed for diluting samples before pooling them.

First use get_dilution_info to get a list of water / EB volumes per sample
Copy that list into this protocol and run this protocol on the OT2

Samples can be provided in a PCR plate, PCR strips or 1.5mL tubes.
The protocol will skip samples that should not be diluted
Dilutions will be made in 1.5mL tubes.

You have to provide:
    A fixed sample volume
    List with volumes of water/EB to dilute a certain volume of sample in
        make sure the order is similar to the sample orientation
        negative values will be skipped
        
    Location of the starting tip in P20 or P200
    Type of tubes the samples are in (max 3 racks/deck positions)

The protocol will tell you what tube and volume of water/EB you need to provide
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the tips?
starting_tip_p20 = 'A1'
starting_tip_p200 = 'A1'

# Use get_uL_info.py to get a list of volumes
dilution_µL_list = ([35.81, -244.2, 218.04, 185.13, 
                     133.82, 185.78, 164.05, 260.63,
                     283.59, 114.26, -7.35, 175.14, 
                     200.77, 193.68, 55.63, -9.21,
                     177.6, 59.54, 259.24, 255.98, 
                     68.96, 294.65, 102.1, 116.59,
                     
                     20.71, 191.48, 76.66, 268.19, 
                     199.99, 216.99, 15.25, 296.05, 
                     123.83, 108.11, 169.59, 19.95, 
                     36.88, 177.57, 293.8, 223.58, 
                     127.49, 216.68, 272.17, 131.68, 
                     32.14, -5.79, -5.27, 118.39, 
                     
                     55.13, 64.29, 83.19, 221.55,
                     163.06, 117.26, 260.96, 268.64,
                     105.88, 196.42, 14.65, 242.2, 
                     83.12, 296.91, -0.08, 143.16, 
                     294.16, 260.89, 96.89, 226.7, 
                     212.2, 297.14, 10.98, 91.54, 
                     
                     64.0, 109.48, 63.42, 85.49, 
                     110.96, 43.12, 46.5, 116.12, 
                     213.0, 98.19, 180.25, 130.45, 
                     217.06, 69.88, 105.4, 243.11, 
                     103.99, 155.62, 196.6, 291.2, 
                     31.83, 96.05, 283.2, 99.59])
  ## Also include the negative volumes and zeros. These will be skipped.

# Specify the number of samples, to check if the number of volumes is correct    
number_of_samples = 96
  ## max 96
  ## max 3 deck position, so (1xplate, 3x 3- or 4strips or 3x 24 tubes)
  ## Including the ones that should not be diluted because of low concentration

# What labware are your samples in?
sample_tube_type = 'plate_96' 
  ##Other options:
# sample_tube_type = 'PCR_strip'                                        
# sample_tube_type = 'tube_1.5mL'  

if sample_tube_type == 'PCR_strips':
    # In which columns are the strips in the plate (ignore if not using strips)?
    sample_columns = ['2', '7','11']
      ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
      ## max 4 racks with strips!

# Volume of sample to add to the dilution reagent
sample_volume = 10

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
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
      ## Volume_tracking module for robot

if simulate: #Simulator
    from mollab_modules import volume_tracking_v1 as vt
      ## Volume_tracking module for simulator
    import json
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.     
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
# Raise exception when number of volumes and number of samples are different
if len(dilution_µL_list) != number_of_samples:
    raise Exception(
        "The number of volumes provided"
        " is not equal to the given number of samples!")

# Check if p300 + tips are needed
if any(i >= 19 for i in dilution_µL_list):
    pipette_p300 = True

# How many sample_tube_racks are needed
if sample_tube_type == 'tube_1.5mL':
    samples_per_rack = 24
if sample_tube_type == 'plate_96':
    samples_per_rack = 96
if sample_tube_type == 'PCR_strip':
    samples_per_rack = 8 * len(sample_columns)
sample_racks = math.ceil(number_of_samples / samples_per_rack)
  ## How many tube_racks are needed
if sample_racks > 3:
    raise Exception("This protocol can only handle 3 sample racks")

# How many dilution_tube_racks are needed (1.5mL tubes)
dilution_racks = math.ceil(number_of_samples / 24)

# Calculate total volume of reagent necesarry to dilute all samples
dilution_reagent_volume = sum(dilution_µL_list)
# Add 10%
dilution_reagent_volume = (dilution_reagent_volume + (dilution_reagent_volume*0.2))

# Based on total_cleanup_volume, determine tube to pool in
if dilution_reagent_volume <= 1500:
    dilution_reagent_tube_type = 'tube_1.5mL'
elif dilution_reagent_volume <=5000:
    dilution_reagent_tube_type = 'tube_5mL'
## NO OFFSETS YET!
# else:
#     raise Exception("There are no offsets available for 15mL/50mL tubes")
elif dilution_reagent_volume <=15000:
    dilution_reagent_tube_type = 'tube_15mL'
else:
    dilution_reagent_tube_type = 'tube_50mL'

# Info for comment about how many tubes with how much reagent to insert
# And to keep track if more than 1 tube is needed
amount_of_tubes = math.ceil(dilution_reagent_volume/50000)
dilution_reagent_volume = dilution_reagent_volume / amount_of_tubes
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'equimolar_dilutions.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('pooling samples in equimolar amounts'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    dilute samples so they end up with all the same concentration
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    labwares = {}
      ## empty dict to add labware and labware_names to, to loop through
      
    ##### Loading pipettetips
    if pipette_p300:
        tips_200 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  
            10,                                  
            '200tips')
        labwares[tips_200] = 'filtertips_200'
        
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  
        11,                                  
        '20tips')
    labwares[tips_20_1] = 'filtertips_20'
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  
        9,                                  
        '20tips')
    labwares[tips_20_2] = 'filtertips_20'
    
    ##### Loading labware
    
    ## Tubes to get samples from
    if sample_tube_type == 'plate_96':
        samples1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            3,
            'samples1')
        labwares[samples1] = 'plate_96'
        if sample_racks > 1:
            samples2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                2,
                'samples2')
            labwares[samples2] = 'plate_96'
            if sample_racks > 2:
                samples3 = protocol.load_labware(
                    'biorad_96_wellplate_200ul_pcr',
                    1,
                    'samples3')
    
    elif sample_tube_type == 'PCR_strip':
        if simulate:
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            samples1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                3,                         
                'samples1')
            if sample_racks > 1:
                samples2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips,     
                    2,                         
                    'samples2')
                if sample_racks > 2:
                    samples3 = protocol.load_labware_from_definition( 
                        labware_def_pcrstrips,     
                        1,                         
                        'samples3')
        else:
            samples1 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                3,                                     
                'samples1')
            labwares[samples1] = 'pcr_strips'
            if sample_racks > 1:
                samples2 = protocol.load_labware( 
                    'pcrstrips_96_wellplate_200ul',        
                    2,                                     
                    'samples2')
                labwares[samples2] = 'pcr_strips'
                if sample_racks > 2:
                    samples3 = protocol.load_labware( 
                        'pcrstrips_96_wellplate_200ul',        
                        1,                                     
                        'samples3')
                    labwares[samples3] = 'pcr_strips'
        
    elif sample_tube_type == 'tube_1.5mL':
        samples1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            3,
            'samples1')
        labwares[samples1] = '1.5mL_tubes'
        if sample_racks > 1:
            samples2 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                2,
                'samples2')
            labwares[samples2] = '1.5mL_tubes'
            if sample_racks > 2:
                samples3 = protocol.load_labware(
                    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                    1,
                    'samples3')
                labwares[samples3] = '1.5mL_tubes'

    ## Tubes to dilute samples in
    dilutions1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        6,
        'dilutions1')
    labwares[dilutions1] = '1.5mL_tubes'
    if number_of_samples > 24:
        dilutions2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            5,
            'dilutions2')
        labwares[dilutions2] = '1.5mL_tubes'
        if number_of_samples > 48:
            dilutions3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                4,
                'dilutions3')
            labwares[dilutions3] = '1.5mL_tubes'
            if number_of_samples > 72:
                dilutions4 = protocol.load_labware(
                    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                    7,
                    'dilutions4')
                labwares[dilutions4] = '1.5mL_tubes'
    
    ## Tube to get water or buffer from to make the dilutions
    if dilution_reagent_volume < 1500:
        dilution_reagent = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            8,
            'dilution_reagent')
    elif dilution_reagent_volume < 5000:
        if simulate:
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                      "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                    labware_def_5mL = json.load(labware_file)
            dilution_reagent = protocol.load_labware_from_definition( 
                labware_def_5mL, 
                8, 
                'dilution_reagent')
        else:
            dilution_reagent = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                8,
                'dilution_reagent')
    elif dilution_reagent_volume < 15000:
        dilution_reagent = protocol.load_labware(
            'opentrons_15_tuberack_falcon_15ml_conical',
            8,
            'dilution_reagent')
    else:
        dilution_reagent = protocol.load_labware(
            'opentrons_6_tuberack_falcon_50ml_conical',
            8,
            'dilution_reagent')
    
    ## Pipettes
    if pipette_p300:
        p300 = protocol.load_instrument(
            'p300_single_gen2',             
            'right',                        
            tip_racks=[tips_200])
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  
        'left',                             
        tip_racks=[tips_20_1,tips_20_2])
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

# SETTING LOCATIONS============================================================
# =============================================================================
    # Setting starting tip    
    if pipette_p300:
        p300.starting_tip = tips_200.well(starting_tip_p200)
    
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
    
    # Make a list of all possible sample wells in the sample racks
    sample_wells = []
    # For PCR_strips this depends on the used columns
    if sample_tube_type == 'PCR_strip':
       sample_columns = (
           ([samples1.columns_by_name()[column_name] 
             for column_name in sample_columns]))
       if sample_racks > 1:
           sample_columns_2 = (
               ([samples2.columns_by_name()[column_name] 
                 for column_name in sample_columns]))
           for column in sample_columns_2:
               sample_columns.append(column)
           if sample_racks > 2:
               sample_columns_3 = (
                   ([samples3.columns_by_name()[column_name] 
                     for column_name in sample_columns]))
               for column in sample_columns_3:
                   sample_columns.append(column)
       for column in sample_columns:
           for well in column:
               sample_wells.append(well)
    # For plates and 1.5mL tubes, all wells should be included                      
    else:
        for well in samples1.wells():
            sample_wells.append(well)
            if sample_racks > 1:
                for well in samples2.wells():
                    sample_wells.append(well)
                if sample_racks > 2:
                    for well in samples3.wells():
                        sample_wells.append(well)
    
    # Cut of sample_wells list after certain amount of samples
    sample_wells = sample_wells[:number_of_samples]
    
    # Make a list of all possible wells in the dilution racks
    dilution_wells = []
    for well in dilutions1.wells():
        dilution_wells.append(well)
    if dilution_racks > 1:
        for well in dilutions2.wells():
            dilution_wells.append(well)
    if dilution_racks > 2:
        for well in dilutions3.wells():
            dilution_wells.append(well)
    if dilution_racks > 3:
        for well in dilutions4.wells():
            dilution_wells.append(well)
    dilution_wells = dilution_wells[:number_of_samples]
    
    # Make a list of tubes with dilution reagent
    reagent_tubes = []
    for well in dilution_reagent.wells():
        reagent_tubes.append(well)
        reagent_tubes = reagent_tubes[:amount_of_tubes]
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
## COMMENTS--------------------------------------------------------------------    
    protocol.pause("Insert " + str(amount_of_tubes) + " " 
                   + dilution_reagent_tube_type + " containing " 
                   + str(round(dilution_reagent_volume/1000,3)) + "mL water or"
                   " EB buffer into the appropriate rack on slot 5")
## ----------------------------------------------------------------------------   
## LIGHTS----------------------------------------------------------------------    
    protocol.set_rail_lights(True)
## ----------------------------------------------------------------------------
## Aliquoting water or buffer--------------------------------------------------
    # Variables for volume tracking
    counter = 0 #to keep track at which buffer tube you are
    source = reagent_tubes[counter]
    container = dilution_reagent_tube_type
    start_height = vt.cal_start_height(
        dilution_reagent_tube_type, dilution_reagent_volume)
      ## Call start height calculation function from volume tracking module.
    current_height = start_height
      ## Set the current height to start height at the beginning of the     
      ## protocol.  
    
    # Keep track of how many times the tips are used
    p200_counter = 0
    p20_counter = 0
    
    for (well, volume) in zip(dilution_wells, dilution_µL_list):
      ## aliquot the right volume of reagent in the correct wells
      ## For each well do the following:
        if volume > 0:  
        
            # If volume > 199, it needs to be added in multiple steps
            number_of_full_pipettings = math.floor(volume / 199)
            rest_volume = volume - (number_of_full_pipettings * 199) 
            
            # If you need >199µL, the robot needs to do it in multiple times
            for i in range(number_of_full_pipettings):
                pipette = p300
                ## Pipette 199µL for predefined number of times
                current_height, pip_height, bottom_reached = vt.volume_tracking(
                    container, 199, current_height)
                    ## call volume_tracking function, obtain current_height,     
                    ## pip_height and whether bottom_reached.
                # If necesarry pick up tip, or after every 24 pipettings change                    
                if p200_counter == 0:
                    p300.pick_up_tip()
                elif p200_counter % 24 == 0:
                    p300.drop_tip()
                    p300.pick_up_tip()
                
                # If the bottom of the tube is reached and there are more tubes
                # Change to the next tube
                if (bottom_reached and
                    counter + 1 < amount_of_tubes):
                    ## continue with next tube, reset vt                       
                    current_height = start_height
                    current_height, pip_height, bottom_reached = (
                        vt.volume_tracking(
                            container, 199, current_height))
                    counter = counter + 1
                    source = reagent_tubes[counter]
                    aspiration_location = source.bottom(current_height)
                    protocol.comment(
                    "Continue with tube " + str(counter + 1) + " of reagent")         
                # If the bottom of the tube is reached and there are no more
                # tubes, keep pipetting from the bottom
                elif (bottom_reached and
                      counter + 1 == amount_of_tubes):
                    aspiration_location = source.bottom(z=1)
                    protocol.comment("You've reached the bottom of the tube!")
                      ## If bottom is reached keep pipetting from bottom + 1
                # If bottom is not reached, pipette from pip_height
                else:
                    aspiration_location = source.bottom(pip_height)
                      ## Set the location of where to aspirate from.           
  
                #### The actual aliquoting
                pipette.aspirate(200, aspiration_location)
                  ## Aspirate the amount specified in aspiration_vol from the  
                  ## location specified in aspiration_location.                
                pipette.dispense(199, well.top(z = - 10))
                  ## Dispense the amount specified in dispension_vol to the    
                  ## location specified in well (looping through plate)        
                pipette.dispense(10, aspiration_location)
                  ## Alternative for blow-out, make sure the tip doesn't fill  
                  ## completely when using a disposal volume by dispensing some 
                  ## of the volume after each pipetting step. (blow-out too many
                  ## bubbles)                                                   
                
                p200_counter = p200_counter + 1
      
            ##### Pipette rest volume
            # For samples that need < 199µL or when there is some volume left
            if rest_volume > 0:
                # If it's above 19µL, use p300
                if rest_volume > 19:
                    pipette = p300
                    if p200_counter == 0:
                        p300.pick_up_tip()
                    elif p200_counter % 24 == 0:
                        p300.drop_tip()
                        p300.pick_up_tip()
                    p200_counter = p200_counter + 1
                # If it's below 19µL, use p300
                else:
                    pipette = p20
                    if p20_counter == 0:
                        p20.pick_up_tip()
                    elif p20_counter % 24 == 0:
                        p20.drop_tip()
                        p20.pick_up_tip()
                    p20_counter = p20_counter + 1
    
                # Volume tracking
                current_height, pip_height, bottom_reached = vt.volume_tracking(
                        container, rest_volume, current_height)
                      ## call volume_tracking function, obtain current_height,
                      ## pip_height and whether bottom_reached.
                
                # If the bottom of the tube is reached and there are more tubes
                # Change to the next tube
                if (bottom_reached and
                    counter + 1 < amount_of_tubes):
                    ## continue with next tube, reset vt 
                    current_height = start_height
                    current_height, pip_height, bottom_reached = (
                        vt.volume_tracking(
                            container, rest_volume, current_height))
                    counter = counter + 1
                    source = reagent_tubes[counter]
                    aspiration_location = source.bottom(current_height)
                    protocol.comment(
                    "Continue with tube " + str(counter) + " of water")
                
                # If the bottom of the tube is reached and there are no more
                # tubes, keep pipetting from the bottom
                elif (bottom_reached and
                      counter + 1 == amount_of_tubes):
                    aspiration_location = source.bottom(z=1)
                    protocol.comment("You've reached the bottom of the tube!")
                      ## If bottom is reached keep pipetting from bottom + 1 
                
                # If bottom is not reached, pipette from pip_height
                else:
                    aspiration_location = source.bottom(pip_height)
                      ## Set the location of where to aspirate from.
                
                #### The actual aliquoting of mastermix
                pipette.aspirate(rest_volume + 1, aspiration_location)
                  ## Aspirate the amount specified in aspiration_vol from the
                  ## location specified in aspiration_location.
                pipette.dispense(rest_volume, well.top(z = - 10))
                  ## Dispense the amount specified in dispension_vol to the    
                  ## location specified in well (looping through plate)         
                pipette.dispense(10, aspiration_location)
                  ## Alternative for blow-out
        
    # when done drop tips
    if p200_counter > 0:
        p300.drop_tip()
    if p20_counter > 0:
        p20.drop_tip()
## ----------------------------------------------------------------------------
## Adding sample---------------------------------------------------------------
    # Loop through sample wells, dilution wells and dilution volumes
    for (sample_well, dilution_well, volume) in zip(
            sample_wells, dilution_wells, dilution_µL_list):
        
        # For every sample that needs to be diluted
        if volume > 0:
            # pick up a new tip     
            p20.pick_up_tip()
            # Aspirate sample from sample_well
            p20.aspirate(sample_volume, sample_well)
            # Dispense sample in the dilution_well
            p20.dispense(sample_volume, dilution_well)
            # Mix 3x by pipetting up and down
            p20.mix(3, sample_volume + 3, dilution_well)
            # Blow out
            p20.dispense(10, dilution_well)
            # Drop the tip
            p20.drop_tip()

# =============================================================================

# TURN RAIL LIGHT OFF==========================================================
# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================
