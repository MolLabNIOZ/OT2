# =============================================================================
# Author(s): Maartje Brouwer & Sanne Vreugdenhil
# Creation date: 210414
# Description: protocol for aliquoting 16S illumina primers, 1 eppendorf rack
#   at a time.
# =============================================================================

##### Import statements
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
  
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
  
# =============================================================================

##### Metadata
metadata = {
    'protocolName': 'Aliquoting Illumina primers, 1 rack at a time',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('Protocol for aliquoting 128 illumina primers, 1 eppendorf' 
                    ' rack at a time. Pausing after every rack so that'
                    ' you can put the next rack in.'
                    'NOTE: PUT STRIPS IN COLUMNS 2, 7, 11 WITH THE CAPS TO'
                    ' THE RIGHT'),
    'apiLevel': '2.9'}

##### Define function
def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting Illumina primers from 1 tube rack filled with 1.5 mL tubes,
    to 3 PCR strips in a BioRad 96-well plate, calibrated with Westburg
    PCR strips.
    """
      
# =============================================================================
    ##### Loading labware
    ## For available labware see "labware/list_of_available_labware".       ##
    tips_200_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        10,                                  #deck position
        '200tips')                          #custom name
    tips_200_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        7,                                  #deck position
        '200tips')                          #custom name
    tips_200_3 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        4,                                  #deck position
        '200tips')                          #custom name
    tips_200_4 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        1,                                  #deck position
        '200tips')                          #custom name
    primer_tubes = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        3,                                                       #deck position
        'primer_tubes')                                        #custom name
    ##### !!! OPTION 1: ROBOT      
    pcr_strips = protocol.load_labware(
        'pcrstrips_96_wellplate_200ul',     #labware definition
        6,                                  #deck position
        'pcr_strips')                        #custom name
    ##### !!! OPTION 2: SIMULATOR
    # with open("labware/pcrstrips_96_wellplate_200ul/"
    #           "pcrstrips_96_wellplate_200ul.json") as labware_file:
    #         labware_def_pcrstrips = json.load(labware_file)
    # pcr_strips = protocol.load_labware_from_definition( 
    #         labware_def_pcrstrips, #variable derived from opening json
    #         6, 
    #         'pcr_strips') 
        #Load the labware using load_labware_from_definition() instead of  ##
        #load_labware(). Then use the variable you just set with the opened##
        #json file to define which labware to use.                         ##
    
    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200_1, tips_200_2, tips_200_3, tips_200_4])#as tiprack
    
# =============================================================================

# =============================================================================
#     ##### !!! Variables to set       
    p300.starting_tip = tips_200_1.well('H1')     
    primer_volume = 30
# =============================================================================

# =============================================================================
    ##### Aliquoting the primers
    
    protocol.set_rail_lights(True)
    
    protocol.pause('Put F primers F1 to F47 in, and'
                   '3 empty PCR strips in columns 2, 7, and 11 with the caps '
                   'to the right.')
    
    # F1 to F47 + corresponding R primers
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    protocol.pause('Remove F primers and put corresponding'
                   ' R primers on slot 3.')
    
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    protocol.pause('Remove R primers and PCR strips, '
                   'put new strips in columns 2, 7 and 11 with caps to '
                   'the right and put F49 to F95 on slot 3.')
    
    # F49 to F95 + corresponding R primers
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    protocol.pause('Remove F primers and put corresponding'
                   ' R primers on slot 3.')
    
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    protocol.pause('Remove R primers and PCR strips, '
                   'put new strips in columns 2, 7 and 11 with caps to '
                   'the right and put F97 to F143 on slot 3.')
    
    # F97 to F143 + corresponding R primers
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    protocol.pause('Remove F primers and put corresponding'
                   ' R primers on slot 3.')
    
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    protocol.pause('Remove R primers and PCR strips, '
                   'put new strips in columns 2, 7 and 11 with caps to '
                   'the right and put F145 to F191 on slot 3.')
    
    # F145 to F191 + corresponding R primers
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    protocol.pause('Remove F primers and put corresponding'
                   ' R primers on slot 3.')
    
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    protocol.pause('Remove R primers and PCR strips, '
                   'put new strips in columns 2, 7 and 11 with caps to '
                   'the right and put F193 to F239 on slot 3.')
    
    # F193 to F239 + corresponding R primers
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    protocol.pause('Remove F primers and put corresponding'
                   ' R primers on slot 3.')
    
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    protocol.pause('Remove R primers and PCR strips, '
                   'put new strips in column 7 with caps to '
                   'the right and put F241 to F255 in columns 1+2'
                   ' + corresponding R primers in columns 5+6 on slot 3.')
    
    # F241 to F255 + corresponding R primers
     #Forward:
    p300.transfer(
        primer_volume,
        [primer_tubes.columns_by_name()[column_name] for column_name in 
         ['1', '2']],
        pcr_strips.columns_by_name()['7'],
        new_tip='always',
        air_gap=1)
     #Reverse:
    p300.transfer(
        primer_volume,
        [primer_tubes.columns_by_name()[column_name] for column_name in 
         ['5', '6']],
        pcr_strips.columns_by_name()['7'],
        new_tip='always',
        air_gap=1)
    
    protocol.set_rail_lights(False)
    
# =============================================================================
