#SV200917 - trying lists and dictionary functionality in well position

#import statements
from opentrons import protocol_api

metadata = {
    'protocolName': 'well_transfer',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'Well position try out.',
    'apiLevel': '2.6'}

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
#load column & row
     #dictionary indexing - row A and column 1
    row_dict = plate.rows_by_name()['A']
    column_dict = plate.columns_by_name()['1']
     #zero-indexing - row B anc column 2
    row_list = plate.rows()[1]
    column_list = plate.columns()[1]
    
    print('Column "1" has', len(column_dict), 'wells')
    print('Row "A" has', len(row_dict), 'wells')
    
    for well in row_dict:
        print(well)
    for well in column_dict:
        print(well)
    for well in row_list:
        print(well)
    for well in column_list:
        print(well)

