"""
VERSION: V_June22
    Author(s): Maartje Brouwer
    Creation date: 210916
EVE_MM_and_samples_in_varying_volumes.py is a protocol written for EVE for the
aliquoting of mastermix, and the addition of samples with varying volumes
EVE also adds up to the max volume with water.

You have to provide:
    Number of samples (max 96, Including PC and NTC)
    Maximum DNA volume
        This is the highest volume of DNA that you have, it is the volume
        to which EVE adds water to the tubes if the DNA volume is less.
    A list with the volumes of DNA that you want to add.
    The location of the tube with water that needs to be used to fill up the
    samples.
    The starting volume of the water
    The well location of the mastermix tube
    The starting volume of the mastermix tube
    The volume of mastermix that is to be dispensed 
    The type of tube that you are doing the PCR in
        Options are PCR strips or 96 wells plate
        If you are using PCR strips you'll need to specify the columns in
        which you are puting the strips
    The starting tip of both the P300 and the P20
    
Updates:
    (SV) 220617:
        - updated protocol for API level 2.12
        - added simulate as a variable to set instead of commenting it out
        - moved the import statements to after the variables to set
"""


# VARIABLES TO SET#!!!=========================================================
# =============================================================================
#### SAMPLES
number_of_samples = 44   # max 96 
  ## How many samples do you want to include? Including PC and NTC           ##
max_DNA_volume = 5
  ## highest DNA volume, to add up to with water if needed
DNA_µL_list = ([3.0, 3.0, 5.0, 5.0, 5.0, 5.0, 2.5, 3.25,
                2.0, 5.0, 3.25, 3.25, 2.5, 3.0, 2.5, 1.5,
                2.5, 2.0, 3.5, 3.25, 2.25, 3.0, 4.0, 2.75,
                3.0, 1.5, 1.25, 1.25, 2.75, 1.0, 1.5, 2.0,
                2.75, 2.25, 2.25, 1.75, 2.25, 3.0, 1.5, 1.25,
                1.0, 1.25, 5.0, 0.0])
  ##How much DNA should be added for each sample (µL)
water_tube = 'C2'
  ## Where is the water tube located in the rack                             ##
  ## Water should be provided in a 5mL tube
start_vol_w = 500
  ## The start_vol_w is the volume (ul) of water that is in the source       ##
  ## labware at the start of the protocol.                                   ##
  
#### Mastermix
mastermix_source = 'C1'
  ## Where is the mastermix tube located in the rack                         ##
  ## Mastermix should be provided in a 5mL tube
start_vol_MM = 2092
  ## The start_vol_MM is the volume (ul) of mastermix that is in the source  ##
  ## labware at the start of the protocol.                                   ##
dispension_vol = 45 
  ## Volume of MasterMix to be aliquoted                                     ##

#### PCR
PCR_tubes = 'PCR_strips'
  ## What kind of tubes will the PCR be in?
  ## Options: 'PCR_strips' or 'plate_96'
if PCR_tubes == 'PCR_strips':
    strip_positions = ['2', '5', '8','11']
    ## optional: ['2', '7', '11'] or ['2', '5', '8','11'] or 
    ## ['1', '3', '5', '7', '9', '11']
    ## max 3 racks with strips!

#### GENRAL
starting_tip_p20 = 'A1'
starting_tip_p200 = 'A1'
  ## The starting_tip is the location of first pipette tip in the box        ##
  
# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol 
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                       ##
import math
  ## To do some calculations (rounding up)
import pandas as pd
  ## For accessing offset .csv file
if simulate: #Simulator
    from mollab_modules import volume_tracking_v1 as vt
    import json 
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.     
else: #Robot
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
# =============================================================================

# OFFSETS======================================================================
# =============================================================================
# If not simulated, import the .csv from the robot with robot_specific 
# labware off_set values
if not simulate:
    offsets = pd.read_csv(
        "data/user_storage/mollab_modules/labware_offset.csv", sep=';'
        )
      ## import .csv
    offsets = offsets.set_index('labware')
      ## remove index column
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
if PCR_tubes == 'PCR_strips':
    if strip_positions == ['2', '5', '8','11']:
        PCR_tubes_per_rack = 32
    elif strip_positions == ['2', '7','11']:
        PCR_tubes_per_rack = 24
    elif strip_positions == ['1', '3', '5', '7', '9', '11']:
        PCR_tubes_per_rack = 48
    PCR_racks = math.ceil(number_of_samples/PCR_tubes_per_rack)
  ## How many PCR tube racks are needed
