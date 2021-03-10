#SV201028 complex commands OT-2 parameters

# import statements
from opentrons import protocol_api

metadata = {
    'protocolName': 'Complex command parameters',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'Trying out complex command parameters.',
    'apiLevel': '2.6'}


def run(protocol: protocol_api.ProtocolContext):
    """Function to try out complex command parameters."""

    # load labware (from opentrons labware library)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1, 
                                  '96plate')
    tiprack_300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2,
                                          '300tips')
    
    # load pipettes
    p300 = protocol.load_instrument('p300_single_gen2', 'right', 
                                    tip_racks=[tiprack_300_1])
    
    
    # by default transfer command uses the same tip for each well
    # this can be changed using the parameter for new_tip
    p300.transfer(100, 
                  [plate.wells_by_name()[well_name] for well_name in 
                   ['A1', 'A2', 'A3']], 
                  [plate.wells_by_name()[well_name] for well_name in 
                   ['B1', 'B2', 'B3']],
                  new_tip='always')
    
    # for scenarios where you instead are calling pick_up_tip() and drop_tip()
    #elsewhere in your protocol, you can ignore the picking up or dropping tip
    p300.pick_up_tip()
    p300.transfer(100, 
                  [plate.wells_by_name()[well_name] for well_name in 
                   ['C1', 'C2', 'C3']], 
                  [plate.wells_by_name()[well_name] for well_name in 
                   ['D1', 'D2', 'D3']],
                  new_tip='never')
    p300.drop_tip()
    
    # by default complex commands will drop tips into the trash container
    # this can be changed by setting the trash parameter to False
    # the command will then return the tip to it's original location
    p300.transfer(100, plate['A1'], plate['B1'], trash=False)
    
    # touch tip can be performed after every aspirate and dispense by setting
    #the parameter touch_tip to True
    p300.transfer(100, plate['A1'], plate['B1'], touch_tip=True)
    
    # blow out can be performed after every dispense by setting the parameter 
    #blow_out to True
    p300.transfer(100, plate['A1'], plate['B1'], blow_out=True)
    
    # mix can be performed before every aspirate (mix_before) and after every
    #dispense (mix_after), value must be a tuple, first number = repetitions
    #second number = volume
    p300.transfer(100, plate['A1'], plate['B1'], 
                  mix_before=(2, 50), #mix 2 times 50ul before aspirate
                  mix_after=(3, 75)) #mix 3 times 75ul after dispense
    
    # air gap can be performed after every aspirate by setting the parameter
    #air_gap=volume (value is volume in ul of air), entire volume of air +
    #liquid will be aspirated
    p300.transfer(100, plate['A1'], plate['B1'], air_gap=20)
    
    # disposal volume can be set using the parameter disposal_volume, an extra
    #volume wil be aspirated but not dispensed
    p300.distribute(30, [plate.wells_by_name()[well_name] for well_name in 
                         ['A1', 'A2']], 
                    plate.columns_by_name()['2'],
                    disposal_volume=60)
    
