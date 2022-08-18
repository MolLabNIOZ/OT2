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

# How many primers do you want to dilute? 
number_of_primers = 96
  ## primer_diltution_tubes == 'plate_96'  MAX = 192
  ###   = 4 primer PCR strip racks & 2 dilution plates
  ## primer_dilution_tubes == 'PCR_strips' MAX = 144
  ###   = 3 primer PCR strip racks & 3 dilution PCR strip racks
  
final_volume = 50
  ## How much primer dilution do you want to create?
  ## Advised: a minimum of 20µL and a maximum of 60µL
  
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

number_of_water_tubes = math.ceil((total_water_volume)/4800)
  ## How many tubes of 5mL water are needed 

primer_stock_racks = math.ceil(number_of_primers / 48)
  ## How many primer_racks are needed (1,2,3 or 4), primer_stock_racks are
  ## always PCR strips.
  
if primer_dilution_tubes == 'PCR_strips':
    primer_dilution_racks = math.ceil(number_of_primers / 48)
elif primer_dilution_tubes == 'plate_96':
    primer_dilution_racks = math.ceil(number_of_primers / 96)
  ## How many primer_dilution_racks are needed (1 or 2)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'primer_dilution.py',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('A protocol for the 10x dilution of many primers.'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Dilute primers 10x - a protocol for the dilution of many primers
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
    if water_volume >= 19:
      ## When the volume to be dispensed >= 19, 200µL tips are          
      ## needed in addition to the 20µL tips.                              
        tips_200 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', 
            10,                                  
            '200tips')   
        labwares[tips_200] = 'filtertips_200'                       
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            7,                                  
            '20tips_1')           
        labwares[tips_20_1] = 'filtertips_20'                     
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            4,                                 
            '20tips_2')               
        labwares[tips_20_2] = 'filtertips_20'          
        tips_20 = [tips_20_1, tips_20_2]
    else:
      ## When the mm volume to be dispensed <=19, only 20µL are needed      
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            10,                                  
            '20tips_1')        
        labwares[tips_20_1] = 'filtertips_20'                   
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            7,                                  
            '20tips_2')    
        labwares[tips_20_2] = 'filtertips_20'                       
        tips_20_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            4,                                 
            '20tips_3')           
        labwares[tips_20_3] = 'filtertips_20'                  
        tips_20 = [tips_20_1, tips_20_2, tips_20_3]
        
    # Pipettes
    if total_water_volume >= 19:
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
        if primer_dilution_racks >= 1:        
            primer_dilution_dest_1 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                6,
                'primer_dilution_dest_1')
        if primer_dilution_racks >= 2:            
            primer_dilution_dest_2 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                3,
                'primer_dilution_dest_2')
    
    if not protocol.is_simulating():
        if primer_stock_racks >= 1:
            primer_source_1 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                8,                                      
                'primer_source_1')                      
        if primer_stock_racks >= 2:
            primer_source_2 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                5,                                      
                'primer_source_2')                      
        if primer_stock_racks >= 3:   
            primer_source_3 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                2,                                      
                'primer_source_3')                      
        if primer_stock_racks >= 4: 
            primer_source_4 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                1,                                      
                'primer_source_4')                      
        if primer_dilution_tubes == 'PCR_strips':
            if primer_dilution_racks >= 1:
                primer_dilution_dest_1 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    9,                                      
                    'primer_dilution_dest_1')                      
            if primer_dilution_racks >= 2:
                primer_dilution_dest_2 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    6,                                      
                    'primer_dilution_dest_2')                      
            if primer_dilution_racks >= 3:    
                primer_dilution_dest_3 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',         
                    3,                                      
                    'primer_dilution_dest_3')                                               
        water_tubes = protocol.load_labware(
            'eppendorfscrewcap_15_tuberack_5000ul',     
            11,                                          
            'water_tubes')  
            
    else:
        with open("labware/pcrstrips_96_wellplate_200ul/"
                  "pcrstrips_96_wellplate_200ul.json") as labware_file:
                labware_def_pcrstrips = json.load(labware_file)
        if primer_stock_racks >= 1:
            primer_source_1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, 
                8,                     
                'primer_source_1')     
        if primer_stock_racks >= 2:
            primer_source_2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, 
                5,                     
                'primer_source_2')     
        if primer_stock_racks >= 3:
            primer_source_3 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, 
                2,                     
                'primer_source_3')     
        if primer_stock_racks >= 4:
            primer_source_4 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, 
                1,                     
                'primer_source_4')     
        if primer_dilution_tubes == 'PCR_strips':
            if primer_dilution_racks >= 1:
                primer_dilution_dest_1 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    9,                     
                    'primer_dilution_dest_1')     
            if primer_dilution_racks >= 2:
                primer_dilution_dest_2 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    6,                     
                    'primer_dilution_dest_2')     
            if primer_dilution_racks >= 3:
                primer_dilution_dest_3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips, 
                    3,                     
                    'primer_dilution_dest_3')        
        with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                  "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                labware_def_5mL = json.load(labware_file)
        water_tubes = protocol.load_labware_from_definition( 
            labware_def_5mL, 
            9, 
            'water_tubes')    
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    # Setting starting tip                                           
    if water_volume >= 19:
        ## If the mm volume to be dispendsed >= 19, assign p300 starting tip
        p300.starting_tip = tips_200.well(starting_tip_p200)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
    
    # Create an empty list to append the wells for the water source to
    water_sources = []
    # Append well locations of water tubes, depending on how many water tubes
    for well in water_tubes.wells():
        water_sources.append(well)
    water_sources = water_sources[:number_of_water_tubes]
    # if water_tubes == 1:
    #     water_wells = water_tubes.wells_by_name()['A1']
    #     water_sources.append(water_wells)
    # if water_tubes == 2:
    #     water_wells = water_tubes.wells_by_name()['A1', 'B1']
    #     water_sources.append(water_wells)
    # if water_tubes == 3:
    #     water_wells = water_tubes.wells_by_name()['A1', 'B1', 'C1']
    #     water_sources.append(water_wells)
    # if water_tubes == 4:
    #     water_wells = water_tubes.wells_by_name()['A1', 'B1', 'C1', 'D1']
    #     water_sources.append(water_wells)
        
    # Create an empty list to append the wells for the primer stock source to
    primer_stock_sources = []
    # First make a list with columns of primer sources
    primer_stock_columns = (
        ([primer_source_1.columns_by_name()[column_name] 
          for column_name in ['1', '3', '5', '7', '9', '11']]))
    if primer_stock_racks >= 2:
        primer_stock_columns_2 = (
            ([primer_source_2.columns_by_name()[column_name] 
              for column_name in ['1', '3', '5', '7', '9', '11']]))
        for column in primer_stock_columns_2:
            primer_stock_columns.append(column)
    if primer_stock_racks >= 3:
        primer_stock_columns_3 = (
            ([primer_source_3.columns_by_name()[column_name] 
              for column_name in ['1', '3', '5', '7', '9', '11']]))
        for column in primer_stock_columns_3:
            primer_stock_columns.append*(column)
    if primer_stock_racks >= 4:
        primer_stock_columns_4 = (
            ([primer_source_4.columns_by_name()[column_name] 
              for column_name in ['1', '3', '5', '7', '9', '11']]))
        for column in primer_stock_columns_4:
            primer_stock_columns.append*(column)
    # Separate columns into wells and add wells to list of primer stock sources
    for column in primer_stock_columns:
        for well in column:
            primer_stock_sources.append(well)
    primer_stock_sources = primer_stock_sources[:number_of_primers]  
      
    # Create an empty list to append the wells for the primer dilutions to
    primer_dilution_wells = []
    # Add wells to the list of primer dilution wells, if plate_96
    if primer_dilution_tubes == 'plate_96':
        if primer_dilution_racks >= 1:
            for well in primer_dilution_dest_1.wells():
                primer_dilution_wells.append(well)
        if primer_dilution_racks >= 2:
            for well in primer_dilution_dest_2.wells():
                primer_dilution_wells.append(well)
        if primer_dilution_racks >= 3:
            for well in primer_dilution_dest_3.wells():
                primer_dilution_wells.append(well)
    # Make a list of primer dilution columns, if PCR strips            
    if primer_dilution_tubes == 'PCR_strips':
        primer_dilution_columns = (
            ([primer_dilution_dest_1.columns_by_name()[column_name] 
              for column_name in ['1', '3', '5', '7', '9', '11']]))
        if primer_dilution_racks >= 2:
            primer_dilution_columns_2 = (
                ([primer_dilution_dest_2.columns_by_name()[column_name] 
                  for column_name in ['1', '3', '5', '7', '9', '11']]))
            for column in primer_dilution_columns_2:
                primer_dilution_columns.append(column)
        if primer_dilution_racks >= 3:
            primer_dilution_columns_3 = (
                ([primer_dilution_dest_3.columns_by_name()[column_name] 
                  for column_name in ['1', '3', '5', '7', '9', '11']]))
            for column in primer_dilution_columns_3:
                primer_dilution_columns.append(column)
    # Separate columns into wells and add wells to list of primer dilution wells
        for column in primer_dilution_columns:
            for well in column:
                primer_dilution_wells.append()
    primer_dilution_wells = primer_dilution_wells[:number_of_primers]
