# =============================================================================
# Author(s): Sanne Vreugdenhil & Maartje Brouwer
# Creation date: 210916
# Description: 
#   - add samples from 1.5 mL tubes to 96 wells plate
# Update (SV) 211028: Added option for standard sample
# =============================================================================


# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import math
  ## To do some calculations (rounding up)
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# =============================================================================


# VARIABLES TO SET#!!!=========================================================
# =============================================================================
number_of_samples = 48   # max 96 - (8 * number_std_series) - NTC - mock
  ## How many samples do you want to include?                           ##
mock = False #also False if added by hand
  ## False if not added or added by hand, True if added by robot
std_sample = True
  ## True if you are doing a qPCR and add a std_sample for Svec method  ##
if std_sample:
    no_of_std_samples = 6
else:
    no_of_std_samples = 0
 ## Number of replicates of the std sample, usually 6                   ##
sample_vol = 2 
  ## The sample_vol is the volume (ul) of sample added to the PCR       ##
starting_tip_p20 = 'A3'
  ## The starting_tip is the location of first pipette tip in the box   ##
# =============================================================================


# CALCULATED VARIABLES=========================================================
# =============================================================================
if mock:
    number_of_samples = number_of_samples + 1
if std_sample:
    number_of_samples = number_of_samples + 1 
sample_racks = math.ceil(number_of_samples / 24)
  ## How many tube_racks are needed (1,2,3 or 4)
# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'general_illuPCR_EVE',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Illumina PCR - adding samples'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Adding samples from 1.5 mL tubes to a 96 wells plate.
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    
    #pipette tips
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        7,                                  #deck position
        '20tips_1')                         #custom name       
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                 #deck position
        '20tips_2')                         #custom name

    # Tube_racks & plates
    sample_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        4,                                                       #deck position
        'sample_tubes_1')                                        #custom name
    if sample_racks >= 2:
        sample_tubes_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            1,                                                       #deck pos
            'sample_tubes_2')                                        #cust name
    if sample_racks >= 3:
        sample_tubes_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            3,                                                       #deck pos
            'sample_tubes_3')                                        #cust name
    if sample_racks >= 4:
        sample_tubes_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labw def
            11,                                                      #deck pos
            'sample_tubes_4')                                        #cust name
    
    ##### !!! OPTION 1: ROBOT 
    # plate_96 = protocol.load_labware(
    #     'biorad_qpcr_plate_eppendorf_cool_rack',#labware definition
    #     5,                                      #deck position
    #     '96well_plate_rack')                    #custom name  
   ##### !!! OPTION 2: SIMULATOR
    with open("labware/biorad_qpcr_plate_eppendorf_cool_rack/"
                "biorad_qpcr_plate_eppendorf_cool_rack.json") as labware_file:
              labware_def_cool_rack = json.load(labware_file)
    plate_96 = protocol.load_labware_from_definition( 
        labware_def_cool_rack,   #variable derived from opening json
        5,                       #deck position
        '96well_plate_rack')     #custom name 
    
    # Pipettes
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1, tips_20_2])   #assigned tiprack
    
# =============================================================================

# PREDIFINED VARIABLES=========================================================
# =============================================================================
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
      ## The starting_tip is the location of first pipette tip in the box   ##

    # Sample source wells
    sample_sources = []
      ## Create an empty list to append wells to.                           ##
    sample_sources = sample_tubes_1.wells()
    if sample_racks >= 2:
        sample_sources = sample_sources + sample_tubes_2.wells()
    if sample_racks >= 3:
        sample_sources = sample_sources + sample_tubes_3.wells()    
    if sample_racks >= 4:
        sample_sources = sample_sources + sample_tubes_4.wells()
    sample_sources = sample_sources[:number_of_samples]
    if std_sample:
        std_source = [sample_sources[-1]] * (no_of_std_samples - 1)
        for well in std_source:
            sample_sources.append(well)

        
    
# ADDING SAMPLES===============================================================
# =============================================================================
    ## Loop through source and destination wells
    for sample_tube, well in zip(sample_sources, plate_96.wells()):
        p20.pick_up_tip()
        p20.aspirate(sample_vol, sample_tube)
        p20.dispense(sample_vol, well)
        sample_mix_vol = sample_vol + 3
          ## primer_mix_vol = volume for pipetting up and down              ##
        p20.mix(3, sample_mix_vol, well)
        p20.dispense(10, well)
        p20.drop_tip()
# =============================================================================
    