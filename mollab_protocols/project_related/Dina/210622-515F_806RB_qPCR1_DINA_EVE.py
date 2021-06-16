# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 210616
# Description: qPCR protocol. First qPCR of a batch, including 3x std curve
# =============================================================================


# ======================IMPORT STATEMENTS======================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
  ## Import volume_tracking module that is on the OT2                       ##
from mollab_modules import volume_tracking_v1 as vt
 ## Import volume_tracking module for simulator                             ##
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': '210622-515F_806RB_qPCR1_DINA_EVE',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('16S qPCR - aliquoting mix and primers,'
                    'then diluting + adding sample'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    First qPCR of a batch
    Aliquoting Phusion PCRmix with EvaGreen added from a 5 mL tube to a 
    96-wells plate; using volume tracking so that the pipette starts 
    aspirating at the starting height of the liquid and goes down as the 
    volume decreases.
    After that, dilute samples 100x and add to PCR mix.
    Also include a standard sample mix and 3x standard curve
    """
# =============================================================================


# ======================LOADING LABWARE AND PIPETTES===========================
# =============================================================================
    ##### Loading labware
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        3,                                 #deck position
        'tips_200')                         #custom name
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                 #deck position
        'tips_20')                          #custom name       
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        7,                                 #deck position
        'tips_20')                          #custom name       
    plate_96_qPCR = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        5,                                  #deck position
        'plate_96_qPCR')                     #custom name
    plate_96_dil = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        4,                                  #deck position
        'plate_96_dil')                     #custom name   
    ##### !!!OPTION 1: ROBOT      
    sample_strips_1 = protocol.load_labware(
        'pcrstrips_96_wellplate_200ul',     #labware definition
        1,                                  #deck position
        'sample_strips_1')                  #custom name
    sample_strips_2 = protocol.load_labware(
        'pcrstrips_96_wellplate_200ul',     #labware definition
        2,                                  #deck position
        'sample_strips_2')                  #custom name
    
    ####    !!! OPTION 2: SIMULATOR
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
            sample_strips_1 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            1, 
            'sample_strips_1')
            sample_strips_2 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            2, 
            'sample_strips_2')
        




    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20])                #assigned tiprack
    


