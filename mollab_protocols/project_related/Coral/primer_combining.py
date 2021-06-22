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
    #     'primer_strips_1')                  #custom name
    # primer_strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',     #labware definition
    #     5,                                  #deck position
    #     'primer_strips_2')                  #custom name
    
    ####    !!! FOR SIMULATOR
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
            primer_strips_1 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            2, 
            'primer_strips_1')
            primer_strips_2 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            5, 
            'primer_strips_2')


    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 # instrument definition
        'right',                            #mount position
        tip_racks=[tips_200_1, tips_200_2]) #assigned tiprack
   
# =============================================================================


# VARIABLES TO SET#!!!=========================================================
# =============================================================================
    primer_volume = 50
      ## How much volume of each forward and each reverse primer to combine ##
    p300.starting_tip = tips_200_1.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##

    #### primer destinations
    fwd_primers = []
    for column in ([fwd_primer_stocks.columns_by_name()[column_name] 
                    for column_name in ['1', '2', '3']]):
        for well in column:
            fwd_primers.append(well)
    
    rev_primers = []
    for column in ([rev_primer_stocks.columns_by_name()[column_name] 
                    for column_name in ['1', '2']]):
        for well in column:
            rev_primers.append(well)
    
    fwd_columns = (
        [primer_strips_1.columns_by_name()[column_name] for column_name in 
         ['1', '3', '5', '7', '9', '11']]
        +
        [primer_strips_2.columns_by_name()[column_name] for column_name in 
         ['1', '3', '5', '7', '9', '11']]
        )
    
    rev_rows1 = (
        [primer_strips_1.rows_by_name()[row_name] for row_name in 
         ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']]
        )
    rev_rows2 = (
        [primer_strips_2.rows_by_name()[row_name] for row_name in 
         ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']]
        )

# =============================================================================

   
# ALIQUOTING===================================================================
# =============================================================================

    # #### aliquoting 12 unique fwd primers in 12 strips
    for i, fwd_primer in enumerate(fwd_primers):
        source = fwd_primer
        destination = fwd_columns[i]
        p300.distribute(
            primer_volume,
            source,
            destination,
            air_gap = True
            )
    
    #### aliquoting 8 unique rev primers in 8 rows of 12 strips
    for i1, rev_primer in enumerate(rev_primers):
        for i2, well in enumerate(rev_rows1[i1] + rev_rows2[i1]):
            source = rev_primer
            destination = well
            if i2 % 2 == 0:
                ## every other, because strips are only in every other row  ##
                p300.pick_up_tip()
                p300.aspirate(primer_volume, source)
                p300.air_gap(10)
                  ## air_gap to avoid dripping                              ##
                p300.dispense(primer_volume + 10, destination)
                  ## volume + 10 to completely empty tip                    ##
                p300.air_gap(50)
                  ## air_gap to suck up any liquid that remains in the tip  ##
                p300.drop_tip()            
                
                
            
 
    

