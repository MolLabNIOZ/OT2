#SV202007 - try out homing function

#import statements
from opentrons import protocol_api

metadata = {
    'protocolName': 'home',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'Trying out home command',
    'apiLevel': '2.6'}
    #apiLevel is the only required argument here, rest of the metadata is
    # also shown in the Opentrons app so it is usefull to put this in

def run(protocol: protocol_api.ProtocolContext):
    """A function to try out the home commands."""
#load labware
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1, 
        '96plate')
#load pipette
    p300 = protocol.load_instrument('p300_single_gen2', 'right')
   
    
    p300.move_to(plate['A1'].top()) #move to top of well A1 of 96plate
    protocol.home() #homes gantry, z axes, and plungers
    p300.move_to(plate['B1'].top()) #move to top of well B1 of 96plate
    #p300.home() #homes the right z axis and plunger
    #p300.move_to(plate['C1'].top()) #move to top of well C1 of 96plate
    #p300.home_plunger() #homes the right plunger
    