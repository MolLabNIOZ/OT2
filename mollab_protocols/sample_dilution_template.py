# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:42:59 2024

@author: rdebeer
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# If applicable: What is the starting position of the first 20µL tip?
starting_tip_p20 = 'H1'
# If applicable: What is the starting position of the first 200µL tip?
starting_tip_p300 = 'C11'
  ## If volume-wise p20 or p300 is not applicable, this variable won't be used

#How much sample volume (µL) do you want to use for the dilution?
sample_volume = #<Sample_lists>
  ## Can be one volume or a list of volumes
  
water_volume = #<Water_lists>
  # Can be one volume or a list of volumes.

simulate = False
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
total_water = sum(water_volume)
# Calculates in what tube type the water needs to go
reagent_tube_type, number_of_tubes, max_volume = LW.which_tube_type(total_volume = total_water,
                                                                tube_type = False)

# Calculates how many tips you need for pipetting all the sample volumes
p20_tips_sample, p300_tips_sample = LW.amount_of_tips(volumes = sample_volume,
                                                      number_of_transfers = False,
                                                      tip_change = 1,
                                                      max_p20_volume = 15)
# Calculates how many tips you need for pipetting all the water volumes
p20_tips_water, p300_tips_water = LW.amount_of_tips(volumes = water_volume,
                                                    number_of_transfers = False,
                                                    tip_change = 16,
                                                    max_p20_volume = 19)
# Calculates how many tips you need by adding the sample tips with the water tips
p20_tips_needed = p20_tips_sample + p20_tips_water
p300_tips_needed = p300_tips_sample + p300_tips_water

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
    'protocolName': 'sample_dilution.py',
    'author': 'MolLab <molecular.ecology@nioz.nl>',
    'description': ('Sample dilution or tranfer protocol.'),
    'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Dilute samples in a fixed or varying rates 
    or transfer samples to different tubes.
    """

# =============================================================================
## LIGHTS & COMMENT------------------------------------------------------------
    protocol.set_rail_lights(True)
    protocol.comment(f"You need {total_water} μl in a {reagent_tube_type}")
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
    # Loading water tube rack
    water_rack = LW.loading_tube_racks (simulate = simulate, 
                                        tube_type = reagent_tube_type, 
                                        reagent_type = 'Water', 
                                        amount = 1, 
                                        deck_positions = [0], 
                                        protocol = protocol)
    
    # Spefifying location of the water tube
    water_tube = LW.tube_locations(source_racks = water_rack,
                                   specific_columns = False,
                                   skip_wells = False,
                                   number_of_tubes = 1)
    
    # Loading source plate
    source_plate = LW.loading_tube_racks(simulate = simulate,
                                        tube_type = 'plate_96_NIOZholder',
                                        reagent_type = 'source_plate',
                                        amount = 1,
                                        deck_positions = [0],
                                        protocol = protocol)
    
    # Loading destination plate
    destination_plate = LW.loading_tube_racks(simulate = simulate,
                                              tube_type = 'plate_96_NIOZholder',
                                              reagent_type = 'destination_plate',
                                              amount = 1,
                                              deck_positions = [0],
                                              protocol = protocol)
    
    ## ========================================================================

    ## PIPETTING===============================================================
    ## ========================================================================
    # Settings for aliquoting of the water volumes in the destination plate
    PM.aliquoting_varying_volumes(reagent_source = water_rack, 
                                   reagent_tube_type = reagent_tube_type, 
                                   reagent_startvolume = total_water,
                                   aliquot_volumes = water_volume,
                                   destination_wells = destination_plate.wells(),
                                   p20 = p20,
                                   p300 = p300,
                                   tip_change = 16,
                                   action_at_bottom = 'continue_at_bottom',
                                   pause = False,
                                   protocol = protocol)
    
    # Settings for transfering the sample volumes in the destination plate
    PM.transferring_varying_volumes(source_wells = source_plate.wells(),
                                    destination_wells = destination_plate.wells(),
                                    transfer_volumes = sample_volume,
                                    airgap = True,
                                    mix = True,
                                    p20 = p20,
                                    p300 = p300,
                                    protocol = protocol)
## LIGHTS & COMMENT------------------------------------------------------------
    protocol.set_rail_lights(False)