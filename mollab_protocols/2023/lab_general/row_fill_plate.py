"""
This protocol transfers a desired volume of sample from 1.5mL tubes to a 96
wells plate.
The plate will be filled up by row, not the default by column.

updates:
    231113 MB: 
    added option of orientation how to fill the destination_plate
"""
##=============================================================================
#VARIABLES TO SET!!!
##=============================================================================
# Enter the number of samples 
number_of_samples = 24
# Enter the volume of the sample you want transferred
volume_of_sample = 40                
# Enter the starting tip of either the p20 (volume <= 18) or p200 tips
starting_tip = 'G8'
# Do you want to fill the plate per row or column?
pipetting_direction = 'by_column'
# Options: 'by_column' or 'by_row'
# Are you simulating the protocol?
simulate = False            
##=============================================================================

##=============================================================================
# IMPORT STATEMENTS
#==============================================================================
# Import opentrons protocol API v2
from opentrons import protocol_api

# Import other modules
import math #to do some calculations (rounding up)

# For custom labware, we need json while simulating
if simulate: #Simulator
    import json 
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.
##=============================================================================

##=============================================================================
# CALCULATED VARIABLE
##=============================================================================
# Calculating how many sample racks are needed
sample_racks = math.ceil(number_of_samples/24)

# Determine how much volume to use as airgap
if volume_of_sample <= 18:
    airgap = 2
else:
    airgap = 10
##=============================================================================

##=============================================================================
# METADATA
##=============================================================================
metadata = {
    'protocolName': 'row_fill_plate.py',
    'author': 'RB <rob.de.beer@nioz.nl>',
    'description': ('transfering samples to plate, per row of the plate'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    transfering samples from 1.5ml tubes to a PCR-plate.
    The PCR plate will be filled per row (instead of the default per column)
    """
##=============================================================================

##=============================================================================
# LOADING LABWARE AND PIPETTES
##=============================================================================
    # Loading labware - pipettetips
    if volume_of_sample > 18:
        # If you have a volume > 18, load 200µL tips
        tips_1 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',  
                11,                                  
                '200tips_1')
        tips_2 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',  
                10,                                  
                '200tips_2')
    else:
        # If you have a volume <= 18, load 20µL tips (2µL airgap)
        if simulate:
            with open("labware/tipone_96_tiprack_20ul/"
                      "tipone_96_tiprack_20ul.json") as labware_file:
                    labware_def_tipone_96_tiprack_20ul = json.load(labware_file)
            tips_1 = protocol.load_labware_from_definition(
                     labware_def_tipone_96_tiprack_20ul,
                     11,                                  
                     'tipone_20tips_1')
            tips_2 = protocol.load_labware_from_definition(
                     labware_def_tipone_96_tiprack_20ul,
                     10,                                  
                     'tipone_20tips_2')
        else:
            tips_1 = protocol.load_labware(
                    'tipone_96_tiprack_20ul',  
                    11,                                  
                    'tipone_20tips_1')
            tips_2 = protocol.load_labware(
                    'tipone_96_tiprack_20ul',  
                    10,                                  
                    'tipone_20tips_2')
   
    # Loading labware - destination plate
    destination = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                6,
                'destination_plate_96')
    
    # Loading labware - source
    sample_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        5,                                                       
        'sample_tubes_1')                                        
    if sample_racks >= 2:
        sample_tubes_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            8,                                                       
            'sample_tubes_2')                                        
        if sample_racks >= 3:
            sample_tubes_3 = protocol.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                4,                                                       
                'sample_tubes_3')                                        
            if sample_racks >= 4:
                sample_tubes_4 = protocol.load_labware(
                    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
                    7,                                                      
                    'sample_tubes_4')
    
    # Loading pipettes
    if volume_of_sample >= 18:
        pipette = protocol.load_instrument(
            'p300_single_gen2',             
            'right',                        
            tip_racks=[tips_1, tips_2])
    else:
        pipette = protocol.load_instrument(
            'p20_single_gen2',                  
            'left',                             
            tip_racks=[tips_1, tips_2])      
##=============================================================================
      
##=============================================================================
# SETTING LOCATIONS============================================================
##=============================================================================
    #### Setting starting tip
    pipette.starting_tip = tips_1.well(starting_tip)     
    
    #### Setting tube locations
    # Destination wells 
    if pipetting_direction == 'by_column':
        destination_wells = destination.wells()
    else:
        destination_wells = []
        destination_rows = destination.rows_by_name()
        for row, row_wells in destination_rows.items():
            destination_wells = destination_wells + row_wells
        # We want the robot to loop through the wells horizontally (by row) instead
        # of the default (by column).
    destination_wells = destination_wells[:number_of_samples]
    ## cuts off the list after certain number of samples 
    
    # Source wells
    source_wells = [] 
    source_wells = source_wells + sample_tubes_1.wells()
    if sample_racks >= 2:
        source_wells = source_wells + sample_tubes_2.wells()
        if sample_racks >= 3:
            source_wells = source_wells + sample_tubes_3.wells()
            if sample_racks >= 4:
                source_wells = source_wells + sample_tubes_4.wells()               
    source_wells = source_wells[:number_of_samples]
    ## cuts off the list after certain number of samples 
##=============================================================================

##=============================================================================
# Transferring=================================================================
##=============================================================================
    # Turn on light when starting
    protocol.set_rail_lights(True)    
    
    # Set a lower flow rate, so the entire sample is taken up
    if volume_of_sample > 18: 
        pipette.flow_rate.aspirate = 30
        pipette.flow_rate.dispense = 30
    else:
        pipette.flow_rate.aspirate = 3
        pipette.flow_rate.dispense = 3
        
    # The actual transferring of samples
    for source_well, destination_well in zip(source_wells, destination_wells):
        pipette.transfer(volume_of_sample,
                         source_well, 
                         destination_well, 
                         new_tip='always',
                         air_gap = airgap)
    
    # Turn off lighht when finished
    protocol.set_rail_lights(False)   
##=============================================================================