sample_racks = math.ceil((number_of_samples + 1) / 24)
  ## How many tube_racks are needed (1,2,3 or 4) +1 for water_tube
# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'complete_PCR_different_sample_volumes_EVE',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('PCR - MM +  samples in different volumes'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Alliquoting MasterMix
    Adding samples from 1.5 mL tubes to PCR_strips or plate.
    different DNA volumes + water to add up
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".        ##
    labwares = {}
    #pipette tips
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        9,                                  #deck position
        '200tips')                          #custom name
    labwares[tips_200] = 'filtertips_200'    
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        3,                                  #deck position
        '20tips_1')                         #custom name      
    labwares[tips_20_1] = 'filtertips_20'    
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        6,                                  #deck position
        '20tips_2')                         #custom name
    labwares[tips_20_2] = 'filtertips_20'    

    # Tube_racks & plates
    sample_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        1,                                                       #deck position
        'sample_tubes_1')                                        #custom name
    labwares[sample_tubes_1] = '1.5mL_tubes'    
    if sample_racks >= 2:
        sample_tubes_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            4,                                                       #deck pos
            'sample_tubes_2')                                        #cust name
        labwares[sample_tubes_2] = '1.5mL_tubes'    
    if sample_racks >= 3:
        sample_tubes_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            7,                                                       #deck pos
            'sample_tubes_3')                                        #cust name
        labwares[sample_tubes_3] = '1.5mL_tubes'    
    if sample_racks >= 4:
        sample_tubes_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            10,                                                      #deck pos
            'sample_tubes_4')                                        #cust name
        labwares[sample_tubes_4] = '1.5mL_tubes'    
   
    if PCR_tubes == 'plate_96': 
        PCR_1 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        2,                                  #deck position
        'plate_96')                         #custom name
        labwares[PCR_1] = 'plate_96'    
    

    if simulate: #Simulator
        with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                    "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                  labware_def_5mL = json.load(labware_file)
        tubes_5mL = protocol.load_labware_from_definition( 
            labware_def_5mL,   #variable derived from opening json
            11,                 #deck position
            'tubes_5mL')  #custom name 
        labwares[tubes_5mL] = '5mL_screw_cap'    
        if PCR_tubes == 'PCR_strips':
            with open("labware/pcrstrips_96_wellplate_200ul/"
                        "pcrstrips_96_wellplate_200ul.json") as labware_file:
                      labware_def_pcrstrips = json.load(labware_file)
            PCR_1 = protocol.load_labware_from_definition( 
                  labware_def_pcrstrips, #variable derived from opening json
                  2,                     #deck position
                  'PCR_tube_1')          #custom name
            labwares[PCR_1] = 'pcr_strips'    
            if PCR_racks >= 2:
                PCR_2 = protocol.load_labware_from_definition( 
                      labware_def_pcrstrips, #variable derived from opening json
                      5,                     #deck position
                      'PCR_tube_2')          #custom name
                labwares[PCR_2] = 'pcr_strips'
            if PCR_racks >= 3:
                PCR_3 = protocol.load_labware_from_definition( 
                      labware_def_pcrstrips, #variable derived from opening json
                      8,                     #deck position
                      'PCR_tube_2')          #custom name
                labwares[PCR_3] = 'pcr_strips'
    else: #Robot        
        tubes_5mL = protocol.load_labware(
            'eppendorfscrewcap_15_tuberack_5000ul', #labware def
            11,                                     #deck position
            'tubes_5mL')  
        labwares[tubes_5mL] = '5mL_screw_cap' 
        PCR_1 = protocol.load_labware(
          'pcrstrips_96_wellplate_200ul',    #labware definition
          2,                                 #deck position
          'PCR_tube_1')                      #custom name
        labwares[PCR_1] = 'pcr_strips'
        if PCR_racks >= 2:
            PCR_2 = protocol.load_labware(
                  'pcrstrips_96_wellplate_200ul',    #labware definition
                  5,                                 #deck position
                  'PCR_tube_2')                      #custom name
            labwares[PCR_2] = 'pcr_strips'
        if PCR_racks >= 3:
            PCR_3 = protocol.load_labware(
                  'pcrstrips_96_wellplate_200ul',    #labware definition
                  8,                                 #deck position
                  'PCR_tube_3')                      #custom name
            labwares[PCR_3] = 'pcr_strips'
 
    # Pipettes
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1, tips_20_2])   #assigned tiprack
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack    
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

