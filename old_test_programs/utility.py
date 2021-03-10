#SV201006 try out utility commands

#import statements
from opentrons import protocol_api

metadata = {
    'protocolName': 'utility',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'Trying out utility commands',
    'apiLevel': '2.6'}
    #apiLevel is the only required argument here, rest of the metadata is
    # also shown in the Opentrons app so it is usefull to put this in

def run(protocol: protocol_api.ProtocolContext):
    """Function to try out utility commands."""
#loading labware (from opentrons labware library)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1, 
        '96plate')
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2, 
        '300tips')
#load pipette 
    p300 = protocol.load_instrument('p300_single_gen2', 'right', 
        tip_racks=[tiprack_1])
    
    
    p300.pick_up_tip()
     #aspirating 50 ul from well A1 of 96plate at 2x default flow rate, 
     #2mm from bottom
    p300.aspirate(50, plate['A1'].bottom(z=2), rate=2.0)
     #aspirating 50 ul from current location (= well A1)
    p300.aspirate(50)
    
     #move pipette well 
    p300.move_to(plate['B1'].bottom()) #to bottom of well B1
    p300.move_to(plate['B1'].top()) #to top off well B1
    p300.move_to(plate['B1'].bottom(2)) #to 2 mm abouve bottom of well B1
    p300.move_to(plate['B1'].top(-2)) #to 2 mm below top of well B1
    
     #move DIRECTLY pipette within well (without going up each time)
    p300.move_to(plate['C1'].top())
    p300.move_to(plate['C1'].bottom(1), force_direct=True)
    p300.move_to(plate['C1'].top(-2), force_direct=True)
    p300.move_to(plate['C1'].top())
    
    p300.drop_tip()
    
