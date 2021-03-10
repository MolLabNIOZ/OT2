#SV200914 - trying out changing the default gantry speed

#import statements
from opentrons import protocol_api, types

metadata = {
    'protocolName': 'gantry_speed',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'Try out, changing default gantry speed.',
    'apiLevel': '2.6'}


def run(protocol: protocol_api.ProtocolContext):
    """Function to change the gantry speed of the robot."""
     #loading labware (from opentrons labware library)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1, 
        '96plate')
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2, 
        '300tips')
    
     #load pipette 
    p300 = protocol.load_instrument('p300_single_gen2', 'right', 
        tip_racks=[tiprack_1])
    
     #transfer 100ul from plate well A1 to plate well B1
    p300.transfer(100, plate['A1'], plate['B1'])
    
     #move to 50 mm above front left of slot 5, very quickly
    p300.move_to(protocol.deck.position_for('5').move(types.Point(z=50)))
     #slow down pipette
    p300.default_speed = 100
     #move to 50 mm above front left of slot 9, much more slowly
    p300.move_to(protocol.deck.position_for('9').move(types.Point(z=50)))



