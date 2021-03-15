# SV&MB 210312
# Script to test if we can implement volume tracking

# Import statements
from opentrons import protocol_api
#import json to import custom labware with labware_from_definition, 
#so that we can use the simulate_protocol with custom labware
import json


#import module for disposal aspiration volume
from modules import disposal_volume as dv
# import module for volume tracking
from modules import volume_tracking as vol_track


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
    # #for robot
    # tubes_5mL = protocol.load_labware(
    #     'eppendorf_15_tuberack_5000ul', 
    #     2, 
    #     '5mL_tubes')
    
    #for simulator
    #open json file of 5mL tube rack and set as variable
    with open("custom_labware_definitions/eppendorf_15_tuberack_5000ul/"
          "eppendorf_15_tuberack_5000ul.json") as labware_file:
        labware_def_5mL = json.load(labware_file)
    tubes_5mL = protocol.load_labware_from_definition( 
        labware_def_5mL, #variable derived from opening json
        2, 
        '5mL_tubes')
    
    # Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2', 'right', tip_racks=[tips_200])
    
    # Set variables 
    container = 'tube_5mL'
    #container options: 'tube_1.5ml', 'tube_2mL', 'tube_5mL', 'tube_15mL', 'tube_50mL'
    start_vol = 2600 #volume in ul that is in your tube at the beginning
    dispension_vol = 24 #volume that is dispensed each time
    aspiration_vol = dv.disposal_volume_p300(dispension_vol) #volume that is aspirated each time
    #NOTE: for aspiration volume you can choose whether you want to have
    #a disposal volume or not - for aliquoting liquids we advise to use it
    #When using a disposal volume use: 
    # dv.disposal_volume_p300(dispension_vol) 
    # dv.disposal_volume_p20(dispension_vol)
    # MAX = dispension_volume = 196 ul
    #When NOT using a disposal volume
    # aspiration_vol = dispension_vol
    
    # Volume tracking
    current_vol = start_vol
    #If you don't want to use volume tracking ommit the .bottom() 
    
    #set lights on
    protocol.set_rail_lights(True)
    
    # Aliquoting mix from 5 mL tube to entire 96-wells plate
    p300.pick_up_tip(tips_200['A3'])
    for well in plate_96.wells():
        current_height, current_vol, delta_height = vol_track.volume_tracking(container, current_vol, aspiration_vol)
        aspiration_location = tubes_5mL['A1'].bottom(current_height) #where to get the mastermix from
        p300.aspirate(aspiration_vol, aspiration_location)
        p300.dispense(dispension_vol, well)
        p300.blow_out(tubes_5mL['A1'])
        if current_height - delta_height <= 1: #make sure bottom is never reached
            protocol.home()
            protocol.pause('Your mix is finished.')
    p300.drop_tip()
    
    #set lights off
    protocol.set_rail_lights(False)
