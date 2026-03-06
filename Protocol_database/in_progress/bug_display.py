"""
basic protocol to show bug with tip tracking while changing between nozzle_layout
in 8 channel pipet
"""
#### Import opentrons protocol API v2
from opentrons import protocol_api

#### MetaData
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': '8_channel tip tracking bug_display',
            'description': 'basic protocol to show bug with tip tracking while changing between nozzle_layout in 8 channel pipet'}
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}

#### start run def
def run(protocol: protocol_api.ProtocolContext):

    # load tip rack
    tip_rack = protocol.load_labware('opentrons_96_filtertiprack_20ul',4,'tips_p20_1')

    
    # load pipette
    left_pipette = protocol.load_instrument('p20_multi_gen2','left',[tip_rack])
    left_pipette.starting_tip = tip_rack.well("B1") 
    
    # # set nozzle_layout to single channel
    # left_pipette.configure_nozzle_layout(style=protocol_api.SINGLE, start='A1', tip_racks=[tip_rack])
    
    # # pick_up and drop some tips
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()     
    
    # # set nozzle_layout to all channel
    # left_pipette.configure_nozzle_layout(style=protocol_api.ALL, tip_racks=[tip_rack])
    
    # # pick_up and drop some tips
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    
    # set nozzle_layout to partial column
    left_pipette.configure_nozzle_layout(style=protocol_api.PARTIAL_COLUMN, start="H1", end="E1", tip_racks=[tip_rack])
    
    # pick_up and drop some tips
    left_pipette.pick_up_tip()
    left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    
    # # set nozzle_layout to single channel
    # left_pipette.configure_nozzle_layout(style=protocol_api.SINGLE, start='A1', tip_racks=[tip_rack])
    
    # # pick_up and drop some tips
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip()
    # left_pipette.pick_up_tip()
    # left_pipette.drop_tip() 