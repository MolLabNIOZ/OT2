#SV201007 - implement door safety in protocol

#import statements
from opentrons import protocol_api

metadata = {
    'protocolName': 'basic_transfer',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'First try out API protocol on OT-2.',
    'apiLevel': '2.6'}
    #apiLevel is the only required argument here, rest of the metadata is
    # also shown in the Opentrons app so it is usefull to put this in

def run(protocol: protocol_api.ProtocolContext):
    """Function to transfer 100ul from 1 well to another."""

#loading labware (from opentrons labware library)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1, 
        '96plate')
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2, 
        '300tips')
#load pipette 
    p300 = protocol.load_instrument('p300_single_gen2', 'right', 
        tip_racks=[tiprack_1])
    
#run protocol
    while protocol.door_closed:
        if not protocol.door_closed:
            protocol.set_rail_lights(True)
            protocol.home()
            protocol.pause('Press resume when you are ready :)!')        
    
        protocol.set_rail_lights(False)        
     
    #transfer 100ul from plate well A1 to plate well B1 with default settings    
        p300.pick_up_tip()
         #aspirate & dispense at default flow rate of 92.86 ul/s
        p300.aspirate(100, plate['A1'])
        p300.dispense(100, plate['B1'])
        p300.blow_out() #blow out in current location
        p300.drop_tip() #automatically in trash
        
    #all following pipetting steps with changed default flow rates
         #aspirate at 150 ul/s
        p300.flow_rate.aspirate = 150
         #dispense at 300 ul/s
        p300.flow_rate.dispense = 300
         #blow out at 200 ul/s
        p300.flow_rate.blow_out = 200  
        
        p300.pick_up_tip()
        p300.aspirate(100, plate['C1'])
        p300.dispense(100, plate['D1'])
        p300.blow_out(plate['D1']) #blow out in destination well
        p300.drop_tip() #automatically in trash
    
        
    #all following pipetting steps aspirate & dispense other height (in mm)
         #aspirate 2 mm from bottom
        p300.well_bottom_clearance.aspirate = 3
         #dispense 10 mm from bottom
        p300.well_bottom_clearance.dispense = 10 
        
        p300.pick_up_tip()
        p300.aspirate(100, plate['E1'])
        p300.dispense(100, plate['F1'])
        p300.blow_out(plate['F1']) #blow out in destination well
        p300.drop_tip() #automatically in trash
        
        #display a comment in the opentrons app
        protocol.comment('Hello you!')
    
    #all following pipetting steps with per-axis speed limits
         #limit x-axis to 50 mm/s
        protocol.max_speeds['X'] = 50
         #limit y-axis to 50 mm/s
        protocol.max_speeds['Y'] = 50
         #limit a-axis to 50 mm/s
        protocol.max_speeds['A'] = 50
        
        p300.pick_up_tip()
        p300.aspirate(100, plate['G1'])
        p300.dispense(100, plate['H1'])
        p300.blow_out(plate['H1']) #blow out in destination well
        p300.drop_tip() #automatically in trash
        
    #all following pipetting steps with per-axis speed limits to default
         #reset x-axis speed limit - delete method
        del protocol.max_speeds['X']
         #reset y-axis speed limit - none method
        protocol.max_speeds['Y'] = None
         #reset a-axis speed limit - none method
        protocol.max_speeds['A'] = None
        
        p300.pick_up_tip()
        p300.aspirate(100, plate['B1'])
        p300.dispense(100, plate['A1'])
        p300.blow_out(plate['A1']) #blow out in destination well
        p300.drop_tip() #automatically in trash
        
        break
        
