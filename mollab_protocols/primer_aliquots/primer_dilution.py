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
  ## primer_tubes == 'PCR_strips', primer_diltution_tubes == 'plate_96'  MAX = 192
  ###   = 4 primer PCR strip racks & 2 dilution plates
  ## primer_tubes == 'PCR_strips', primer_primer_dilution_tubes == 'PCR_strips' MAX = 144
  ###   = 3 primer PCR strip racks & 3 dilution PCR strip racks
  
final_volume = 50
  ## How much primer dilution do you want to create?
  
primer_primer_dilution_tubes = 'plate_96'
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

# tips_20_needed = (len([x for x in water_volumes if x < 20]) +
#                   len([x for x in sample_volumes if x <= 17]))
# tips_200_needed = (len([x for x in water_volumes if x >= 20]) +
#                    len([x for x in sample_volumes if x > 17]))
# ## How many p20 / p200 tips do you need?
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'primer_dilution.py',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Primer dilution protocol.'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Dilute primers in fixed volumes - the protocol is originally designed
    for the dilution of many (barcoded) primers.
    """
    # IMPORT for simulator
    if not protocol.is_simulating(): 
        from data.user_storage.mollab_modules import volume_tracking_v1 as vt
    else:
        import json
        from mollab_modules import volume_tracking_v1 as vt
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    labwares = {}
    # Pipette tips
    if dispension_vol >= 19:
      ## When the mm volume to be dispensed >= 19, 200µL tips are          
      ## needed in addition to the 20µL tips.                              
        tips_200 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', 
            4,                                  
            '200tips')   
        labwares[tips_200] = 'filtertips_200'                       
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            7,                                  
            '20tips_1')           
        labwares[tips_20_1] = 'filtertips_20'                     
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            10,                                 
            '20tips_2')               
        labwares[tips_20_2] = 'filtertips_20'          
        tips_20 = [tips_20_1, tips_20_2]
    else:
      ## When the mm volume to be dispensed <=19, only 20µL are needed      
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            4,                                  
            '20tips_1')        
        labwares[tips_20_1] = 'filtertips_20'                   
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            7,                                  
            '20tips_2')    
        labwares[tips_20_2] = 'filtertips_20'                       
        tips_20_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            10,                                 
            '20tips_3')           
        labwares[tips_20_3] = 'filtertips_20'                  
        tips_20 = [tips_20_1, tips_20_2, tips_20_3]
        
   # Pipettes
   if dispension_vol >= 19:
       p300 = protocol.load_instrument(
           'p300_single_gen2',             
           'right',                        
           tip_racks=[tips_200])           
   p20 = protocol.load_instrument(
       'p20_single_gen2',                  
       'left',                             
       tip_racks=tips_20)
    
    # Labware
    if primer_dilution_tubes == 'plate_96':
        if primer_primer_dilution_racks >= 1:        
            primer_dilution_dest_1 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                6,
                'primer_dilution_dest_1')
        if primer_dilution_racks >= 2:            
            primer_dilution_dest_2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                3,
                'primer_dilution_dest_2')
        if primer_dilution_racks >= 3:             
            primer_dilution_dest_3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                5,
                'primer_dilution_dest_3')
    
    if not protocol.is_simulating():
        if primer_tubes == 'PCR_strips':
            if primer_racks >= 1:
                primer_source_1 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    1,                                      
                    'primer_source_1')                      
            if primer_racks >= 2:
                primer_source_2 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    4,                                      
                    'primer_source_2')                      
            if primer_racks >= 3:   
                primer_source_3 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    2,                                      
                    'primer_source_3')                      
            if primer_racks >= 4: 
                primer_source_4 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    5,                                      
                    'primer_source_4')                      
        if primer_dilution_tubes == 'PCR_strips':
            if primer_dilution_racks >= 1:
                primer_dilution_dest_1 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    3,                                      
                    'primer_dilution_dest_1')                      
            if primer_dilution_racks >= 2:
                primer_dilution_dest_2 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    6,                                      
                    'primer_dilution_dest_2')                      
            if primer_dilution_racks >= 3:    
                primer_dilution_dest_3 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    5,                                      
                    'primer_dilution_dest_3')                      
            if primer_dilution_racks >= 4:        
                primer_dilution_dest_4 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    2,                                      
                    'primer_dilution_dest_4')                          
        if water_tubes > 0:
            tubes_5mL = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',     
                9,                                          
                'tubes_5mL')  
            
    else:
        with open("labware/pcrstrips_96_wellplate_200ul/"
                  "pcrstrips_96_wellplate_200ul.json") as labware_file:
                labware_def_pcrstrips = json.load(labware_file)
        if primer_tubes == 'PCR_strips':
            if primer_racks >= 1:
                primer_source_1 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    1,                     
                    'primer_source_1')     
            if primer_racks >= 2:
                primer_source_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    4,                     
                    'primer_source_2')     
            if primer_racks >= 3:
                primer_source_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    2,                     
                    'primer_source_3')     
            if primer_racks >= 4:
                primer_source_4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    5,                     
                    'primer_source_4')     
        if primer_dilution_tubes == 'PCR_strips':
            if primer_dilution_racks >= 1:
                primer_dilution_dest_1 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    3,                     
                    'primer_dilution_dest_1')     
            if primer_dilution_racks >= 2:
                primer_dilution_dest_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    6,                     
                    'primer_dilution_dest_2')     
            if primer_dilution_racks >= 3:
                primer_dilution_dest_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    5,                     
                    'primer_dilution_dest_3')     
            if primer_dilution_racks >= 4:
                primer_dilution_dest_4 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    2,                     
                    'primer_dilution_dest_4')       
        if water_tubes > 0: 
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                      "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                    labware_def_5mL = json.load(labware_file)
            tubes_5mL = protocol.load_labware_from_definition( 
                labware_def_5mL, 
                9, 
                '5mL_tubes')    
# =============================================================================