# PREDIFINED VARIABLES=========================================================
# =============================================================================
    ##### Mastermix
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
      ## The aspiration_vol is the volume (ul) that is aspirated from the    ##
      ## container.                                                          ##
    MM_start_height = vt.cal_start_height('tube_5mL', start_vol_MM)
      ## Call start height calculation function from volume tracking module. ##
    MM_current_height = MM_start_height
      ## Set the current height to start height at the beginning of the      ##
      ## protocol.                                                           ##
    
    ##### Water
    w_start_height = vt.cal_start_height('tube_5mL', start_vol_w)
      ## Call start height calculation function from volume tracking module. ##
    w_current_height = w_start_height
      ## Set the current height to start height at the beginning of the      ##
      ## protocol.                                                           ## 
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    ##### Setting starting tip                                               ##
    p300.starting_tip = tips_200.well(starting_tip_p200)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
      ## The starting_tip is the location of first pipette tip in the box    ##

    # Sample source wells
    sample_sources = []
      ## Create an empty list to append wells to.                            ##
    sample_sources = sample_tubes_1.wells()
    if sample_racks >= 2:
        sample_sources = sample_sources + sample_tubes_2.wells()
    if sample_racks >= 3:
        sample_sources = sample_sources + sample_tubes_3.wells()    
    if sample_racks >= 4:
        sample_sources = sample_sources + sample_tubes_4.wells()
    sample_sources = sample_sources[:number_of_samples]
    
    # Destination wells
    sample_destinations = []
      ## Create an empty list to append wells to.                            ##
    if PCR_tubes == 'plate_96':
        sample_destinations = PCR_1.wells()
    elif PCR_tubes == 'PCR_strips':
        PCR_columns = (
            ([PCR_1.columns_by_name()[column_name]
            for column_name in strip_positions]))        
        if PCR_racks >= 2:
            PCR_columns_2 = (
            ([PCR_2.columns_by_name()[column_name]
              for column_name in strip_positions]))
            PCR_columns = PCR_columns + PCR_columns_2
        if PCR_racks >= 3:
            PCR_columns_3 = (
            ([PCR_3.columns_by_name()[column_name]
              for column_name in strip_positions]))
            PCR_columns = PCR_columns + PCR_columns_3
        for column in PCR_columns:
            for well in column:
                sample_destinations.append(well)
                
    sample_destinations = sample_destinations[:number_of_samples]

    ##### Tube locations                                                     ##
    MasterMix = tubes_5mL[mastermix_source]
      ## Location of the 5mL tube with mastermix                             ##
    water = tubes_5mL[water_tube]       
      ## Location of the 5mL tube with water                                 ##

## ALIQUOTING MASTERMIX========================================================
## ============================================================================
    for i, well in enumerate(sample_destinations):
      ## aliquot mix, for each well do the following:                       ##
        if i == 0: 
            p300.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    ##
        elif i % 16 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
              ## Then, after every 16th well, drop tip and pick up new       ##
    
        MM_current_height, pip_height, bottom_reached = vt.volume_tracking(
                'tube_5mL', dispension_vol, MM_current_height)
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

# ADDING SAMPLES AND WATER=====================================================
# =============================================================================
    ## Loop through source and destination wells
    for sample_tube, well, sample_vol in zip(
            sample_sources, sample_destinations, DNA_µL_list
            ):
        if sample_vol > 0:
            p20.pick_up_tip()
            p20.aspirate(sample_vol, sample_tube)
            p20.dispense(sample_vol, well)
            sample_mix_vol = sample_vol + 3
              ## mix_vol = volume for pipetting up and down                  ##
            p20.mix(3, sample_mix_vol, well)
            p20.dispense(10, well)
            p20.drop_tip()
        
        water_vol = max_DNA_volume - sample_vol
          ## volume of water needed to add a total of max_DNA_volume
        if water_vol > 0:
            
            w_current_height, pip_height, bottom_reached = vt.volume_tracking(
                    'tube_5mL', water_vol, w_current_height)
                   ## call volume_tracking function, obtain current_height,  ##
                   ## pip_height and whether bottom_reached.                 ##
            if bottom_reached:
                aspiration_location = water.bottom(z=1)
                protocol.comment("You've reached the bottom of the tube!")
                  ## If bottom is reached keep pipetting from bottom + 1     ##
            else:
                aspiration_location = water.bottom(pip_height)
                  ## Set the location of where to aspirate from.             ##
            
            p20.pick_up_tip()
            p20.aspirate(water_vol, aspiration_location)
            p20.dispense(water_vol, well)
            mix_vol = water_vol + 3
              ## mix_vol = volume for pipetting up and down                  ##
            p20.mix(3, mix_vol, well)
            p20.dispense(10, well)
            p20.drop_tip()
        
        
# =============================================================================
    