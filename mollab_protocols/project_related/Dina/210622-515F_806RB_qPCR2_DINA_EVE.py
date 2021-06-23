# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 2106123
# Description: general qPCR protocol. Samples will be diluted, than added to
# PCR. Adjust number of samples and diltion series as desired. Locations n
# plates will be updated accordingly.
# =============================================================================


# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
#   # Import volume_tracking module that is on the OT2                       ##
from mollab_modules import volume_tracking_v1 as vt
  ## Import volume_tracking module for simulator                             ##
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
    Second qPCR of a batch. Still all first reactions. All need to be diluted.
    First aliquot water for diluting samples into a 96_wells plate. 
    The source = 3 5mL tubes. Use volume tracking, which resets after every
    tube. 
    Then aliquoting Phusion PCRmix with EvaGreen added from a 5 mL tube to a 
    96-wells plate; use volume tracking.
    After that, dilute samples 100x and add to PCR mix.
    Also include a standard sample mix (dilute one time but distribute to an
    entire column.
    No dilution series.
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
    plate_96_dil = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        #labware definition
        4,                                      #deck position
        'plate_96_dil')                         #custom name   

    # ##### !!! FOR ROBOT      
    # sample_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',         #labware definition
    #     1,                                      #deck position
    #     'sample_strips_1')                      #custom name
    # sample_strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',         #labware definition
    #     2,                                      #deck position
    #     'sample_strips_2')                      #custom name
    # tubes_5mL = protocol.load_labware(
    #     'eppendorfscrewcap_15_tuberack_5000ul', #labware definition
    #     6,                                      #deck position
    #     'tubes_5mL')                            #custom name    
    
    ####    !!! FOR SIMULATOR
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
            sample_strips_1 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            1, 
            'sample_strips_1')
            sample_strips_2 = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            2, 
            'sample_strips_2')
    with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
              "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
            labware_def_5mL = json.load(labware_file)
            tubes_5mL = protocol.load_labware_from_definition( 
            labware_def_5mL, #variable derived from opening json
            6, 
            '5mL_tubes')      

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


# VARIABLES TO SET#!!!=========================================================
# =============================================================================
    number_of_samples = 64
      ## How many samples will you include in this PCR                      ##
    number_std_series = 3
      ## How many dilution series do you want to include in this PCR        ##    
    start_vol_mix = 2332 
      ## The start_vol_m is the volume (ul) of mix that is in the source    ##
      ## labware at the start of the protocol.                              ##
    start_vol_water = 5000 
      ## The start_vol_w is the volume (ul) of water that is in the source  ##
      ## labware at the start of the protocol.                              ##
    dispension_vol_mix = 22 
      ## The dispension_vol_m is the volume (ul) of mastermix that needs to ##
      ## be aliquoted into the destination wells/tubes.                     ##
    dispension_vol_water = 148.5
      ## The dil_vol_w is the volume of water to be pipetted for the        ##
      ## dilution.                                                          ##
    sample_vol_dil = 1.5
      ## The dil_vol_s is the volume of sample to be pipetted for the       ##
      ## 100x dilution.                                                     ##
    sample_vol_pcr = 3 
      ## The sample_vol is the volume (ul) of sample added to the PCR       ##
      ## reaction.                                                          ##
    p300.starting_tip = tips_200.well('H4')
    p20.starting_tip = tips_20_1.well('A8')
      ## The starting_tip is the location of first pipette tip in the box   ##

    #### Which wells/tubes are used 
    mastermix = tubes_5mL['C1']
    H2O = ([tubes_5mL.wells_by_name()[well_name] for well_name in
         ['B1', 'B2', 'B3']])
    sample_mix = sample_strips_2['H12']
      
# =============================================================================


