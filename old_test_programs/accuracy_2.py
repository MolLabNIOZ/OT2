#SV201030 - trying to implement liquid level

#import statements
from opentrons import protocol_api

metadata = {
    'protocolName': 'accuracy',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'Testing accuracy of different 300 ul tips.',
    'apiLevel': '2.6'}

def run(protocol: protocol_api.ProtocolContext):
    """Function to implement liquid level in program."""
    
    # loading labware
    tube_rack_50ml = protocol.load_labware(
        'opentrons_6_tuberack_falcon_50ml_conical', 1, '50mL')
    
    tube_rack_ep = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2, 
        'Eppies')
    
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 4, 
                                      'TipOneFilter300')
    
    # load pipette 
    p300 = protocol.load_instrument('p300_single_gen2', 'right', 
                                    tip_racks=[tiprack])
    
    #set volumes
    max_vol = 50000
    rem_vol = 50000
    volume = 300
    max_height = 113,3

    #set height
    height_per_vol = volume * max_height / max_vol
    height_decrease = max_height - height_per_vol
    
    #set source and destination
    source_tube = tube_rack_50ml['A1']
    dest_tube = tube_rack_ep['A1']
    
    p300.pick_up_tip()
    while rem_vol > 0:
        protocol.comment(str(height_decrease) #print current height
        
        # transfer command will start pipetting from top of source to bottom 
        #destination and will continue tracking height of volumes in each tube
        source = (source_tube.top(z=source_height))
        destination = destination_tubes
        p300.transfer(transfer_volume, source, destination,
                      blow_out=True, new_tip='never')
        
        #update height by substracting ratio of transfer_volume:initial_volume
        #or set to bottom of tube is "below" bottom
        if height > -1:
            height -= (transfer_volume/initial_volume)*2 
            #x2 because tube size is -1 to 1 i.e. a difference of 2
        else: 
            height = -1
            
        #update source height or set to bottom of tube
        source_height = height - source_height_offset
        if source_height < -1:
            source_height = -1
        
        #update remaining volume
        remaining_volume -= transfer_volume
    p300.drop_tip()
        

            
        
    
    
    
    