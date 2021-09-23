# =============================================================================
# Author: Sanne Vreugdenhil
# Creation date: 210920
# Description: protocol for aliquoting illumina primers
# =============================================================================


# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
  
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
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
    Aliquoting Illumina primers from 1 tube rack filled with 1.5 mL tubes,
    to PCR strips in a BioRad 96-well plate, calibrated with Westburg
    PCR strips.
    """   
# =============================================================================


# VARIABLES TO SET#!!!=========================================================
# =============================================================================      
    primer_volume = 15
      ## NOTE: The type of pipette is dependent on the primer volume.
    primer_combinations = 24
    starting_tip = 'B6'
    starting_tip_box = 1
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    primer_tubes = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        3,                                                       #deck position
        'primer_tubes')                                          #custom name
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
    
    if primer_volume <= 20:
        tips_1= protocol.load_labware(
            'opentrons_96_filtertiprack_20ul', #labware definition
            10,                                #deck position
            '20tips')                          #custom name
        tips_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul', #labware definition
            7,                                 #deck position
            '20tips')                          #custom name
        tips_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul', #labware definition
            4,                                 #deck position
            '20tips')                          #custom name
        tips_4 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul', #labware definition
            1,                                 #deck position
            '20tips')                          #custom name
        pipette = protocol.load_instrument(
            'p20_single_gen2',                 #instrument definition
            'left',                            #mount position
            tip_racks=[tips_1, tips_2, tips_3, tips_4])#as tiprack  
        if starting_tip_box == 1:
            pipette.starting_tip = tips_1.well(starting_tip)
        if starting_tip_box == 2:
            pipette.starting_tip = tips_2.well(starting_tip)
        if starting_tip_box == 3:
            pipette.starting_tip = tips_3.well(starting_tip)
        if starting_tip_box == 4:
            pipette.starting_tip = tips_4.well(starting_tip)
        airgap_vol = 5   
        
    if primer_volume > 20:
        tips_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            10,                                  #deck position
            '200tips')                          #custom name
        tips_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            7,                                  #deck position
            '200tips')                          #custom name
        tips_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            4,                                  #deck position
            '200tips')                          #custom name
        tips_4 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            1,                                  #deck position
            '200tips')                          #custom name
        pipette = protocol.load_instrument(
            'p300_single_gen2',                 #instrument definition
            'right',                            #mount position
            tip_racks=[tips_1, tips_2, tips_3, tips_4])#as tiprack
        if starting_tip_box == 1:
            pipette.starting_tip = tips_1.well(starting_tip)
        if starting_tip_box == 2:
            pipette.starting_tip = tips_2.well(starting_tip)
        if starting_tip_box == 3:
            pipette.starting_tip = tips_3.well(starting_tip)
        if starting_tip_box == 4:
            pipette.starting_tip = tips_4.well(starting_tip)
        airgap_vol = 10
# =============================================================================
    primers = int(primer_combinations * 2)
    source = primer_tubes.wells()
    destination = (
        [pcr_strips.wells_by_name()[well_name] for well_name in 
         ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
          'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
          'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11'
          ]])
    destinations = []
    for well in destination:
        destinations.append(well)
    destinations = destinations[:primers]
    
    primer_tubes_1 = (
        [primer_tubes.wells_by_name()[well_name] for well_name in
         ['A1', 'B1', 'C1', 'D1', 'A2', 'B2', 'C2', 'D2']])
    primer_tubes_2 = (
        [primer_tubes.wells_by_name()[well_name] for well_name in
         ['A3', 'B3', 'C3', 'D3', 'A4', 'B4', 'C4', 'D4']])
    primer_tubes_3 = (
        [primer_tubes.wells_by_name()[well_name] for well_name in
         ['A5', 'B5', 'C5', 'D5', 'A6', 'B6', 'C6', 'D6']])
    
    primer_strips_1 = (
        [pcr_strips.wells_by_name()[well_name] for well_name in 
         ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2']])
    primer_strips_2 = (
        [pcr_strips.wells_by_name()[well_name] for well_name in 
         ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7']])
    primer_strips_3 = (
        [pcr_strips.wells_by_name()[well_name] for well_name in 
         ['A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11']])
# =============================================================================    

    protocol.set_rail_lights(True)
    protocol.pause('Are the right pipette tips in (20 for <= 20uL and 200' 
                   ' for >20 uL)?')
    while primers >= 24: 
        for primer_tube, pcr_strip_tube in zip(source, destination):
             ## simultanious loop through primer_tubes and PCR_strips       ##
             ## From wells to columns doesn't work, therefore all PCRstrip  ##
             ## wells are given.                                            ##
            pipette.pick_up_tip()
            pipette.aspirate(primer_volume, primer_tube)
            pipette.air_gap(airgap_vol)
            pipette.dispense(primer_volume + 50, pcr_strip_tube)
            pipette.air_gap(airgap_vol)
             ## air_gap to suck up any liquid that remains in the tip       ##
            pipette.drop_tip()
         ## Used aspirate/dipense instead of transfer, to allow for more    ##
         ## customization.                                                  ##
        protocol.pause('Time for new primers!')
        primers -= 24 
        if primers / 2 <= 24:
            protocol.pause('STOP')
   
    protocol.set_rail_lights(False)

    # for primer in range(primers):
    #     for primer_tube, pcr_strip_tube in zip(source, destination):
    #          ## simultanious loop through primer_tubes and PCR_strips       ##
    #          ## From wells to columns doesn't work, therefore all PCRstrip  ##
    #          ## wells are given.                                            ##
    #         pipette.pick_up_tip()
    #         pipette.aspirate(primer_volume, primer_tube)
    #         pipette.air_gap(airgap_vol)
    #         pipette.dispense(primer_volume + 50, pcr_strip_tube)
    #         pipette.air_gap(airgap_vol)
    #          ## air_gap to suck up any liquid that remains in the tip       ##
    #         pipette.drop_tip()
    #      ## Used aspirate/dipense instead of transfer, to allow for more    ##
    #      ## customization.                                                  ##
    #     protocol.pause('Time for new primers!')
    #     primer_combinations -= 24   