# PREDIFINED VARIABLES=========================================================
# =============================================================================
    container_mix = container_water  = 'tube_5mL'
    
    ##### Variables for volume tracking
    start_height_mix = vt.cal_start_height(container_mix, start_vol_mix)
    start_height_water = vt.cal_start_height(container_water, start_vol_water)
    
    ##### Location determination for different steps
    columns_odd = ['1','3','5','7','9','11']
    columns_all = ['1','2','3','4','5','6','7','8','9','10','11','12']
    
      ## Where the samples are located                                      ##
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

      ## Where the samples go in the PCR plate                              ##
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
# =============================================================================    


# ALIQUOTING DILUTION WATER AND MASTERMIX======================================
# =============================================================================
    number_of_mix_wells = number_of_samples + 8 + (number_std_series * 8)
      ## number of wells in the plate, mastermix will be aliquoted to       ##
      ## number_of_samples + 8x sample_mix for uniforming over PCRs         ##
      ## + 8 wells per dilution series                                      ##
    
    PCR_plate = plate_96_qPCR.wells()
    PCR_plate = PCR_plate[:number_of_mix_wells]
    dilution_plate = plate_96_dil.wells()
    dilution_plate = dilution_plate[:number_of_samples+1]  
      ## How many wells do need to be filled depends on the number of       ##
      ## samples and dilution series. (+1 is for sample_mix                 ##

    aliquots = ['water', 'PCR_mix']
      ## what will be aliquoted in this protocol
      
    for aliquot in aliquots:
        if aliquot == 'PCR_mix':
            source = mastermix
            destination = PCR_plate
            current_height = start_height_mix
            container = container_mix
            dispension_vol = dispension_vol_mix
        
        elif aliquot == 'water':
            counter = 0 # how many tubes emptied
            source = H2O[counter]
            destination = dilution_plate
            current_height = start_height_water
            container = container_water
            dispension_vol = dispension_vol_water
            
        for i, well in enumerate(destination):
          ## aliquot mix in entire qPCR plate, for each well do the following:  
           
            aspiration_vol = dispension_vol + (dispension_vol/100*2)
              ## Set correct variables for volume_tracking
            
            if i == 0: 
                p300.pick_up_tip()
                  ## If we are at the first well, start by picking up a tip.##
            elif i % 8 == 0:
                p300.drop_tip()
                p300.pick_up_tip()
                  ## Then, after every 8th well, drop tip and pick up new   ##
            
            current_height, pip_height, bottom_reached = vt.volume_tracking(
                container, dispension_vol, current_height)
                  ## call volume_tracking function, obtain current_height,  ##
                  ## pip_height and whether bottom_reached.                 ##
            
            if bottom_reached:
                if aliquot == 'dilution_plate':
                      ## continue with next tube, reset vt
                    current_height = start_height_water
                    current_height, pip_height, bottom_reached = (
                        vt.volume_tracking(
                            container, dispension_vol, current_height))
                    counter = counter + 1
                    source = H2O[counter]
                    aspiration_location = source.bottom(current_height)
                    protocol.comment("Continue with next tube of water")
                    
                elif aliquot == 'PCR_plate':    
                    aspiration_location = source.bottom(z=1)
                    protocol.comment("You've reached the bottom of the tube!")
            
            else:
                aspiration_location = source.bottom(pip_height)
                  ## Set the location of where to aspirate from.            ##
    
            #### The actual aliquoting of mastermix
            p300.aspirate(aspiration_vol, aspiration_location)
              ## Aspirate the amount specified in aspiration_vol from the   ##
              ## location specified in aspiration_location.                 ##
            p300.dispense(dispension_vol, well)
              ## Dispense the amount specified in dispension_vol to the     ##
              ## location specified in well (looping through plate)         ##
            p300.dispense(10, aspiration_location)
              ## Alternative for blow-out, make sure the tip doesn't fill   ##
              ## completely when using a disposal volume by dispensing some ##
              ## of the volume after each pipetting step. (blow-out too many##
              ## bubbles)                                                   ##
        p300.drop_tip()
          ## when entire plate is full, drop tip                            ##
