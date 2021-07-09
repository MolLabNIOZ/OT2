# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 210708
# Description: general qPCR protocol. 
# =============================================================================


# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
#   # Import volume_tracking module that is on the OT2                        ##
from mollab_modules import volume_tracking_v1 as vt
  ## Import volume_tracking module for simulator                          ##
# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': '210622-515F_806RB_qPCR1_DINA_EVE',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('qPCR - aliquoting water and mix,'
                    'then diluting + adding samples. adding std sample.' 
                    'Std dilution series should be added by hand.'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    General protocol for multiple qPCRs of a batch. 
    Define if and how many dilution series you want to include. Usually only
    in the first PCR of a batch, 3 dilution series are included.
    Aliquoting Phusion PCRmix with EvaGreen added from a 5 mL tube to a 
    96-wells plate; use volume tracking.
    After that, add samples to PCR mix.
    Also include a standard sample mix (dilute one time but distribute to an
    entire column).
    Dilution series should be added by hand in the first (how many you chose) 
    columns.
    """
# =============================================================================

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
    number_of_samples = 64  # 
      ## How many samples do you want to include? 
    number_std_series = 3
      ## How many dilution series do you want to include in this PCR        ##
    number_of_samplemix = 8
      ## How many sample_mix to include (for normalization between qPCRs)   ##
    start_vol_mix = 2332
      ## The start_vol_m is the volume (ul) of mix that is in the source    ##
      ## labware at the start of the protocol.                              ##
    sample_volume = 3
      ## How much sample (µL) to add to the PCR
    dispension_vol_mix = 22 
      ## The dispension_vol_m is the volume (ul) of mastermix that needs to ##
      ## be aliquoted into the destination wells/tubes.                     ##
    first_sample = 'A1'
      ## In which well is the first sample of this PCR located
    starting_tip_p200 = 'A1'
    starting_tip_p20 = 'A1'
      ## The starting_tip is the location of first pipette tip in the box   ##
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading labware
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',     #labware definition
        3,                                      #deck position
        'tips_200')                             #custom name
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',      #labware definition
        10,                                     #deck position
        'tips_20')                              #custom name       
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',      #labware definition
        7,                                      #deck position
        'tips_20')                              #custom name       
    plate_96_qPCR = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        #labware definition
        5,                                      #deck position
        'plate_96_qPCR')                        #custom name
    plate_96_dil_1 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        #labware definition
        4,                                      #deck position
        'plate_96_dil')                         #custom name
    plate_96_dil_2 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        #labware definition
        1,                                      #deck position
        'plate_96_dil_2')                         #custom name 

    ##### !!! FOR ROBOT      
    tubes_5mL = protocol.load_labware(
        'eppendorfscrewcap_15_tuberack_5000ul', #labware definition
        6,                                      #deck position
        'tubes_5mL')                            #custom name    
    
    # ####    !!! FOR SIMULATOR
    # with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
    #           "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
    #         labware_def_5mL = json.load(labware_file)
    #         tubes_5mL = protocol.load_labware_from_definition( 
    #         labware_def_5mL, #variable derived from opening json
    #         6, 
    #         '5mL_tubes')      

    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1, tips_20_2])   #assigned tiprack
    
# =============================================================================

# SETTING LOCATIONS#!!!============================================================
# =============================================================================
    ##### Setting starting tip
    p300.starting_tip = tips_200.well(starting_tip_p200)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
      ## The starting_tip is the location of first pipette tip in the box   ##
    
    ##### Tube locations
    MasterMix = tubes_5mL['C1']
      ## Location of the 5mL tube with mastermix                            ##
      
    samples = []
    sample_columns = (                                                           
        ([sample_strips_1.columns_by_name()[column_name] 
          for column_name in columns_odd]) 
        + 
        ([sample_strips_2.columns_by_name()[column_name] 
          for column_name in columns_odd])
        )
    for column in sample_columns:
        for well in column:
            samples.append(well)
      ## makes a list of all wells in 2 full plates of PCR strips           ##
    samples = samples[:number_of_samples]
      ## cuts off the list after certain number of samples                  ##
    
    number_of_wells = (
        number_of_samples + 
        number_std_series + 
        number_of_samplemix)
      ##How many wells do need to be filled with mastermix                  ##
    MasterMixAliquots = []
    for well in plate_96_qPCR.wells():
        MasterMixAliquots.append(well)
      ## Make a list with all wells of the plate                            ##
    MasterMixAliquots = MasterMixAliquots[:number_of_wells]
      ## cuts off the list after a certain number of samples                ##
    
    ##### Where the samples go in the PCR plate                              ##
    sample_dest = []
    sample_dest_columns = (
        [plate_96_qPCR.columns_by_name()[column_name] for column_name in
         columns_all[number_std_series+1:]]
         )
      ## skip columns for dilution series and 1 column for sample_mix       ##
    for column in sample_dest_columns:
        for well in column:
            sample_dest.append(well)
      ## makes a list of all wells after dilution series and sample_mix     ##
    sample_dest = sample_dest[:number_of_samples]
      ## cuts off the list after a certain number of samples                ##
    
      ## Where the sample_mix will go in the PCR plate                      ##
    sample_mix_dest = []
    sample_mix_column = str(number_std_series+1)
    for well in plate_96_qPCR.columns_by_name()[sample_mix_column]:
        sample_mix_dest.append(well)
      ## PCR will start with dilution series (if desired), followed by an   ## 
      ## entire column with sample mix. This is used to normalize between   ##
      ## PCRs                                                               ##    
    
    
    