# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 210820
# Description: qPCR protocolfor re-do 
# =============================================================================

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
number_of_samples = 38   
  ## How many samples do you want to include? 
number_std_series = 0
  ## How many dilution series do you want to include in this PCR        ##
number_of_samplemix = 8
  ## How many sample_mix to include (for normalization between qPCRs)   ##
number_of_NTCs = 2
  ## How many NTCs to include 
start_vol_mix = 1166
  ## The start_vol_m is the volume (ul) of mix that is in the source    ##
  ## labware at the start of the protocol.                              ##
sample_volume = 3
  ## How much sample (µL) to add to the PCR
dispension_vol_mix = 22 
  ## The dispension_vol_m is the volume (ul) of mastermix that needs to ##
  ## be aliquoted into the destination wells/tubes.                     ##
samples_plate_96_dil_1 = ['F2','G2','A4','D5','C7','G7','A8','G10']
samples_plate_96_dil_2 = ['A1','C1','F2','E4','G4']
samples_undil_sample_strips = ['F2','H2','B7','E7','F7','E11']
  ## In which wells are the samples located
sample_mix_well = 'G6'
  ## In which well is the sample_mix located
starting_tip_p200 = 'A3'
starting_tip_p20 = 'A4'
  ## The starting_tip is the location of first pipette tip in the box   ##
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
  # Import volume_tracking module that is on the OT2                        ##
