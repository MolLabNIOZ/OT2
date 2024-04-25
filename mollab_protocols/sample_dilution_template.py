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
sample_volume = [10,10,10 ]#<Sample_lists>
  ## Can be one volume or a list of volumes
  
water_volume = [10,10,10]#<Water_lists>
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
    # If water_volume >= 19µL use pp20 and p300, otherwise use p20 only
    #### Loading labware