# SV&MB 210312
# Script to test if we can implement volume tracking

# Import statements
from opentrons import protocol_api
#import json to import custom labware with labware_from_definition, 
#so that we can use the simulate_protocol with custom labware
import json
#import math for tracking calculations
import math

#open json file of 5mL tube rack and set as variable
with open("C:/Users/svreugdenhil/Documents/GitHub/OT2/" 
          "custom_labware_definitions/eppendorf_15_tuberack_5000ul/"
          "eppendorf_15_tuberack_5000ul.json") as labware_file:
    labware_def_5mL = json.load(labware_file)

# Metadata
metadata = {
    'protocolName': 'distribute_test.py',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': 'check if distribute function can blow-out in source well',
    'apiLevel': '2.9'}

# Define function
def run(protocol: protocol_api.ProtocolContext):
    """check if distribute function can blow-out in source well"""
    
    # Loading labware
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', 
        1, 
        '200tips')
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr', 
        3, 
        '96well_plate')
    tubes_5mL = protocol.load_labware_from_definition(
        labware_def_5mL, #variable derived from opening json
        2, 
        '5mL_tubes')
    
    # Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2', 'right', tip_racks=[tips_200])
    
    # Set variables for volume_tracking
    start_vol = 3000 #starting volume at the beginning of the protocol in ul
    diameter = 13.3 #diameter of the top of the tube in mm
    start_height = start_vol/(math.pi*((diameter/2)**2))
    transfer_vol = 200
    delta_height =  transfer_vol/(math.pi*((diameter/2)**2))
    current_height = start_height - 1
    
    for well in plate_96.wells():
        p300.transfer(transfer_vol, tubes_5mL['A1'], well.bottom(current_height))
        if current_height - delta_height > 1:
            current_height = current_height - delta_height
    
    
    
    
    
    