from mollab_modules import volume_tracking_v1 as vt
#   ## Import volume_tracking module for simulator                          ##
# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'qPCRre-do',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('qPCR - aliquoting mix,'
                    'then adding samples. adding std sample.'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    protocol for re-do qPCRs with only specific samples. When after the first
    series of qPCRs you find a too large stdev or a too low copy number, you
    can use this protocol to do a qPCR with only a few samples.
    Aliquoting Phusion PCRmix with EvaGreen added from a 5 mL tube to a 
    96-wells plate; use volume tracking.
    After that, add samples to PCR mix.
    Also include a standard sample mix (distribute to an entire column).
    """
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
        'plate_96_dil_2')                       #custom name

    ##### !!! FOR ROBOT      
    # tubes_5mL = protocol.load_labware(
    #     'eppendorfscrewcap_15_tuberack_5000ul', #labware definition
    #     6,                                      #deck position
    #     'tubes_5mL')                            #custom name
    # undil_sample_strips = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',         #labware definition
    #     2,                                      #deck position
    #     'undil_sample_strips')                  #custom name
    
    # ####    !!! FOR SIMULATOR
    with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
              "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
            labware_def_5mL = json.load(labware_file)
            tubes_5mL = protocol.load_labware_from_definition( 
            labware_def_5mL, #variable derived from opening json
            6,               #deck position
            '5mL_tubes')     # custom name
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
            undil_sample_strips = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            2,                     #deck position
            'undil_sample_strips') #custom name  

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

# SETTING LOCATIONS============================================================
# =============================================================================
    ##### Setting starting tip                                              ##
    p300.starting_tip = tips_200.well(starting_tip_p200)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
      ## The starting_tip is the location of first pipette tip in the box   ##
    
    ##### Tube locations                                                    ##

    MasterMix = tubes_5mL['C1']
      ## Location of the 5mL tube with mastermix                            ##
   
    #### Where should mastermix go                                          ##
    number_of_wells = (
        number_of_samples + 
        (number_std_series * 8) + 
        number_of_samplemix +
        number_of_NTCs
        )
      ##How many wells do need to be filled with mastermix                  ##
    MasterMixAliquots = []
    for well in plate_96_qPCR.wells():
        MasterMixAliquots.append(well)
      ## Make a list with all wells of the plate                            ##
    MasterMixAliquots = MasterMixAliquots[:number_of_wells]
      ## cuts off the list after a certain number of samples                ##

      #### Where are the samples located
    samples = []
    wells_plate_96_dil = (
        [plate_96_dil_1.wells_by_name()[well_name] for well_name in
         samples_plate_96_dil_1])
    wells_plate_96_dil_2 = (
        [plate_96_dil_2.wells_by_name()[well_name] for well_name in
         samples_plate_96_dil_2])
    wells_undil_sample_strips = (
        [undil_sample_strips.wells_by_name()[well_name] for well_name in
         samples_undil_sample_strips])
    for well in wells_plate_96_dil:
        samples.append(well)
    for well in wells_plate_96_dil_2:
        samples.append(well)
    for well in wells_undil_sample_strips:
        samples.append(well)
    samples = samples + samples

      #### Where do the samples go in the PCR plate                         ##
    sample_dest = []
    for well in plate_96_qPCR.wells():
        sample_dest.append(well)
    sample_dest = sample_dest[((number_std_series * 8) + number_of_samplemix):]
      ## skip wells for dilution series and sample_mix                      ##
    sample_dest = sample_dest[:number_of_samples]
      ## cuts off the list after a certain number of samples                ##
    
      #### Where is the sample_mix located
    sample_mix = plate_96_dil_2.well(sample_mix_well)
      #### Where the sample_mix will go in the PCR plate                    ##
    sample_mix_dest = []
    sample_mix_column = str(number_std_series+1)
    for well in plate_96_qPCR.columns_by_name()[sample_mix_column]:
        sample_mix_dest.append(well)
      ## PCR will start with dilution series (if desired), followed by an   ## 
      ## entire column with sample mix. This is used to normalize between   ##
      ## PCRs                                                               ##
    sample_mix_dest = sample_mix_dest[:number_of_samplemix]
      ## Cuts of the list of wells after the desired number of sample mixes ##

# # ALIQUOTING MASTERMIX=======================================================
# # ===========================================================================      

    ##### Variables for volume tracking
    start_height_mix = vt.cal_start_height('tube_5mL', start_vol_mix)
    current_height = start_height_mix
        
    for i, well in enumerate(MasterMixAliquots):
      ## aliquot mix, for each well do the following:                       ##
    
        aspiration_vol = dispension_vol_mix + (dispension_vol_mix/100*2)
              ## Set correct variables for volume_tracking                  ##
        if i == 0: 
            p300.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    ##
        elif i % 8 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
              ## Then, after every 8th well, drop tip and pick up new       ##
    
        current_height, pip_height, bottom_reached = vt.volume_tracking(
                'tube_5mL', dispension_vol_mix, current_height)
                  ## call volume_tracking function, obtain current_height,  ##
                  ## pip_height and whether bottom_reached.                 ##
        
        if bottom_reached:
            aspiration_location = MasterMix.bottom(z=1)
            protocol.comment("You've reached the bottom of the tube!")
              ## If bottom is reached keep pipetting from bottom + 1        ##
        else:
            aspiration_location = MasterMix.bottom(pip_height)
              ## Set the location of where to aspirate from.                ##
        
        #### The actual aliquoting of mastermix                             ##
        p300.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the       ##
          ## location specified in aspiration_location.                     ##
        p300.dispense(dispension_vol_mix, well)
          ## Dispense the amount specified in dispension_vol to the         ##
          ## location specified in well (looping through plate)             ##
        p300.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill       ##
          ## completely when using a disposal volume by dispensing some     ##
          ## of the volume after each pipetting step. (blow-out too many    ##
          ## bubbles)                                                       ##
    p300.drop_tip()
      ## when done, drop tip                                                ##
      
# DISTRIBUTING SAMPLES AND SAMPLE MIX==========================================
# =============================================================================
    ##### Distributing sample
    for sample, destination_well in zip(samples, sample_dest):
        ## Combine each sample with a destination well                      ##
        p20.pick_up_tip()
          ## p20 picks up tip from location of specified starting_tip       ##
          ## or following                                                   ##
        p20.aspirate(sample_volume, sample)
          ## aspirate sample_volume from sample                             ##
        p20.dispense(sample_volume, destination_well)
          ## dispense sample_volume in destination_well                     ##
        p20.mix(3, 20, destination_well, rate=5)
          ## pipette max pipette_volume up&down 3                           ##
        p20.dispense(20, destination_well)
          ## alternative to blow_out                                        ##
        p20.drop_tip()
          ## Drop tip in trashbin on 12.                                    ##
    
    ##### Distributing sample_mix
    for destination_well in sample_mix_dest:
        p20.pick_up_tip()
          ## p20 picks up tip from location of specified tip                ##
        p20.aspirate(sample_volume, sample_mix)
          ## aspirate sample_volume from sample                             ##
        p20.dispense(sample_volume, destination_well)
          ## dispense sample_volume in destination_well                     ##
        p20.mix(3, 20, destination_well, rate=5)
          ## pipette max pipette_volume up&down 3                           ##
        p20.dispense(20, destination_well)
          ## alternative to blow_out                                        ##
        p20.drop_tip()
          ## Drop tip in trashbin on 12.                                    ##        
