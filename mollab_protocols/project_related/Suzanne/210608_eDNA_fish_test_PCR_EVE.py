# =============================================================================
# Author(s): Sanne Vreugdenhil
# Creation date: 210610
# Description: protocol to add samples to the mix.
# =============================================================================

# ==========================IMPORT STATEMENTS==================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
  
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': '210610_eDNA_fish_test_PCR_EVE',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('eDNA fish 12S test PCR - adding samples'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Adding samples to the wells with mix.
    """
# =============================================================================


# ======================LOADING LABWARE AND PIPETTES===========================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                 #deck position
        'tips_20')                          #custom name
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        5,                                 #deck position
        'tips_20')                          #custom name
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',
        4,
        'plate_96')
    sample_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        7,                                                       #deck position
        'sample_tubes_1')                                        #custom name  
    sample_tubes_2 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        1,                                                       #deck position
        'sample_tubes_2')                                        #custom name         
    ##### Loading pipettes
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1, tips_20_2])                #assigned tiprack
# =============================================================================


# ==========================VARIABLES TO SET#!!!===============================
# =============================================================================
    sample_vol = 5
      ## The primer_vol is the volume (ul) of NON barcoded F or R primer    ##
      ## that needs to be added to the reactions that do NOT get a barcode. ##
    p20.starting_tip = tips_20_1.well('F6')
      ## The starting_tip is the location of first pipette tip in the box   ##
# =============================================================================


# ==========================PREDIFINED VARIABLES===============================
# ========================creating list with sample tubes======================
## This is a list with wells in plate_96 that should be filled with sample  ##   
    samples = []
      ## Create an empty list to append wells to for the mastermix wells.   ##
    sample_columns = (
        [sample_tubes_1.columns_by_name()[column_name] for column_name in
         ['1','2','3','4','5','6']] +
        [sample_tubes_2.columns_by_name()[column_name] for column_name in
         ['1','2','3']]
        )
    for column in sample_columns:
        for well in column:
            samples.append(well)
      ## Separate the columns into wells and append them to the empty       ##
      ## mastermix wells list                                               ##
    sample_wells = (
        [sample_tubes_2.wells_by_name()[well_name] for well_name in 
         ['A4', 'B4']]
        )
    for well in sample_wells:
        samples.append(well)
# ================creating list with sample destination wells==================
## This is a list with wells in plate_96 that should be filled with sample  ##   
    sample_destinations = []
      ## Create an empty list to append wells to for the mastermix wells.   ##
    sample_destionation_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in
         ['1', '2', '3', '4', '5', '6']]
        )
    for column in sample_destionation_columns:
        for well in column:
            sample_destinations.append(well)
      ## Separate the columns into wells and append them to the empty       ##
      ## mastermix wells list                                               ##
# =============================================================================


# ================================ADDING SAMPLES===============================
# =============================================================================
## For the columns in both the source (primers) and the destination:        ##
## loop trough the wells in those columns.                                  ##
    for sample, sample_dest in zip(samples, sample_destinations):
        p20.pick_up_tip()
        p20.aspirate(sample_vol, sample)
        ## primer_mix_vol = volume for pipetting up and down                ##
        mix_vol = sample_vol + 3
        p20.mix(3, mix_vol, sample_dest)
        ## primer_dispense_vol = volume to dispense that was mixed          ##
        dispense_vol = mix_vol + 3
        p20.dispense(dispense_vol, sample_dest)
        p20.drop_tip()
# =============================================================================
