"""
VERSION: V_May22
pooling_replicates.py is a protocol for pooling replicate PCR reactions.
It takes PCR product from 2 different locations and pools it in a third 
location.
This protocol assumes the 3 PCRs are done in 3PCR plates, and the placement of 
samples is the exact same for all 3 plates.
It is however possible to skip certain reactions.

You have to provide:
    Location of the starting tip in P20 or P200 (depending on the PCR
        reaction volume x 2)
    Location of first sample in the plate
    Location of last sample in the plate
    List with specific sample locations to skip
    PCR reaction volume
    Number of replicates
    
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the tips?
starting_tip = 'A1'
  ## Either p20 or p200. 
  ## You need the tips that fit PCR reaction volume x (number of replicates -1)
  ## + 1µL extra per (number of replicate -1)

# What is the location of the first and last sample you want to pool
first_sample_well = 'A1'
  ## If you want to skip the first couple of samples, please indicate the 
  ## location in the plates of the first sample you want to pool.
last_sample_well = 'H12'
  ## If you want to skip the last couple of samples, or your PCR plates are not 
  ## completely filled, please indicate the location in the plates of the last
  ## sample you want to pool.

# Are there any wells between the first and last sample that need to be skipped
skipp_samples = True
if skipp_samples:
    skipped_wells = (
        ['D1', 'G5'])
    ## Fill in the wells that need to be skipped while pooling
    
# What is the PCR reaction_volume (per reaction)?
reaction_volume = 25

# How many replicates do you have?
replicates = 3
  ## How many reactions do you want to pool, including the original PCR?
  ## For now 3 is max. If you want more, protocol needs to be adjusted

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
if simulate: #Simulator
    import json

# CALCULATED VARIABLES=========================================================
# =============================================================================
# What volume needs to be aspirated (all replicates combined + airgaps)
transfer_volume = (reaction_volume * (replicates -1)) + (replicates -1)

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


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'pooling_replicates.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('pooling replicates after replicate PCRs in plates'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix;
    Adding samples from different labware.
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    labwares = {}
      ## empty dict to add labware and labware_names to, to loop through

      
    ##### Loading pipettetips
    if transfer_volume >= 20:
        tips = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  
            11,                                  
            '200tips')
        labwares[tips] = 'tips_200'
    else:
        tips = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            11,                                 
            '20tips')
        labwares[tips] = 'tips_20'
    
    ##### Loading labware
    if simulate: #Simulator
        with open("labware/biorad_qpcr_plate_nioz_plateholder/"
             "biorad_qpcr_plate_nioz_plateholder.json") as labware_file:
                  labware_def_plate_nioz_plateholder = json.load(labware_file)
        PCR1 = protocol.load_labware_from_definition( 
            labware_def_plate_nioz_plateholder,           
            9,                         
            'PCR1')
        PCR2 = protocol.load_labware_from_definition( 
            labware_def_plate_nioz_plateholder,           
            8,                         
            'PCR2')
        if replicates > 2:
            PCR3 = protocol.load_labware_from_definition( 
                labware_def_plate_nioz_plateholder,           
                7,                         
                'PCR3')
            
    else:
        PCR1 = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',
            9,
            'PCR1')
        labwares[PCR1] = 'plate_plateholder'

        PCR2 = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',
            8,
            'PCR2')
        labwares[PCR2] = 'plate_plateholder'
        if replicates > 2:
            PCR3 = protocol.load_labware(
                'biorad_qpcr_plate_nioz_plateholder',
                7,
                'PCR3')
            labwares[PCR3] = 'plate_plateholder'

    ##### Loading pipettes
    if transfer_volume >= 20:
        pipette = protocol.load_instrument(
            'p300_single_gen2',             
            'right',                        
            tip_racks=tips)
    else:
        pipette = protocol.load_instrument(
            'p20_single_gen2',                  
            'left',                             
            tip_racks=tips)    
# =============================================================================

# LABWARE OFFSET===============================================================    
# =============================================================================
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
    pipette.starting_tip = tips.well(starting_tip)
    
    # Make lists of all wells that should be skipped in the pooling
    PCR1_skipped_wells = (
        [PCR1.wells_by_name()[well_name] for well_name in
        skipped_wells])
    PCR2_skipped_wells = (
        [PCR2.wells_by_name()[well_name] for well_name in
        skipped_wells])
    if PCR3:
        PCR3_skipped_wells = (
            [PCR3.wells_by_name()[well_name] for well_name in
            skipped_wells])

    # Make lists of wells that should be included in the pooling
    PCR1_wells = PCR1.wells()
      ## Make a list of all wells
    for well in PCR1_skipped_wells:
        PCR1_wells.remove(well)
      ## remove wells to skip from the list
    PCR2_wells = PCR1.wells()
    for well in PCR2_skipped_wells:
        PCR2_wells.remove(well)
    if PCR3:
        PCR3_wells = PCR3.wells()
        for well in PCR3_skipped_wells:
            PCR3_wells.remove(well)
# =============================================================================


## PIPETTING===================================================================
## ============================================================================
    # Turn on lights    
    protocol.set_rail_lights(True)
    
    if replicates == 2:
        for well_PCR2, well_PCR1 in zip(PCR2_wells, PCR1_wells):
            pipette.pick_up_tip()
            pipette.aspirate(transfer_volume, well_PCR2)
            pipette.dispense(transfer_volume, well_PCR1)
            pipette.dispense(10, well_PCR1)
            pipette.drop_tip()
    
    if replicates == 3:
        for well_PCR3, well_PCR2, well_PCR1 in zip(
                PCR3_wells, PCR2_wells, PCR1_wells):
            pipette.pick_up_tip()
            pipette.aspirate(reaction_volume + 1, well_PCR3)
            pipette.aspirate(reaction_volume + 1, well_PCR2)
            pipette.dispense(transfer_volume, well_PCR1)
            pipette.dispense(10, well_PCR1)
            pipette.drop_tip()        

    # Turn off lights
    protocol.set_rail_lights(False)

    
    
    
    
    