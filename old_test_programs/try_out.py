#try out for methods and functions from the Opentrons Protocol API v2

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
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1, 
        '96plate')
    
    #dictionary indexing
    row_dict = plate.rows_by_name()['A']
    column_dict = plate.columns_by_name()['1']
    #zero-indexing
    row_list = plate.rows()[0]
    column_list - plate.columns()[0]

    print('Column "1" has', len(column_dict), 'wells')

run(protocol)
