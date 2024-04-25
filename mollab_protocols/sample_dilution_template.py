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
starting_tip_p200 = 'C11'
  ## If volume-wise p20 or p200 is not applicable, this variable won't be used

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

# Calculates how many tips you need for this protocol
p20_tips_needed = 0

for value in water_volume: 
    if 0 < value < 19:
        p20_tips_needed += 1
    else: pass 

# Calculates how many pipette boxes you need by using the function 'pipette_boxes'
amount_tip_racks_p20, amount_tip_racks_p200 = LW.pipette_boxes(starting_tip_p20,
                  starting_tip_p200,
                  tips_needed_p20,
                  tips_needed_p200)
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
# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    # If water_volume >= 19µL use p20 and p300, otherwise use p20 only
    #### Loading labware
    