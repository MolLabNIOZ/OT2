#SV201008 - complex commands OT-2

#import statements
from opentrons import protocol_api

metadata = {
    'protocolName': 'Complex commands',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'Trying out complex commands.',
    'apiLevel': '2.6'}


def run(protocol: protocol_api.ProtocolContext):
    """Function to try out complex commands."""

    #load labware (from opentrons labware library)
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1, 
                                  '96plate')
    tiprack_300_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2,
                                          '300tips')
    
    #load pipettes
    p300 = protocol.load_instrument('p300_single_gen2', 'right', 
                                    tip_racks=[tiprack_300_1])
    
    
    #transfer 400ul (2x 200ul) from A1 to B1
    #pipette will automatically use the same tip for all actions
    #pipette will automatically transfer 2x 200 ul
    p300.transfer(400, plate.wells_by_name()['A1'], 
                  plate.wells_by_name()['B1'])
    
    #transfer 200ul from A1 to A2, B1 to B2, C1 to C2 etc
    #pipette will automatically use the same tip for all actions
    p300.transfer(200, plate.columns_by_name()['1'], 
                  plate.columns_by_name()['2'])
    
    #transfer 200ul from A1 to B1, A2 to B2, A3 to B3
    #pipette will automatically use the same tip for all actions
    p300.transfer(200, plate.rows_by_name()['A'], 
                  plate.rows_by_name()['B'])
  
    #transfer 200ul from A1 to A2, A1 to B2, A1 to C2 etc 
    #= from 1 well to multiple destinations
    #pipette will automatically use the same tip for all actions
    p300.transfer(200, plate.wells_by_name()['A1'],
                  plate.columns_by_name()['2'])
    
    #transfer of different volumes from 1 well to multiple others
    #20ul from A1 to B1, 40ul from A1 to B2, 60ul from A1 to B3
    #pipette will automatically use the same tip for all actions
    p300.transfer([20, 40, 60], plate.wells_by_name()['A1'], 
                  [plate.wells_by_name()[well_name] for well_name in 
                  ['B1' ,'B2', 'B3']])
    
    #aspirate 295ul from A1, dispense 55ul in A1, A2, A3, A4, A5
    #blow out at trash 
    #aspirate 295ul from A1, dispense 55ul in A6, A7, A8, A9, A10
    #blow out at trash
    #aspirate 130ul from A1, dispense 55ul in A11, A12
    #blow out at trash and drop tip
    #the pipette will aspirate more liquid then it intends to dispense 
    # =(disposal_volume), can be specified
    p300.distribute(55, plate.wells_by_name()['A1'], plate.rows_by_name()['A'])
    
    #multiple source wells distribute
    # p300.distribute(30, [plate.wells_by_name()[well_name] for well_name in
    #                 ['A1', 'A2']], plate.rows_by_name()['A'])
    #Should aspirate 210 ul from A1 and dispense to A1, A2, A3, A4, A5, A6
    #blow out at trash
    #aspirate 210 ul from A2 and dispense to A7, A8, A9, A10, A11, A12
    #blow out at trash and drop tip 
    #BUT doesn't work as intended
    
    #transfer 8x 30ul from wells in column 2 to well A1 using 1 tip
    p300.consolidate(30, plate.columns_by_name()['2'], 
                      plate.wells_by_name()['A1'])
    
    #transfer 4x 30ul from wells A2, B2, C2, D2 to well A1 AND
    #transfer 4x 30ul from wells E2, F2, G2, H2 to well B1
    # p300.consolidate(30, plate.columns_by_name()['1'], 
    #                  [plate.wells_by_name()[well_name] for well_name in 
    #                  ['A1', 'A2']])
    #For some reason the above code doesn't work as intended.
    
    
    
    #transfer with different arguments added
    #p300.transfer(100, 'always', mix_before(2, 50), mix_after(2, 50), 
     #             touch_tip=True, air_gap=20, blow_out=True, trash=False, 
      #            disposal_volume=20, plate.wells_by_name()['A1'], 
       #           plate.wells_by_name()['B1'])
    
    