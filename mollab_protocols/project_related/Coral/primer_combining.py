# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 210621
# Description: cross-mix 12 uniquely barcoded forward primers with 8
# uniquely barcoded reverse primers.  
# =============================================================================


# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
  ## Import volume_tracking module that is on the OT2                       ##
# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'primer_combining.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('cross_mix barcoded primers'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    We have 12 unique forward primers and 8 unique reverse primers. This
    protocol will make 96 unique combinations. Stocks will be in 1.5mL tubes.
    The combinations will be made in PCR strips
    """
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading labware
    tips_200_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',     #labware definition
        10,                                  	#deck position
        'tips_200_1')                           #custom name
    tips_200_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',     #labware definition
        7,                                  	#deck position
        'tips_200_2')                           #custom name

    fwd_primer_stocks = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', #labw def
        1,                                  	#deck position
        'fwd_primers')                           #custom name    
    rev_primer_stocks = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', #labw def
        3,                                  	#deck position
        'rev_primers')                           #custom name      

    # ##### !!! FOR ROBOT      
    # primer_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',     #labware definition
    #     2,                                  #deck position
    #     'sample_strips_1')                  #custom name
    # primer_strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',     #labware definition
    #     5,                                  #deck position
    #     'sample_strips_2')                  #custom name
    
    ####    !!! FOR SIMULATOR
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
            primer_strips_1 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            2, 
            'sample_strips_1')
            primer_strips_2 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            5, 
            'sample_strips_2')


    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200_1, tips_200_2]) #assigned tiprack
   
# =============================================================================


# VARIABLES TO SET#!!!=========================================================
# =============================================================================
    primer_volume = 50
      ## How much volume of each forward and each reverse primer to combine ##
    p300.starting_tip = tips_200_1.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##

    #### primer combinations
    
    
    

    
# ALIQUOTING===================================================================
# =============================================================================

    ## F1
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['A1']],
        [primer_strips_1.columns_by_name()[column_name] for column_name in ['1']]            
        )
    ## F2
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['B1']],
        [primer_strips_1.columns_by_name()[column_name] for column_name in ['3']]            
        )
    ## F3
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['C1']],
        [primer_strips_1.columns_by_name()[column_name] for column_name in ['5']]            
        )
    ## F4
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['D1']],
        [primer_strips_1.columns_by_name()[column_name] for column_name in ['7']]            
        )
    ## F5
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['A2']],
        [primer_strips_1.columns_by_name()[column_name] for column_name in ['9']]            
        )
    ## F6
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['B2']],
        [primer_strips_1.columns_by_name()[column_name] for column_name in ['11']]            
        )
    ## F7
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['C2']],
        [primer_strips_2.columns_by_name()[column_name] for column_name in ['1']]            
        )
    ## F8
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['D2']],
        [primer_strips_2.columns_by_name()[column_name] for column_name in ['3']]            
        )
    ## F9
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['A3']],
        [primer_strips_2.columns_by_name()[column_name] for column_name in ['5']]            
        )
    ## F10
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['B3']],
        [primer_strips_2.columns_by_name()[column_name] for column_name in ['7']]            
        )
    ## F11
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['C3']],
        [primer_strips_2.columns_by_name()[column_name] for column_name in ['9']]            
        )
    ## F12
    p300.distribute(
        primer_volume, 
        [fwd_primer_stocks.wells_by_name()[well_name] for well_name in ['C4']],
        [primer_strips_2.columns_by_name()[column_name] for column_name in ['11']]            
        )

# =============================================================================

    ## R1
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['A1']],
        [primer_strips_1.wells_by_name()[well_name] for well_name in ['A1', 'A3', 'A5', 'A7', 'A9', 'A11']]            
        )
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['A1']],
        [primer_strips_2.wells_by_name()[well_name] for well_name in ['A1', 'A3', 'A5', 'A7', 'A9', 'A11']]            
        )

    ## R2
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['B1']],
        [primer_strips_1.wells_by_name()[well_name] for well_name in ['B1', 'B3', 'B5', 'B7', 'B9', 'B11']]            
        )
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['B1']],
        [primer_strips_2.wells_by_name()[well_name] for well_name in ['B1', 'B3', 'B5', 'B7', 'B9', 'B11']]            
        )
    
    ## R3
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['C1']],
        [primer_strips_1.wells_by_name()[well_name] for well_name in ['C1', 'C3', 'C5', 'C7', 'C9', 'C11']]            
        )
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['C1']],
        [primer_strips_2.wells_by_name()[well_name] for well_name in ['C1', 'C3', 'C5', 'C7', 'C9', 'C11']]            
        )
    
    ## R4
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['D1']],
        [primer_strips_1.wells_by_name()[well_name] for well_name in ['D1', 'D3', 'D5', 'D7', 'D9', 'D11']]            
        )
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['D1']],
        [primer_strips_2.wells_by_name()[well_name] for well_name in ['D1', 'D3', 'D5', 'D7', 'D9', 'D11']]            
        )

    ## R5
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['A2']],
        [primer_strips_1.wells_by_name()[well_name] for well_name in ['E1', 'E3', 'E5', 'E7', 'E9', 'E11']]            
        )
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['A2']],
        [primer_strips_2.wells_by_name()[well_name] for well_name in ['E1', 'E3', 'E5', 'E7', 'E9', 'E11']]            
        )
    
    ## R6
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['B2']],
        [primer_strips_1.wells_by_name()[well_name] for well_name in ['F1', 'F3', 'F5', 'F7', 'F9', 'F11']]            
        )
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['B2']],
        [primer_strips_2.wells_by_name()[well_name] for well_name in ['F1', 'F3', 'F5', 'F7', 'F9', 'F11']]            
        )
    
    ## R7
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['C2']],
        [primer_strips_1.wells_by_name()[well_name] for well_name in ['G1', 'G3', 'G5', 'G7', 'G9', 'G11']]            
        )
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['C2']],
        [primer_strips_2.wells_by_name()[well_name] for well_name in ['G1', 'G3', 'G5', 'G7', 'G9', 'G11']]            
        )
    
    ## R8
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['D2']],
        [primer_strips_1.wells_by_name()[well_name] for well_name in ['H1', 'H3', 'H5', 'H7', 'H9', 'H11']]            
        )
    p300.distribute(
        primer_volume, 
        [rev_primer_stocks.wells_by_name()[well_name] for well_name in ['D2']],
        [primer_strips_2.wells_by_name()[well_name] for well_name in ['H1', 'H3', 'H5', 'H7', 'H9', 'H11']]            
        )