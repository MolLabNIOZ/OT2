#SV201012 - protocol to check accuracy of different 300 ul tips

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
    
    # set volumes
    transfer_volume = 100
    initial_volume = 50000 #volume in source tube
        
    source_tube = tube_rack_50ml['A1']
    destination_tubes = tube_rack_ep.rows()
    
    
    
    source_height_offset = 0.5 #offset so that pipette is slightly submerged
    
   
    def check_volume():
        
        height = 1 #initial height in source tube
        source_height = height - source_height_offset  
        remaining_volume = 50000
        
        while remaining_volume > 0:
            protocol.comment(str(source_height)) #print current source_height
            
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
            
            if remaining_volume > 0:
                print(source_height)
                return True
    
    # transfer command will start pipetting from top of source to bottom 
    #destination and will continue tracking height of volumes in each tube
    # source = (source_tube.top(z=source_height))
    # destination = destination_tubes                        
    
    # if check_volume():
    #     p300.transfer(transfer_volume, source, destination)
    
    check_volume()

     

    
    
    
    