# -*- coding: utf-8 -*-
"""
Version: V_July22_offsets

primer_dilution_plate.py is a protocol written to dilute (barcoded) primer
stocks. Primer stocks should be in PCR strips, dilutions are being made
in a PCR plate. Note that the plate needs to be sealed and than mixed
properly before usage!
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# If applicable: What is the starting position of the first 20µL tip?
starting_tip_p20 = 'A1'
# If applicable: What is the starting position of the first 200µL tip?
starting_tip_p200 = 'A1'
  ## If volume-wise p20 or p200 is not applicable, this variable won't be used

# How many samples do you want to dilute? 
number_of_primers = 96
  ## primer_tubes == 'PCR_strips', diltution_tubes == 'plate_96'     MAX = 192
  ###   = 4 primer PCR strip racks & 2 dilution plates
  ## primer_tubes == 'PCR_strips', dilution_tubes == 'PCR_strips'    MAX = 144
  ###   = 3 primer PCR strip racks & 3 dilution PCR strip racks
  
final_volume = 50
  ## How much primer dilution do you want to create?
  
primer_dilution_tubes = 'plate_96'
  ## Options: 'plate_96', 'PCR_strips'
# =============================================================================
 
# IMPORT STATEMENTS============================================================
# =============================================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
                                      
##### Import volume_tracking module 
# if not protocol.is_simulating(): 
#     from data.user_storage.mollab_modules import volume_tracking_v1 as vt
# else:
#     import json
#     from mollab_modules import volume_tracking_v1 as vt
                                          
# Import other modules
import math
  ## math to do some calculations (rounding up)  
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
primer_stock_volume = final_volume / 10
water_volume = final_volume - primer_stock_volume
total_water_volume = water_volume * number_of_primers

water_tubes = math.ceil((total_water_volume)/4800)
  ## How many tubes of 5mL water are needed 

primer_stock_racks = math.ceil(number_of_primers / 48)
  ## How many primer_racks are needed (1,2,3 or 4), primer_stock_racks are
  ## always PCR strips.
  
if primer_dilution_tubes == 'PCR_strips':
    primer_dilution_racks = math.ceil(number_of_primers / 48)
elif primer_dilution_tubes == 'plate_96':
    primer_dilution_racks = math.ceil(number_of_primers / 96)
  ## How many primer_dilution_racks are needed (1 or 2)

tips_20_needed = (len([x for x in water_volumes if x < 20]) +
                  len([x for x in sample_volumes if x <= 17]))
tips_200_needed = (len([x for x in water_volumes if x >= 20]) +
                   len([x for x in sample_volumes if x > 17]))
## How many p20 / p200 tips do you need?