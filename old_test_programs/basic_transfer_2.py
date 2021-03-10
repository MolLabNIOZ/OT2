#SV200908 - trying first example protocol on OT2

#import statements
from opentrons import protocol_api

metadata = {
    'protocolName': 'basic_transfer_2',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'Trying out more functions.',
    'apiLevel': '2.6'}

def run(protocol: protocol_api.ProtocolContext):
    """Function to iterate trough tips."""
#loading labware (from opentrons labware library)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2, 
        '300tips')
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 3, 
        '300tips')
#loading pipette
    p300 = protocol.load_instrument('p300_single_gen2', 'right', 
        tip_racks=[tiprack_1, tiprack_2])
    
    protocol.set_rail_lights(True)
    
     #starting point A1 tiprack_1 - end point H12 tiprack_2
    for _ in range(96):
        p300.pick_up_tip()
        p300.return_tip()
    
     #another pick_up_tip() will raise error because tips ran out
    # ~ p300.pick_up_tip()
    #unless you reset tip tracking:
    
     #reset tip tracking
    p300.reset_tipracks()
    
     #starting point C3 tiprack_1 - end point H12 tiprack_2
#    for _ in range(78+96):
 #       p300.starting_tip = tiprack_1.well('C3')
  #      p300.pick_up_tip()
   #     p300.return_tip()
    
     #reset tip tracking
#    p300.reset_tipracks()
    
     #starting point A1 tiprack_1 - end point F10 tiprack_2
 #   for _ in range(78+96):
  #      p300.pick_up_tip()
   #     p300.return_tip()
   
    protocol.set_rail_lights(False)
    
