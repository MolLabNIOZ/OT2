# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 09:45:27 2024

@author: rdebeer
"""
# What is the starting position of the tips?
starting_tip_p20 = 'C8'
starting_tip_p300 = 'B2'

# Use get_uL_info.py to get a list of volumes
DNA_µL_list = <DNA_volumes> 

# Do you want to simulate the protocol?
simulate = False
  ## True for simulating protocol, False for robot protocol
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
                                      
##### Import volume_tracking module 
if simulate:
    import json
    
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW         
                                 
# Import other modules
import math
  ## math to do some calculations (rounding up)
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
# Calculate the total pool volume
total_pool_volume = sum(DNA_µL_list)

# calculate total_pool_volume + buffer to add for clean-up 
# to determine what kind of tube to use
PB_volume = total_pool_volume * 5
total_cleanup_volume = total_pool_volume + PB_volume

# Calculates in what tube type you need to pool everything
reagent_tube_type, number_of_tubes, max_volume = LW.which_tube_type(total_volume = total_cleanup_volume,
                                                                    tube_type = False)

# Calculates how many tips you need for pipetting all the water volumes
p20_tips_needed, p300_tips_needed =  LW.amount_of_tips(volumes = DNA_µL_list,
                                                       number_of_transfers = False,
                                                       tip_change = 1,
                                                       max_p20_volume = 15)

# Calculates how many pipette boxes you need by using the function 'number_of_tipracks'
amount_p20_tipracks = LW.number_of_tipracks(starting_tip = starting_tip_p20,
                                     tips_needed = p20_tips_needed)
amount_p300_tipracks = LW.number_of_tipracks(starting_tip = starting_tip_p300,
                                     tips_needed = p300_tips_needed)

# Checks whether or not you need the P20 and/or P300 and sets them to false if you dont need them
if amount_p20_tipracks == 0:
    P20 = False
else:
    P20 = True
if amount_p300_tipracks == 0:
    P300 = False
else:
    P300 = True
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'equimolar_pooling.py',
    'author': 'MolLab <molecular.ecology@nioz.nl>',
    'description': ('pooling samples in equimolar amounts'),
    'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):
    """
    pool samples together in different volumes
    """
# =============================================================================
## LIGHTS & COMMENT------------------------------------------------------------
    protocol.set_rail_lights(True)
    protocol.comment(f"You need {PB_volume} μl PB buffer in a {reagent_tube_type}")
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    # Loading p20 tips
    tips_20 = LW.loading_tips(simulate = simulate, 
                     tip_type = 'tipone_20uL', 
                     amount = amount_p20_tipracks, 
                     deck_positions = [0], 
                     protocol = protocol)
    
    # Loading p300 tips
    tips_300 = LW.loading_tips(simulate = simulate,
                              tip_type = 'opentrons_200uL',
                              amount = amount_p300_tipracks,
                              deck_positions = [0],
                              protocol = protocol)
    
    ### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20 = P20, 
                                    tips_20 = tips_20,
                                    starting_tip_p20 = starting_tip_p20,
                                    P300 = P300, 
                                    tips_300 = tips_300,
                                    starting_tip_p300 = starting_tip_p300,
                                    protocol = protocol)
    #### Loading labware
    # Loading source plate
    source_plate = LW.loading_tube_racks(simulate = simulate,
                                        tube_type = 'plate_96_NIOZholder',
                                        reagent_type = 'source_plate',
                                        amount = 1,
                                        deck_positions = [0],
                                        protocol = protocol)
    # Loading destination tube rack
    destination_rack = LW.loading_tube_racks (simulate = simulate, 
                                              tube_type = reagent_tube_type, 
                                              reagent_type = 'PB-buffer', 
                                              amount = 1, 
                                              deck_positions = [0], 
                                              protocol = protocol)
    
    # Spefifying location of the destination tube
    destination_tube = LW.tube_locations(source_racks = destination_rack,
                                   specific_columns = False,
                                   skip_wells = False,
                                   number_of_tubes = 1)
    ## ========================================================================

    ## PIPETTING===============================================================
    ## ========================================================================
    # Settings for transfering the sample volumes in the destination plate
    PM.transferring_varying_volumes(source_wells = source_plate.wells(),
                                    destination_wells = destination_tube,
                                    transfer_volumes = DNA_µL_list,
                                    airgap = True,
                                    mix = True,
                                    p20 = p20,
                                    p300 = p300,
                                    protocol = protocol)
## LIGHTS & COMMENT------------------------------------------------------------
    protocol.set_rail_lights(False)