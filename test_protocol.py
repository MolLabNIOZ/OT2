from opentrons import protocol_api, types

metadata = {
    'apiLevel': '2.8'
}

def run(protocol: protocol_api.ProtocolContext): 
	tiprack = protocol.load_labware('opentrons_96_filtertiprack_200ul', '1')
	plate =protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', '2')
    
 
	p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])
	#p300.transfer(100, plate['A1'], plate['B1'])
	#p300.pick_up_tip()
	#p300.aspirate(100, plate['A1'])
	#p300.dispense(20, plate['B1'])
	#p300.dispense(30, plate['C1'])
	#p300.drop_tip()
	chunks = ['B1','C1','D1']
	p300.distribute([20,30], plate['A1'],   [plate.wells_by_name()[well_name] for well_name in ['A1', 'A2']])