# =============================================================================


# DILUTING AND DISTRIBUTING SAMPLES============================================
# =============================================================================
    for sample, dilution_well, pcr_well in zip(
            samples,
            dilution_plate,
            sample_dest            
            ):
      ## Combine each sample with a dilution_well and a destination well    ##
          p20.pick_up_tip()
          ## p20 picks up tip from location of specified starting_tip       ##
          ## or following                                                   ##
          p20.aspirate(sample_vol_dil, sample)
          ## aspirate sample_volume_dil = volume for dilution from sample   ##
          p20.dispense(sample_vol_dil, dilution_well)
          ## dispense sample_volume_dil = volume for dilution into dil_well ##
          mix_vol = sample_vol_dil + 3
          ## Set volume for mixing up and down.                             ##
          for i in range (3):
            p20.aspirate(mix_vol, dilution_well)
            p20.dispense(mix_vol, dilution_well)
              ## Mix 3 times up and down with sample volume +3.             ##
          p20.aspirate(sample_vol_pcr, dilution_well)
          ## aspirate sample_vol_mix = volume for in mastermix from dil_well##
          p20.dispense(sample_vol_pcr, pcr_well)
          ## dispense sample_vol_mix = volume for in mastermix into pcr_well##
          mix_vol = sample_vol_pcr + 3
          ## Set volume for mixing up and down.                             ##
          for i in range (3):
            p20.aspirate(mix_vol, pcr_well)
            p20.dispense(mix_vol, pcr_well)
              ## Mix 3 times up and down with sample volume +3.             ##
          sample_dispense = mix_vol + 3
          ## Set extra dispension volume after mixing to mix volume +3.     ##
          p20.dispense(sample_dispense, pcr_well)
          ## Dispese the mix volume + 3 in the well.                        ##
          p20.drop_tip()
          ## Drop tip in trashbin on 12.                                    ##

# DILUTING AND DISTRIBUTING SAMPLE MIX=========================================
# =============================================================================

    #### diluting sample mix.                                               ##
    p20.pick_up_tip()
      ## p20 picks up tip from location of specified starting_tip or        ##
      ## the following.                                                     ##
    p20.aspirate(sample_vol_dil, sample_mix)
      ## aspirate sample_volume_dil = volume for dil. from sample_mix       ##
    p20.dispense(sample_vol_dil, dilution_plate[-1])
      ## dispense sample_volume_dil = volume for dilution into dil_well     ##
    mix_vol = sample_vol_dil + 3
      ## Set volume for mixing up and down.                                 ##
    for i in range (3):
        p20.aspirate(mix_vol, dilution_plate[-1])
        p20.dispense(mix_vol, dilution_plate[-1])
          ## Mix 3 times up and down with sample volume +3.                 ##
    p20.drop_tip()
    
    #### Distribute from dilution plate to entire column in PCR plate       ##
    for well in sample_mix_dest:
        p20.pick_up_tip()
        p20.aspirate(sample_vol_pcr, dilution_plate[-1])
          ## aspirate sample_vol_pcr = volume for in mastermix from dil_well##
        p20.dispense(sample_vol_pcr, well)
          ## dispense sample_vol_mix = volume for in mastermix into pcr_well##
        mix_vol = sample_vol_pcr + 3
          ## Set volume for mixing up and down.                             ##
        for i in range (3):
            p20.aspirate(mix_vol, well)
            p20.dispense(mix_vol, well)
              ## Mix 3 times up and down with sample volume +3.             ##
        sample_dispense = mix_vol + 3
          ## Set extra dispension volume after mixing to mix volume +3.     ##
        p20.dispense(sample_dispense, well)
          ## Dispese the mix volume + 3 in the well.                        ##
        p20.drop_tip()
          ## Drop tip in trashbin on 12.                                    ##
        
        
              
               
        
