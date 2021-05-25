# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 210525
# Description: trying out looping through columns
# =============================================================================

from opentrons import protocol_api
## Import opentrons protocol API v2.                                         ##
metadata = {
    'protocolName': 'trying out looping through columns',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('trying out looping through columns'),
    'apiLevel': '2.9'}
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):
    """
    Trying out looping through columns.
    """      
# =============================================================================


# =====================LOADING LABWARE AND PIPETTES============================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".        ##
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',                      #labware def
        1,                                                       #deck position
        '200tips')                                               #custom name
    tubes = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        2,                                                       #deck position
        '1.5_tubes')                                             #custom name
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',                         #labware def
        3,                                                       #deck position
        'plate_96')                                          #custom name


    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack

# =============================================================================

    p300.pick_up_tip()
    
    source_well = tubes['D3']

# =============================================================================
# This is how we managed to do it, but is very long
# This works   
# =============================================================================
    # destination_wells = (
    #     [plate_96.wells_by_name()[well_name] for well_name in
    #      ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
    #       'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4',
    #       'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6',
    #       ]]
    #     )

    # for well in destination_wells:
    #     p300.aspirate(100, source_well)
    #     p300.dispense(100, well)
        
# =============================================================================
# Flatten List of Lists Using Nested for Loops
# This works!!
# =============================================================================
        
    # columns = (
    #     [plate_96.columns_by_name()[column_name] for column_name in
    #      ['2', '4', '6']])
    # for column in columns:
    #     for well in column:         
    #         p300.aspirate(100, source_well)
    #         p300.dispense(100, well)
            
# =============================================================================
# Flatten List of Lists Using a List Comprehension
# This works!!
# =============================================================================
    # columns = (
    #     [plate_96.columns_by_name()[column_name] for column_name in
    #       ['2', '4', '6']])
    # wells = [wells for column in columns for wells in column]
    # for well in wells:
    #     p300.aspirate(100, source_well)
    #     p300.dispense(100, well)
        
# =============================================================================
# Flatten List of Lists Using itertools (chain())
# This works, but not sure if robot can handle itertools
# =============================================================================
    # import itertools
    
    # columns = (
    #     [plate_96.columns_by_name()[column_name] for column_name in
    #       ['2', '4', '6']])
    # wells = list(itertools.chain(*columns))
    # for well in wells:
    #     p300.aspirate(100, source_well)
    #     p300.dispense(100, well)
        
# =============================================================================
# Flatten List of Lists Using sum
# This works
# =============================================================================
    columns = (
        [plate_96.columns_by_name()[column_name] for column_name in
          ['2', '4', '6']])
    wells = sum(columns, [])
    for well in wells:
        p300.aspirate(100, source_well)
        p300.dispense(100, well)
        


                
