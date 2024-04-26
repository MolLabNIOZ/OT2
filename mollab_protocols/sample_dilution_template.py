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
sample_volume = [50, 30, 5.0, 20, 10, 10, 50, 50, 10, 5.0, 10, 10, 5.0, 50, 50, 50, 20, 10, 20, 10, 40, 10, 50, 50, 10, 10, 10, 10, 20, 10, 5.0, 50, 30, 50, 30, 5.0, 10, 20, 50, 50, 50, 5.0, 10, 10, 10, 10, 10, 10, 30, 10, 20, 50, 10, 50, 10, 50, 10, 30, 10, 30, 20, 10, 50, 10, 20, 20, 20, 10, 50, 20, 10, 10, 20, 50, 20, 40, 40, 10, 50, 20, 30, 30, 20, 10, 10, 5.0, 50, 10, 5.0, 10, 40, 50, 10, 5.0, 30]#<Sample_lists>
  ## Can be one volume or a list of volumes
  
water_volume = [0.0, 36.11, 145.77, 41.17, 125.45, 149.64, 0.0, 0.0, 136.74, 139.32, 82.45, 137.81, 139.59, 0.0, 0.0, 0.0, 61.91, 167.37, 32.57, 86.75, 13.32, 124.37, 0.0, 0.0, 85.67, 105.02, 167.37, 104.49, 58.47, 49.12, 106.26, 0.0, 27.57, 0.0, 31.76, 147.38, 137.27, 43.32, 0.0, 0.0, 0.0, 151.41, 147.49, 119.0, 107.71, 78.15, 166.3, 106.1, 35.79, 123.84, 68.69, 0.0, 46.97, 0.0, 82.45, 0.0, 141.57, 22.08, 176.51, 34.02, 51.38, 50.2, 0.0, 52.89, 35.79, 40.41, 79.12, 158.24, 0.0, 37.73, 64.17, 132.97, 53.31, 0.0, 32.89, 19.98, 10.74, 72.24, 0.0, 35.79, 36.27, 37.56, 46.33, 55.04, 73.31, 109.22, 0.0, 157.7, 155.98, 153.4, 20.41, 0.0, 84.6, 194.41, 29.02]#<Water_lists>
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