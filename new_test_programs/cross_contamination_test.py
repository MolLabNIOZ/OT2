# SV&MB 210310
# Script to test if cross-contamination occurs when robot moves
# over open tubes/wells

# Import statements
from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'cross_contamination_test.py',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': 'Test for cross-contamination.',
    'apiLevel': '2.9'}

# Define function
def run(protocol: protocol_api.ProtocolContext):
    """Test for cross-contamination."""
    
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
        'opentrons_15_tuberack_falcon_15ml_conical', 
        6, 
        '5mL_tubes')
    
# Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2', 'right', tip_racks=[tips_200])
    p20 = protocol.load_instrument(
        'p20_single_gen2', 'left',  tip_racks=[tips_20])
    
# Distribute mastermix from 5ml_tubes (6) to plate_96 (9) using p300
# with 200_tips (7).
    
    #pick up tip
    p300.pick_up_tip()
    
    #make a list with all the columns
    #NOTE THIS WORKS ONLY FOR 25 UL REACTIONS WITH 200 UL PIPETTE!
    #aspirate 200 ul - dispense 24 ul per time = 8.3 so max 8 dispenses
    #we have 12 columns with 8 rows, so we can aspirate 200 for each column
    #--> IN FUTURE WE SHOULD FIND OUT HOW TO AUTOMATE - dispense only takes 
    #name of 1 well, not multiple wells
    for column in range(1, 13): #13 because range is untill not including
        p300.aspirate(200, tubes_5mL['A1'])
        p300.touch_tip(v_offset=-10)#touch tip 10mm below top current well
        wells = ['A' + str(column), 'B' + str(column), 'C' + str(column),
                 'D' + str(column), 'E' + str(column), 'F' + str(column),
                 'G' + str(column), 'H' + str(column)]
        for well in wells:
            p300.dispense(24, plate_96[well])
            p300.touch_tip(v_offset=-2)#touch tip 2mm below top current well
        p300.blow_out(tubes_5mL['A1'].top(z=-10))#blow out 10mm below top A1
    
    #drop tip
    p300.drop_tip()
    
# Distribute samples from std_tubes (8) to plate_96 (9) using p20
# with 20_tips (4).
    
    #transfer undiluted sample from A1 std_tubes to multiple in plate_96   
    p20.transfer(1, 
                  std_tubes['A1'], 
                  [plate_96.wells_by_name()[well_name] for well_name in 
                  ['A2', 'D4', 'B5', 'F5', 'D6', 'B7', 'F7', 'D8', 'B9', 'F9',
                    'A11']], 
                  new_tip='always',
                  touch_tip=True,
                  blow_out=True,
                  blowout_location='destination well',
                  mix_after=(3, 5),
                  air_gap=1
                  )
              
    #transfer diluted sample from B1-B6 std_tubes to multiple in plate_96   
    p20.transfer(1, 
                  [std_tubes.wells_by_name()[well_name] for well_name in 
                  ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']], 
                  [plate_96.wells_by_name()[well_name] for well_name in 
                  ['B2', 'C2', 'D2', 'E2', 'F2', 'G2']], 
                  new_tip='always',
                  touch_tip=True,
                  blow_out=True,
                  blowout_location='destination well',
                  mix_after=(3, 5),
                  air_gap=1
                  )
    