# =============================================================================      


# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.pause("I need "+ str(number_of_water_tubes) + " 15mL tubes. Filled to "
                   + str(water_volume/1000) + " mL with reagent.") 
# ============================================================================= 
 
## LIGHTS======================================================================
## ============================================================================

    protocol.set_rail_lights(True)
## ============================================================================


## PIPETTING===================================================================
## ============================================================================
# Variables for volume tracking and aliquoting---------------------------------
    counter = 0
    source = water_sources[counter]
    destination = primer_dilution_wells
    start_height = vt.cal_start_height('tube_5mL', water_volume)
    current_height = start_height
    container = 'tube_5mL'
    if water_volume >= 19:
        pipette = p300
    else:
        pipette = p20 
# ----------------------------------------------------------------------------- 
       
    ##### aliquoting
    for i, well in enumerate(destination):
      ## aliquot in the correct wells, for each well do the following:  
        if i == 0: 
            pipette.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    
        elif i % 24 == 0:
            pipette.drop_tip()
            pipette.pick_up_tip()
              ## Then, after every 24th well, drop tip and pick up new      
        
        current_height, pip_height, bottom_reached = vt.volume_tracking(
            container, water_volume, current_height)
              ## call volume_tracking function, obtain current_height,      
              ## pip_height and whether bottom_reached.                     
        
        if bottom_reached:
            ## continue with next tube, reset vt                            
            current_height = start_height
            current_height, pip_height, bottom_reached = (
                vt.volume_tracking(
                    container, water_volume, current_height))
            counter = counter + 1
            source = water_sources[counter]
            aspiration_location = source.bottom(current_height)
            protocol.comment(
            "Continue with tube " + str(counter + 1) + " of reagent")
       
        else:
            aspiration_location = source.bottom(pip_height)
              ## Set the location of where to aspirate from.                
        
        #### The actual aliquoting
        pipette.aspirate(water_volume, aspiration_location)
          ## Aspirate the set volume from the source                        
        pipette.dispense(water_volume + 10, well)
          ## dispense the set volume + extra to avoid drops in the well     
        pipette.dispense(10, aspiration_location)
          ## Alternative for blow-out                                        
    pipette.drop_tip()
      ## when entire plate is full, drop tip                               
## ----------------------------------------------------------------------------        
            
                
    