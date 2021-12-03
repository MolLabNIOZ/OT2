"""
illu_primer.py is a protocol written for WALL-E to make aliquots of (barcoded)
primers -- from 1.5mL tubes into PCR strips.
"""

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
  
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
  
import math
  ## Import math to be able to do some calculations.                        ## 
# =============================================================================



# VARIABLES TO SET#!!!=========================================================
# =============================================================================      
# How much primer volume (µL) do you want to aliquot?
primer_volume = 22
  ## NOTE: The type of pipette is dependent on the primer volume.
  
# How many primer combinations need to be aliquoted?
primer_combinations = 25

# What is the starting position fo the tips?
starting_tip = 'B6'
# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'Aliquoting Illumina primers, 1 rack at a time',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Protocol for aliquoting illumina primers, 1 eppendorf' 
                    ' rack at a time. Pausing after every rack so that'
                    ' you can put the next rack in.'
                    'NOTE: PUT STRIPS IN COLUMNS 2, 7, 11 WITH THE CAPS TO'
                    ' THE RIGHT'),
    'apiLevel': '2.9'}
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting Illumina primers from 1 tube rack filled with 1.5 mL tubes, to
    PCR strips in a BioRad 96-well plate, calibrated with Westburg strips.
    """   
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    # Source racks for primer dilutions in 1.5mL tubes
    F_primers = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        2,                                                       #deck position
        'F_primers')                                          #custom name
    R_primers = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        3,                                                       #deck position
        'R_primers')                                          #custom name
    
    # Destination rack for primer aliquot in PCR strips
    ##### !!! OPTION 1: ROBOT      
    # pcr_strips = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     6,                                 #deck position
    #     'pcr_strips')                      #custom name
    ##### !!! OPTION 2: SIMULATOR
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
    pcr_strips = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            6,                     #deck position
            'pcr_strips')          #custom name
        #Load the labware using load_labware_from_definition() instead of  ##
        #load_labware(). Then use the variable you just set with the opened##
        #json file to define which labware to use.                         ##
    
    # Pipette for small volumes
    if primer_volume <= 20:
        tips_1= protocol.load_labware(
            'opentrons_96_filtertiprack_20ul', #labware definition
            10,                                #deck position
            '20tips_1')                        #custom name
        tips_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul', #labware definition
            7,                                 #deck position
            '20tips_2')                        #custom name
        tips_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul', #labware definition
            4,                                 #deck position
            '20tips_3')                        #custom name
        tips_4 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul', #labware definition
            1,                                 #deck position
            '20tips_4')                        #custom name
        pipette = protocol.load_instrument(
            'p20_single_gen2',                 #instrument definition
            'left',                            #mount position
            tip_racks=[tips_1, tips_2, tips_3, tips_4])#as tiprack  
        pipette.starting_tip = tips_1.well(starting_tip)
        airgap_vol = 5   
    
    # Pipette for big volumes
    if primer_volume >= 21:
        tips_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            10,                                 #deck position
            '200tips_1')                         #custom name
        tips_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            7,                                  #deck position
            '200tips_2')                        #custom name
        tips_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            4,                                  #deck position
            '200tips_3')                        #custom name
        tips_4 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            1,                                  #deck position
            '200tips_4')                        #custom name
        pipette = protocol.load_instrument(
            'p300_single_gen2',                 #instrument definition
            'right',                            #mount position
            tip_racks=[tips_1, tips_2, tips_3, tips_4])#as tiprack
        pipette.starting_tip = tips_1.well(starting_tip)
        airgap_vol = 10
# =============================================================================

    F_primers = F_primers.wells()
    R_primers = R_primers.wells()
    primer_strips = (
        [pcr_strips.columns_by_name()[well_name] for well_name in 
         ['2', '7', '11']])
    
    F_source = []
    R_source = []
    destination = []
    
    # for well in F_primers:
    #     F_source.append(well)
    #     F_source = F_source[:primer_combinations]
    # for well in R_primers:
    #     R_source.append(well)
    #     R_source = R_source[:primer_combinations]
    # for column in primer_strips:
    #     for well in column:
    #         destination.append(well)
    #         destination = destination[:primer_combinations]

# =============================================================================
    protocol.set_rail_lights(True)
    protocol.pause('Are the right pipette tips in (20 for <= 20uL and 200' 
                   ' for >20 uL)?')
    
    for primer in range(primer_combinations):
        primer_combinations = primer_combinations
        for well in F_primers:
            F_source.append(well)
            F_source = F_source[:primer_combinations]
        for well in R_primers:
            R_source.append(well)
            R_source = R_source[:primer_combinations]
        for column in primer_strips:
            for well in column:
                destination.append(well)
                destination = destination[:primer_combinations]
        for primer_tube, pcr_strip_tube in zip(F_source, destination):
            pipette.pick_up_tip()
            pipette.aspirate(primer_volume, primer_tube)
            # pipette.air_gap(airgap_vol)
            pipette.dispense(primer_volume + 50, pcr_strip_tube)
            # pipette.air_gap(airgap_vol)
             ## air_gap to suck up any liquid that remains in the tip       ##
            pipette.drop_tip()
        for primer_tube, pcr_strip_tube in zip(R_source, destination):
            pipette.pick_up_tip()
            pipette.aspirate(primer_volume, primer_tube)
            # pipette.air_gap(airgap_vol)
            pipette.dispense(primer_volume + 50, pcr_strip_tube)
            # pipette.air_gap(airgap_vol)
             ## air_gap to suck up any liquid that remains in the tip       ##
            pipette.drop_tip()   
        protocol.pause()
        primer_combinations - 24