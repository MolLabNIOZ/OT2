# SV&MB 210312
# Script to test if we can implement volume tracking

# Import statements
from opentrons import protocol_api
#import json to import custom labware with labware_from_definition, 
#so that we can use the simulate_protocol with custom labware
import json
#import math for tracking calculations
import math


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
    #for robot
    tubes_5mL = protocol.load_labware(
        'eppendorf_15_tuberack_5000ul', 
        2, 
        '5mL_tubes')
    
    # #for simulator
    # #open json file of 5mL tube rack and set as variable
    # with open("C:/Users/svreugdenhil/Documents/GitHub/OT2/" 
    #       "custom_labware_definitions/eppendorf_15_tuberack_5000ul/"
    #       "eppendorf_15_tuberack_5000ul.json") as labware_file:
    #     labware_def_5mL = json.load(labware_file)
    # tubes_5mL = protocol.load_labware_from_definition( 
    #     labware_def_5mL, #variable derived from opening json
    #     2, 
    #     '5mL_tubes')
    
    # Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2', 'right', tip_racks=[tips_200])
    
    # Set variables for volume_tracking
    start_vol = 3000 #starting volume at the beginning of the protocol in ul
    diameter = 13.3 #diameter of the top of the tube in mm
    start_height = start_vol/(math.pi*((diameter/2)**2)) #height of the starting volume
    transfer_vol = 200 #volume that is transfered each time
    delta_height =  transfer_vol/(math.pi*((diameter/2)**2)) # height of the transferred volume
    current_height = start_height - 1 #height - something to make sure pipette is submerged
    
    #set lights on
    protocol.set_rail_lights(True)
    
    p300.pick_up_tip(tips_200['A3'])
    for well in plate_96.wells():
        p300.transfer(
            transfer_vol, 
            tubes_5mL['A1'].bottom(current_height), 
            well,
            new_tip='never',
            blow_out='true',
            blowout_location='source well'
            )
        if current_height - delta_height >= 1: #make sure bottom is never reached
            current_height = current_height - delta_height #calculate new hight after pipetting step
        else: 
            protocol.home()
            protocol.pause('Your mix is finished.')
    p300.drop_tip()
    
    #set lights off
    protocol.set_rail_lights(False)    
    
    
    
    
