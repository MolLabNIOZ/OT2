# SV&MB 210311
# Script to test if distribute() can blow-out in source well

# Import statements
from opentrons import protocol_api
import math

# Metadata
metadata = {
    'protocolName': 'distribute_test.py',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': 'check if distribute function can blow-out in source well',
    'apiLevel': '2.9'}

# Define function
def run(protocol: protocol_api.ProtocolContext):
    """check if distribute function can blow-out in source well"""
    
# Loading labware
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', 
        7, 
        '200tips')
    tips_20 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul', 
        4, 
        '20tips')
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr', 
        9, 
        '96well_plate')
    std_tubes = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 
        8,
        '1.5mL_tubes')
    tubes_5mL = protocol.load_labware(
        'eppendorf_15_tuberack_5000ul', #!!!
        6, 
        '5mL_tubes')
    
# Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2', 'right', tip_racks=[tips_200])
    p20 = protocol.load_instrument(
        'p20_single_gen2', 'left',  tip_racks=[tips_20])
    


# Distribute mastermix from 5ml_tubes (6) to plate_96 (9) using p300
# with 200_tips (7)

    p300.distribute(
        24,
        tubes_5mL['A1'],
        plate_96.wells(),
        blow_out = True,
        blowout_location = 'source well',
        liquid_tracking = True
        )

# Distribute samples from std_tubes (8) to plate_96 (9) using p20
# with 20_tips (4).
    
    # #transfer undiluted sample from A1 std_tubes to multiple in plate_96   
    # p20.transfer(1, 
    #               std_tubes['A1'], 
    #               [plate_96.wells_by_name()[well_name] for well_name in 
    #               ['A2', 'D4', 'B5', 'F5', 'D6', 'B7', 'F7', 'D8', 'B9', 'F9',
    #                 'A11']], 
    #               new_tip='always',
    #               touch_tip=True,
    #               blow_out=True,
    #               blowout_location='destination well',
    #               mix_after=(3, 5),
    #               air_gap=1
    #               )
              
    # #transfer diluted sample from B1-B6 std_tubes to multiple in plate_96   
    # p20.transfer(1, 
    #               [std_tubes.wells_by_name()[well_name] for well_name in 
    #               ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']], 
    #               [plate_96.wells_by_name()[well_name] for well_name in 
    #               ['B2', 'C2', 'D2', 'E2', 'F2', 'G2']], 
    #               new_tip='always',
    #               touch_tip=True,
    #               blow_out=True,
    #               blowout_location='destination well',
    #               mix_after=(3, 5),
    #               air_gap=1
    #               )
    
