# =============================================================================
# Author(s): Sanne Vreugdenhil
# Creation date: 210629
# Description: 
#   - add samples from 1.5 mL tubes to the 96 wells plate
# =============================================================================


# ==========================IMPORT STATEMENTS==================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': '12S_illuPCR_qPCR_no2+3_EVE',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Illumina PCR - adding samples - 12S'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Adding samples from 1.5 mL tubes to the 96 wells plate.
    """
# =============================================================================


# ======================LOADING LABWARE AND PIPETTES===========================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    # Pipette tips
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        7,                                  #deck position
        '20tips_1')                         #custom name       
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                 #deck position
        '20tips_2')                         #custom name           
    
    # Tube_racks & plates
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        3,                                  #deck position
        'plate_96')                         #custom name     
    sample_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        '4',                                                     #deck position
        'sample_tubes_1')                                        #custom name
    sample_tubes_2 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        '1',                                                     #deck position
        'sample_tubes_2')                                        #custom name
    
    # Pipettes
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1, tips_20_2])   #assigned tiprack
# =============================================================================


# ==========================VARIABLES TO SET#!!!===============================
# =============================================================================
    sample_vol = 5 
      ## The sample_vol is the volume (ul) of sample added to the PCR       ##
      ## reaction.                                                          ##
    p20.starting_tip = tips_20_1.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##
# Sample source wells==========================================================
    sample_sources = []
      ## Create an empty list to append wells to.                           ##
    sample_source_columns = (
        [sample_tubes_1.columns_by_name()[column_name] for column_name in
         ['1', '2', '3', '4', '5', '6']]+
        [sample_tubes_2.columns_by_name()[column_name] for column_name in
         ['1', '2', '3', '4']]
        )
      ## Maka a list of columns, this is a list of lists!                   ##
    for column in sample_source_columns:
        for well in column:
            sample_sources.append(well)
      ## Separate columns into wells and append them to the list.           ##  
    sample_well = sample_tubes_2['A5']
      ## Create separate well.                                              ##
    sample_sources.append(sample_well)
      ## Add separate well to list.                                         ##
# Odd sample destination wells=================================================
    odd_sample_destinations = []
      ## Create an empty sample list.                                       ##
    odd_sample_destination_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in 
         ['1', '3', '5', '7', '9']]
        )
      ## Maka a list of columns, this is a list of lists!                   ##
    for column in odd_sample_destination_columns:
        for well in column:
            odd_sample_destinations.append(well)
      ## Separate columns into wells and append them to the list.           ##   
    sample_well = plate_96['G11']
      ## Create separate well.                                              ##
    odd_sample_destinations.append(sample_well)
      ## Add separate well to list.                                         ##
# Even sample destination wells================================================
    even_sample_destinations = []
      ## Create an empty sample list.                                       ##
    even_sample_destination_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in 
         ['2', '4', '6', '8', '10']]
        )
      ## Maka a list of columns, this is a list of lists!                   ##
    for column in even_sample_destination_columns:
        for well in column:
            even_sample_destinations.append(well)
      ## Separate columns into wells and append them to the list.           ##   
    sample_well = plate_96['G12']
      ## Create separate well.                                              ##
    even_sample_destinations.append(sample_well)
      ## Add separate well to list.                                         ##
# =============================================================================


# ================================ADDING SAMPLES===============================
# 1x Samples===================================================================
    ## For the columns in both the source (primers) and the destination     ##
    ## (mix): loop trough the wells in those columns.                       #
    for sample_tube, mix_tube in zip(sample_sources, odd_sample_destinations):
        p20.pick_up_tip()
        p20.aspirate(sample_vol, sample_tube)
        p20.dispense(sample_vol, mix_tube)
        sample_mix_vol = sample_vol + 3
        ## primer_mix_vol = volume for pipetting up and down                ##
        p20.mix(3, sample_mix_vol, mix_tube)
        p20.dispense(10, mix_tube)
        p20.drop_tip()
# 2x Samples===================================================================
    ## For the columns in both the source (primers) and the destination     ##
    ## (mix): loop trough the wells in those columns.                       #
    for sample_tube, mix_tube in zip(sample_sources, even_sample_destinations):
        p20.pick_up_tip()
        p20.aspirate(sample_vol, sample_tube)
        p20.dispense(sample_vol, mix_tube)
        sample_mix_vol = sample_vol + 3
        ## primer_mix_vol = volume for pipetting up and down                ##
        p20.mix(3, sample_mix_vol, mix_tube)
        p20.dispense(10, mix_tube)
        p20.drop_tip()
# =============================================================================
    