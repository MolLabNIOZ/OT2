# =============================================================================
# Author: Sanne Vreugdenhil
# Creation date: 211022
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
                    ' you can put the next rack in.'),
    'apiLevel': '2.9'}
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting Illumina primers from 1 tube rack filled with 1.5 mL tubes,
    to a BioRad 96-well plate.
    """   
# =============================================================================


# VARIABLES TO SET#!!!=========================================================
# =============================================================================      
    primer_volume = 22
      ## NOTE: The type of pipette is dependent on the primer volume.
    primer_combinations = 25
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
    # plate = protocol.load_labware(
    #     'biorad_qpcr_plate_eppendorf_cool_rack',    #labware definition
    #     6,                                 #deck position
    #     '96well_plate_rack')                      #custom name
    ##### !!! OPTION 2: SIMULATOR
    with open("labware/biorad_qpcr_plate_eppendorf_cool_rack/"
              "biorad_qpcr_plate_eppendorf_cool_rack.json") as labware_file:
            labware_def_plate = json.load(labware_file)
    plate = protocol.load_labware_from_definition( 
            labware_def_plate,  #variable derived from opening json
            6,                  #deck position
            '96well_plate_rack')#custom name
        #Load the labware using load_labware_from_definition() instead of  ##
        #load_labware(). Then use the variable you just set with the opened##
        #json file to define which labware to use.                         ##

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
        if starting_tip_box == 1:
            pipette.starting_tip = tips_1.well(starting_tip)
        if starting_tip_box == 2:
            pipette.starting_tip = tips_2.well(starting_tip)
        if starting_tip_box == 3:
            pipette.starting_tip = tips_3.well(starting_tip)
        if starting_tip_box == 4:
            pipette.starting_tip = tips_4.well(starting_tip)
        airgap_vol = 5   
        
    if primer_volume >= 21:
        tips_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            10,                                  #deck position
            '200tips_1')                          #custom name
        tips_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            7,                                  #deck position
            '200tips_2')                          #custom name
        tips_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            4,                                  #deck position
            '200tips_3')                          #custom name
        tips_4 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', #labware definition
            1,                                  #deck position
            '200tips_4')                          #custom name
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

# SETTING SOURCE AND DESTINATION===============================================
# =============================================================================  
    primer_tubes = (
        [primer_tubes.wells_by_name()[well_name] for well_name in
         ['A1', 'B1', 'C1', 'D1', 'A2', 'B2', 'C2', 'D2',
          'A3', 'B3', 'C3', 'D3', 'A4', 'B4', 'C4', 'D4',
          'A5', 'B5', 'C5', 'D5', 'A6', 'B6', 'C6', 'D6']])
    primer_plate = plate.wells()
    
    source = primer_tubes[:primer_combinations]
    destination = primer_plate[:primer_combinations]
        
# =============================================================================        
    protocol.set_rail_lights(True)
    protocol.pause('Are the right pipette tips in (20 for <= 20uL and 200' 
                   ' for >20 uL)?')
    
    if primer_combinations >= 24:
        source = primer_tubes[:primer_combinations]
        
        
    for primer in range(primer_combinations):
        if primer % 2 == 0 and primer <= 2:
            for primer_tube, pcr_strip_tube in zip(source, destination):
                ## simultanious loop through primer_tubes and PCR_strips       ##
                ## From wells to columns doesn't work, therefore all PCRstrip  ##
                ## wells are given.                                            ##
               pipette.pick_up_tip()
               pipette.aspirate(primer_volume, primer_tube)
               # pipette.air_gap(airgap_vol)
               pipette.dispense(primer_volume + 50, pcr_strip_tube)
               # pipette.air_gap(airgap_vol)
                ## air_gap to suck up any liquid that remains in the tip       ##
               pipette.drop_tip()
            ## Used aspirate/dipense instead of transfer, to allow for more    ##
            ## customization.                                                  ##
            protocol.pause('Time for new primers!')
