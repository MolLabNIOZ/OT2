# =============================================================================
# Author(s): Maartje Brouwer & Sanne Vreugdenhil
# Creation date: 210510
# Description: protocol for aliquoting 12S illumina primers, 1 eppendorf rack
#   at a time.
# =============================================================================



# ===========================IMPORT STATEMENTS=================================
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
    'protocolName': 'Aliquoting 12S Illumina primers, 1 rack at a time, 6x',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('Protocol for aliquoting 42 illumina primer pairs, '
                    '1 eppendorf rack at a time. '
                    'Pausing after every rack so that you can put the next '
                    'rack in. \n '
                    'NOTE: Start with '),
    'apiLevel': '2.9'}
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting Illumina primers from 1 tube rack filled with 1.5 mL tubes,
    to 3 PCR strips in a BioRad 96-well plate, calibrated with Westburg
    PCR strips.
    """      
# =============================================================================


# =====================LOADING LABWARE AND PIPETTES============================
# =============================================================================
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
     ##   Load the labware using load_labware_from_definition() instead of  ##
     ##   load_labware(). Then use the variable you just set with the opened##
     ##   json file to define which labware to use.                         ##

    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200_1, tips_200_2, tips_200_3, tips_200_4])#as tiprack
# =============================================================================


# ===========================VARIABLES TO SET#!!!==============================
# =============================================================================      
    p300.starting_tip = tips_200_1.well('A2')     
    primer_volume = 30
    asp_height = z=8
     ## asp_height = mm from the bottom from where to aspirate.             ##
     ## depending on the volume in the tube, for larger volumes.            ##
# =============================================================================


# ============================ALIQUOTING PRIMERS===============================
# =============================================================================
    protocol.set_rail_lights(True)
    
    protocol.pause('Put F primers F1 to F47 in slot 3, and '
                    'three empty PCR strips in columns 2, 7, and 11 with the '
                    'caps to the right in slot 6.')  
# =============================================================================
# F1 to F47 + corresponding R primers==========================================
    for primer_tube, pcr_strip_tube in zip(
            primer_tubes.wells(), 
            [pcr_strips.wells_by_name()[well_name] for well_name in 
              ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
              'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
              'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11'
              ]]):
          ## simultanious loop through primer_tubes and PCR_strips           ##
          ## From wells to columns doesn't work, therefore all PCRstrip      ##
          ## wells are given.                                                ##
        p300.pick_up_tip()
        p300.aspirate(primer_volume, primer_tube.bottom(asp_height))
        p300.air_gap(10)
        p300.dispense(primer_volume + 50, pcr_strip_tube)
        p300.air_gap()
          ## air_gap to suck up any liquid that remains in the tip           ##
        p300.drop_tip()
      ## Used aspirate/dipense instead of transfer, to allow for more        ##
      ## customization.  ##
    protocol.pause('Remove F primers and put corresponding'
                   ' R primers on slot 3.')       
        
    for primer_tube, pcr_strip_tube in zip(
            primer_tubes.wells(), 
            [pcr_strips.wells_by_name()[well_name] for well_name in 
              ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
              'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
              'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11'
              ]]):
        p300.pick_up_tip()
        p300.aspirate(primer_volume, primer_tube.bottom(asp_height))
        p300.air_gap(10)
        p300.dispense(primer_volume + 50, pcr_strip_tube)
        p300.air_gap()
        p300.drop_tip()
    protocol.pause('Remove R primers and PCR strips, '
                    'put new strips in columns 2, 7 and 11 with caps to '
                    'the right and put F49 to F83 on slot 3.')
# =============================================================================
# F49 to F83 + corresponding R primers=========================================
    for primer_tube, pcr_strip_tube in zip(
            primer_tubes.wells(), 
            [pcr_strips.wells_by_name()[well_name] for well_name in 
              ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
              'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
              'A11', 'B11'
              ]]):
        p300.pick_up_tip()
        p300.aspirate(primer_volume, primer_tube.bottom(asp_height))
        p300.air_gap(10)
        p300.dispense(primer_volume + 50, pcr_strip_tube)
        p300.air_gap()
        p300.drop_tip()
    protocol.pause('Remove F primers and put corresponding'
                    ' R primers on slot 3.')
    
    for primer_tube, pcr_strip_tube in zip(
            primer_tubes.wells(), 
            [pcr_strips.wells_by_name()[well_name] for well_name in 
              ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
              'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
              'A11', 'B11'
              ]]):
        p300.pick_up_tip()
        p300.aspirate(primer_volume, primer_tube.bottom(asp_height))
        p300.air_gap(10)
        p300.dispense(primer_volume + 50, pcr_strip_tube)
        p300.air_gap()
        p300.drop_tip()
# =============================================================================    
    protocol.set_rail_lights(False)
# =============================================================================
