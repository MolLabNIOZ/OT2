"""
VERSION: V_May22
Qubit_mix_and_samples.py is a protocol written for the aliquoting of Qubit mix
from a 1.5mL or 5mL tube to a PCR plate, standards are added from 1.5mL tubes
to the first row of the plate, then samples are added from either strips, a 
plate or 1.5mL tubes.

You have to provide: 
    Location of the starting tips of the P20 and the P300.
    The number of samples.
        Maximum number of samples = 88 (96-8)
    When you are using PCR strips you need to provide the columns in which you
    will put the strips. 
        Options are columns 2, 7 and 11 or 2, 5, 8 and 11. There is enough 
        space on the deck to use 3 columns per rack for the maximum number of
        samples.
    The well name of your first sample.
        A1 is the standard for tubes and plates, A2 is the standard for PCR
        strips. This is a variable that is especially important when you are
        measuring samples from a plate, and your first sample to measure is 
        not in the first well of the plate.

The protocol calculates how much mix it needs by the number of samples that 
you provide. It also tells you which tube you should put your Qubit mix in 
(<26 samples 1.5mL tube, >26 samples 5mL tube). Aliquotes 48uL of mix
to the first row of the plate, and 49uL of mix to the rest of the wells. 
2uL of standards are added from the standard source rack, 4x STD1 from A1 of
the standard source rack to A1 - D1 of the destination plate, 4x STD2 from 
A2 of the standard source rack to E1 - H1 of the destination plate.
Finally 1uL of samples is added from the sample sources to the rest of the 
wells.

Updates:
(SV) 221020: 
    - automated qubit mix tube selection 
    - added protocol description
220930 MB: 
    - Deleted some unnecesarry things. 
    - Outcommented the offset stuff
    - Changed deck positions for Qmix and std_tubes to make it faster and mix does 
      not go over the standards.
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# What is the starting position of the 200µL tips?
starting_tip_p300 = 'A1'
    ## If not applicable, you do not have to change anything

# How many samples do you want to include?
## For now: max. = 88 samples
number_of_samples = 10

# What labware are your samples in?
sample_tube_type = 'tube_1.5mL'  
  ## If your samples are in strips copy/paste 'PCR_strip'                                       
  ## If your samples are in a plate copy/paste 'plate_96'  
  ## If your samples are in 1.5 ml eppendorfs copy/paste 'tube_1.5mL'  
  
# In which columns are the strips in the plate (ignore if not using strips)?
sample_columns = ['2', '7', '11']
  ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
  ## max 4 racks with strips!  

# What is the location of your first sample (fill in if you have a plate)?                                    
first_sample = 'A1'
  ## 'A1' is standard for tubes and plates. 
  ## 'A2' is standard for tube_strips
  ## But if you have more samples in the plate than
  ## fit in a plate, change the first well position.

# Do you want to simulate the protocol?
simulate = False
  ## True for simulating protocol, False for robot protocol
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.

# import pandas as pd
#   ## Import pandas to open the dataframe with the labware offsets.

import math
  ## Import math for some calculations.

if simulate: #Simulator
    from mollab_modules import volume_tracking_v1 as vt
    import json
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware. 
else: #Robot
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
  
# CALCULATED AND SET VARIABLES=================================================
# =============================================================================
# # If not simulated, import the .csv from the robot with robot_specific 
# # labware off_set values
# if not simulate:
#     offsets = pd.read_csv(
#         "data/user_storage/mollab_modules/labware_offset.csv", sep=';')
#     offsets = offsets.set_index('labware')
# Which tube are you using for your Qubit mix? (options 1.5mL or 5mL)
  ## For samples < 26: 'tube_1.5mL'                                        
  ## For samples > 26: 'tube_5mL'  
if number_of_samples < 26:    
    Qmix_tube_type = 'tube_1.5mL'
else: 
    Qmix_tube_type = 'tube_5mL'

# In which well is your mix tube? 
Qmix_source = 'A1'

# Dispension volume of the mix for the standards
dispension_vol_std = 48

# Dispension volume of the mix for the samples
dispension_vol_sample = 49

# Volume of the standard to add
std_vol = 2

# Volume of the sample to add
sample_vol = 1

std_wells =  ['A1', 'B1']

start_vol = (number_of_samples*dispension_vol_sample) + (8*dispension_vol_std)
# Which tube are you using for your Qubit mix? (options 1.5mL or 5mL)
  ## For volume < 1300: 'tube_1.5mL'                                        
  ## For volume > 1300: 'tube_5mL'  
if start_vol < 1300:
    Qmix_tube_type = 'tube_1.5mL'
else:
    Qmix_tube_type = 'tube_5mL'

if sample_tube_type == 'tube_1.5mL':
    samples_per_rack = 24
if sample_tube_type == 'plate_96':
    samples_per_rack = 96
if sample_tube_type == 'PCR_strip':
    samples_per_rack = 8 * len(sample_columns)
sample_racks = math.ceil(number_of_samples / samples_per_rack)
  ## How many tube_strip_racks are needed (1,2 or 3)
# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'Qubit - mix and samples',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>, MB <maartje.brouwer@nioz.nl>',
    'description': ('Aliquoting Qubit mix and adding samples/standards'),
    'apiLevel': '2.12'}
def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting Qubit mix (48µL for standards, 49µL for samples);
    Adding standards from 1.5mL tubes (2µL)
    Adding samples from different labware (1µL)
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES ================================================
# =============================================================================
    # Create empty dict to add labware and labware_names to     
    labwares = {}    

    # Pipette tips
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',
        10,
        '200tips')
    labwares[tips_200] = 'filtertips_200'
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',
        8,
        '20tips_1')
    labwares[tips_20_1] = 'filtertips_20'
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',
        11,
        '20tips_2')
    labwares[tips_20_2] = 'filtertips_20'
    tips_20 = [tips_20_1, tips_20_2]
    
    # Tube racks & plates
    if Qmix_tube_type == 'tube_1.5mL':
        Qmix_tube = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        4,
        'Qubit_mix_tube')
        labwares[Qmix_tube] = '1.5mL_tubes'

    if sample_tube_type == 'tube_1.5mL':
        sample_source_1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            2,
            'sample_source_1')
        labwares[sample_source_1] = '1.5mL_tubes'
        sample_source_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            3,
            'sample_source_2')
        labwares[sample_source_2] = '1.5mL_tubes'
        sample_source_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            5,
            'sample_source_3')
        labwares[sample_source_3] = '1.5mL_tubes'
        sample_source_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            6,
            'sample_source_4')
        labwares[sample_source_4] = '1.5mL_tubes'
    
    if sample_tube_type == 'plate_96':
        sample_source_1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            2,                                  
            'sample_source_1')
        labwares[sample_source_1] = 'plate_96'

    if simulate: #Simulator
        with open("labware/biorad_qpcr_plate_nioz_plateholder/"
                  "biorad_qpcr_plate_nioz_plateholder.json") as labware_file:
            labware_def_niozplate = json.load(labware_file)
        destination_plate = protocol.load_labware_from_definition(
            labware_def_niozplate,
            7,
            '96well_plate')
        labwares[destination_plate] = 'plate_96'
        if Qmix_tube_type == 'tube_5mL':
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                 "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file: 
                labware_def_5mL = json.load(labware_file)
            Qmix_tube = protocol.load_labware_from_definition( 
                labware_def_5mL,           
                4,                         
                'Qubit_mix_tube')
            labwares[Qmix_tube] = '5mL_screw_cap'
        if sample_tube_type == 'PCR_strip':
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                labware_def_pcrstrips = json.load(labware_file)
            sample_source_1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                2,                         
                'sample_source_1')    
            labwares[sample_source_1] = 'pcr_strips'
            sample_source_2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, 
                3,                     
                'sample_source_2')    
            labwares[sample_source_2] = 'pcr_strips'
            sample_source_3 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,
                5,                   
                'sample_source_3')   
            labwares[sample_source_3] = 'pcr_strips'
            sample_source_4 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,
                6,                   
                'sample_source_4')    
            labwares[sample_source_4] = 'pcr_strips'
    else: 
        destination_plate = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',
            7,
            '96well_plate')
        labwares[destination_plate] = 'plate_96'
        if Qmix_tube_type == 'tube_5mL':
            Qmix_tube = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                4,                                     
                'Qubit_mix_tube') 
            labwares[Qmix_tube] = '5mL_screw_cap'
        if sample_tube_type == 'PCR_strips':
            sample_source_1 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                2,                                     
                'sample_source_1')
            labwares[sample_source_1] = 'pcr_strips'                      
            sample_source_2 = protocol.load_labware_( 
                'pcrstrips_96_wellplate_200ul',    
                3,                                 
                'sample_source_2')         
            labwares[sample_source_2] = 'pcr_strips'
            sample_source_3 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',    
                5,                                
                'sample_source_3') 
            labwares[sample_source_3] = 'pcr_strips'
            sample_source_4 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',    
                6,                                
                'sample_source_4') 
            labwares[sample_source_4] = 'pcr_strips'
   
    std_tube = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        1,
        'std_source')
    labwares[std_tube] = '1.5mL_tubes'

    # Pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',             
        'right',                        
        tip_racks=[tips_200])           
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  
        'left',                             
        tip_racks=tips_20)
# =============================================================================

# LABWARE OFFSET===============================================================    
# =============================================================================
    # if not simulate:
    #     for labware in labwares:
    #         offset_x = offsets.at[labwares[labware],'x_offset']
    #         offset_y = offsets.at[labwares[labware],'y_offset']
    #         offset_z = offsets.at[labwares[labware],'z_offset']
    #         labware.set_offset(
    #             x = offset_x, 
    #             y = offset_y, 
    #             z = offset_z)
# =============================================================================    

# PREDIFINED VARIABLES=========================================================
# =============================================================================
    aspiration_vol_std = (dispension_vol_std + (dispension_vol_std/100*2))
    aspiration_vol_sample = (
        dispension_vol_sample + (dispension_vol_sample/100*2))
      ## The aspiration_vol is the volume (µL) that is aspirated from the   
      ## container.                                                         
    
    ##### Variables for volume tracking
    start_height = vt.cal_start_height(Qmix_tube_type, start_vol)
      ## Call start height calculation function from volume tracking module.
    current_height = start_height
      ## Set the current height to start height at the beginning of the     
      ## protocol.      

    std_mix_vol = std_vol + 3
    sample_mix_vol = sample_vol + 3
      ## mix_vol = volume for pipetting up and down                  
# =============================================================================                   

# SETTING LOCATIONS============================================================
# =============================================================================
    # Setting starting tip
    p300.starting_tip = tips_200.well(starting_tip_p300)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
    
    # Qubit mix location
    QubitMix = Qmix_tube['A1']
    
    # Make a list of all possible wells in the destination plate
    destination_wells = destination_plate.wells()
        
    # Create a list of wells where the standards should go.
    std_wells_0 = destination_wells[0:4]
    std_wells_1 = destination_wells[4:8]
    std_wells = std_wells_0 + std_wells_1
    # Create a list of wells where the samples should go.
    #first we need to slice the list after the standards and after the samples
    slice_sample_wells = slice(8, 8 + number_of_samples)
    #then we add the slice object to access the list
    sample_wells = destination_wells[slice_sample_wells]
    
    # Determin sample
    sample_source_wells = []
    sample_source_wells_string = []
      ## The string list is needed to be able to start at another well
    if sample_tube_type == 'tube_1.5mL' or sample_tube_type == 'plate_96':
        if sample_racks >= 1:
            for well in sample_source_1.wells():
                sample_source_wells.append(well)
                sample_source_wells_string.append(str(well))
        if sample_racks >= 2:
            for well in sample_source_2.wells():
                sample_source_wells.append(well)
                sample_source_wells_string.append(str(well))
        if sample_racks >= 3:
            for well in sample_source_3.wells():
                sample_source_wells.append(well)
                sample_source_wells_string.append(str(well))
        if sample_racks >= 4:
            for well in sample_source_4.wells():
                sample_source_wells.append(well)
                sample_source_wells_string.append(str(well))

    if sample_tube_type == 'PCR_strip':
        sample_source_columns = (
                ([sample_source_1.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
        if sample_racks >= 2:
            sample_columns_2 = (
                ([sample_source_2.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_2:
                sample_source_columns.append(column)
        if sample_racks >= 3:
            sample_columns_3 = (
                ([sample_source_3.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_3:
                sample_source_columns.append(column)
        if sample_racks >= 4:
            sample_columns_4 = (
                ([sample_source_4.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
            for column in sample_columns_4:
                sample_source_columns.append(column)
          ## Make a list of columns, this is a list of lists!   
        for column in sample_source_columns:
            for well in column:
                sample_source_wells.append(well)
                sample_source_wells_string.append(str(well))
          ## Separate the columns into wells and append them to list 

    ## Cut slice out of list of sample_sources, starting with the 
    ## indicated first sample and ending after the number_of_samples                        
    first_sample_index = sample_source_wells_string.index(
        first_sample + ' of sample_source_1 on 2')
      ## Determine the index of the first sample in the list made from 
      ## strings -- we cannot find strings in the normal robot list
      ## so we needed to convert the wells to strings.
    slice_sample_sources = slice(
        first_sample_index, 
        first_sample_index + number_of_samples)
      ## Determine the slice
    ## Cut sample slice out of sample_source_wells list
    sample_sources = sample_source_wells[slice_sample_sources]
    
    ## Determine standard source
    std_source_0 = std_tube.wells_by_name()['A1']
    std_source_1 = std_tube.wells_by_name()['B1']
# =============================================================================

# PIPETTING====================================================================    
# =============================================================================
# LIGHTS-----------------------------------------------------------------------
    # Always put the light off when starting the protocol.
    protocol.set_rail_lights(False)
## COMMENTS--------------------------------------------------------------------    
    protocol.pause("Please insert a " + Qmix_tube_type + " containing " + 
                   str(start_vol) + "µL of QubitMix in a rack on slot 1")
# ALIQUOTING MIX STANDARDS-----------------------------------------------------
    pipette = p300
    for i, well in enumerate(std_wells):
      ## aliquot mix, for each well do the following:                       
        if i == 0: 
            pipette.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    
        elif i % 8 == 0:
            pipette.drop_tip()
            pipette.pick_up_tip()
              ## Then, after every 8th well, drop tip and pick up new       
    
        current_height, pip_height, bottom_reached = vt.volume_tracking(
                Qmix_tube_type, dispension_vol_std, current_height)
                  ## call volume_tracking function, obtain current_height,  
                  ## pip_height and whether bottom_reached.                 
        
        if bottom_reached:
            aspiration_location = QubitMix.bottom(z=1)
            protocol.comment("You've reached the bottom of the tube!")
              ## If bottom is reached keep pipetting from bottom + 1        
        else:
            aspiration_location = QubitMix.bottom(pip_height)
              ## Set the location of where to aspirate from.                

        #### The actual aliquoting of mastermix                             
        pipette.aspirate(aspiration_vol_std, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the       
          ## location specified in aspiration_location.                     
        pipette.dispense(dispension_vol_std, well)
          ## Dispense the amount specified in dispension_vol to the         
          ## location specified in well (so a new well every time the       
          ## loop restarts)                                                 
        pipette.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill      
          ## completely when using a disposal volume by dispensing some     
          ## of the volume after each pipetting step. (blow-out to many     
          ## bubbles)                                                       
    pipette.drop_tip()   
 
 # ALIQUOTING MIX SAMPLES-----------------------------------------------------
    # use the current height  of the mix after pipetting the standards
    # as a starting point
    current_height = current_height
    pipette = p300
    for i, well in enumerate(sample_wells):
      ## aliquot mix, for each well do the following:                       
        if i == 0: 
            pipette.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    
        elif i % 8 == 0:
            pipette.drop_tip()
            pipette.pick_up_tip()
              ## Then, after every 8th well, drop tip and pick up new       
    
        current_height, pip_height, bottom_reached = vt.volume_tracking(
                Qmix_tube_type, dispension_vol_sample, current_height)
                  ## call volume_tracking function, obtain current_height,  
                  ## pip_height and whether bottom_reached.                 
        
        if bottom_reached:
            aspiration_location = QubitMix.bottom(z=1)
            protocol.comment("You've reached the bottom of the tube!")
              ## If bottom is reached keep pipetting from bottom + 1        
        else:
            aspiration_location = QubitMix.bottom(pip_height)
              ## Set the location of where to aspirate from.                
    
        #### The actual aliquoting of mastermix                             
        pipette.aspirate(aspiration_vol_sample, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the       
          ## location specified in aspiration_location.                     
        pipette.dispense(dispension_vol_sample, well)
          ## Dispense the amount specified in dispension_vol to the         
          ## location specified in well (so a new well every time the       
          ## loop restarts)                                                 
        pipette.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill      
          ## completely when using a disposal volume by dispensing some     
          ## of the volume after each pipetting step. (blow-out to many     
          ## bubbles)                                                       
    pipette.drop_tip()    
# ADDING STANDARDS-------------------------------------------------------------
    for well in std_wells_0:
        p20.pick_up_tip()
        p20.aspirate(std_vol, std_source_0)
        p20.dispense(std_vol, well)           
        p20.mix(3, std_mix_vol, well)
        p20.dispense(10, well)
        p20.drop_tip()
    for well in std_wells_1:
        p20.pick_up_tip()
        p20.aspirate(std_vol, std_source_1)
        p20.dispense(std_vol, well)           
        p20.mix(3, std_mix_vol, well)
        p20.dispense(10, well)
        p20.drop_tip()
# ADDING SAMPLES---------------------------------------------------------------
    ## Loop through source and destination wells
    for sample_tube, well in zip(sample_sources, sample_wells):
        p20.pick_up_tip()
        p20.aspirate(sample_vol, sample_tube)
        p20.dispense(sample_vol, well)
        sample_mix_vol = sample_vol + 3
          ## primer_mix_vol = volume for pipetting up and down              
        p20.mix(3, sample_mix_vol, well)
        p20.dispense(10, well)
        p20.drop_tip()
# =============================================================================
    