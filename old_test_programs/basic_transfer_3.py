#SV200924 example protocol liquid handling

#import statements
from opentrons import protocol_api

metadata = {
    'protocolName': 'basic_transfer_3',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'Example protocol liquid-handling commands',
    'apiLevel': '2.6'}
    #apiLevel is the only required argument here, rest of the metadata is
    # also shown in the Opentrons app so it is usefull to put this in

def run(protocol: protocol_api.ProtocolContext):
    """Function to try out liquid-handling commands."""
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
    
     #dispense 50 ul in well B1 of 96plate at 1.5x default flow rate
    p300.dispense(50, plate['B1'], rate=1.5)
     #dispense 50 ul at current location (= well B1)
    p300.dispense(50)
    
     #blow out at current location (= well B1)
    p300.blow_out()
     #blow out at specified location (= well B1)
    p300.blow_out(plate['B1'])
     #touch tip within current location (= well B1)
    
    p300.touch_tip()
     #touch tip 2mm below the top of the current location (=well B1)
    p300.touch_tip(v_offset=-2)
     #touch tip at specified location
    p300.touch_tip(plate['B1'])
     #touch tip at specified location at 100 m/s
    p300.touch_tip(plate['B1'])
     #touch tip at specified location, at 75% of total radius, 2mm below top
     #of well
    p300.touch_tip(plate['B1'], radius=0.75, v_offset=-2)
     #touch tip at specified location, at 50% of total radius, 3 mm below top
     #of well at 50 m/s
    p300.touch_tip(plate['B1'], radius=0.5, v_offset=-3, speed=50)
    
     #mix 4 times, 100 ul, in specified location (= well B1)
    p300.mix(4, 100, plate['B1'])
     #mix 3 times, 50 ul, in current location (= well B1)
    p300.mix(3, 50)
     #mix 2 times, pipette's max volume, in current location (= well B1)
    p300.mix(2)
    
     #aspirate 20 ul of extra air in tip - you can add a second argument here
     #for height but I don't know how to do that exactly
    p300.air_gap(20)
