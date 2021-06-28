# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 2106125
# Description: protocol for a qPCR to test mixing quality when diluting samples
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
    'protocolName': '210624-dilute-mix_test',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('qPCR - aliquoting water and mix,'
                    'then diluting + adding samples.' 
                    'mixing during diluting in different ways'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    During the qPCR (project_related/Dina/21june_qPCRs_DINA_EVE.py) we take
    sample, dilute it 100x (pipetting up-and-down 3x with 4.5uL) and then 
    directly transfer the dilution to the PCR plate. With the sample_mix, which
    was added to the plate 8x I saw a lot of variation in Cq values. I'm under
    the impression mixing was not sufficient. In this protocol I want to 
    compare some different mixing techniques, to see if that can be improved.
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


    # ##### !!! FOR ROBOT      
    # sample_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',         #labware definition
    #     1,                                      #deck position
    #     'sample_strips_1')                      #custom name
    # dilution_strips = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',         #labware definition
    #     4,                                      #deck position
    #     'dilution_strips')                      #custom name
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
            dilution_strips = protocol.load_labware_from_definition( 
            labware_def_pcrstrips, #variable derived from opening json
            4, 
            'dilution_strips')    
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
    start_vol_mix = 2178 
      ## The start_vol_m is the volume (ul) of mix that is in the source    ##
      ## labware at the start of the protocol.                              ##
    start_vol_water = 5000 
      ## The start_vol_w is the volume (ul) of water that is in the source  ##
      ## labware at the start of the protocol.                              ##
      ##!!! Fill up to above 5mL line                                       ##
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
    p300.starting_tip = tips_200.well('A1')
    p20.starting_tip = tips_20_1.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##

    #### Which wells/tubes are used 
    mastermix = tubes_5mL['C1']
    H2O = ([tubes_5mL.wells_by_name()[well_name] for well_name in
         ['B1', 'B2', 'B3']])
    sample = sample_strips_1['A1']
    
      ## where to put mastermix   
    PCR_plate = []
    PCR_plate_columns = (
        [plate_96_qPCR.columns_by_name()[column_name] for column_name in
         ['1','2','3','5','6','7','8','9','10','11']])
    for column in PCR_plate_columns:
        for well in column:
            PCR_plate.append(well)
    
    for well in ([plate_96_qPCR.wells_by_name()[well_name] for well_name in
         ['G12','H12']]):
        PCR_plate.append(well)
      ## where to put water for dilutions
    dilution_plate = dilution_strips.columns_by_name()['1']
      
# =============================================================================


# PREDIFINED VARIABLES=========================================================
# =============================================================================
    container_mix = container_water  = 'tube_5mL'
    
    ##### Variables for volume tracking
    start_height_mix = vt.cal_start_height(container_mix, start_vol_mix)
    start_height_water = vt.cal_start_height(container_water, start_vol_water)
    
# =============================================================================    


# ALIQUOTING DILUTION WATER AND MASTERMIX======================================
# =============================================================================

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
                if aliquot == 'water':
                      ## continue with next tube, reset vt
                    current_height = start_height_water
                    current_height, pip_height, bottom_reached = (
                        vt.volume_tracking(
                            container, dispension_vol, current_height))
                    counter = counter + 1
                    source = H2O[counter]
                    aspiration_location = source.bottom(current_height)
                    protocol.comment("Continue with next tube of water")
                    
                elif aliquot == 'PCR_mix':    
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
    

# DILUTING AND DISTRIBUTING SAMPLE MIX=========================================
# =============================================================================
    
    for mix_method in range(8):
        
        ## where to dilute
        dilution = dilution_plate[mix_method]
        
        
          ## set variables per mix_method
        if mix_method == 0:
            ## 1: Mixing 3x with sample_vol +3. Distribute in 24 wells
            mix_vol = sample_vol_dil + 3
            number_of_mixes = 3
            destination = PCR_plate[:24]
        elif mix_method == 1:
            ## 2: Mixing 5x with sample_vol + 3
            mix_vol = sample_vol_dil + 3
            number_of_mixes = 5
            destination = PCR_plate[24:32]            
        elif mix_method == 2:
            ## 3: Mixing 7x with sample_vol + 3
            mix_vol = sample_vol_dil + 3
            number_of_mixes = 7
            destination = PCR_plate[32:40]              
        elif mix_method == 3:
            ## 4: Mixing 10x with sample_vol + 3
            mix_vol = sample_vol_dil + 3
            number_of_mixes = 10
            destination = PCR_plate[40:48]              
        elif mix_method == 4:
            ## 5: Mixing 3x with 20µL 
            mix_vol = 20
            number_of_mixes = 3
            destination = PCR_plate[48:56]  
        elif mix_method == 5:
            ## 6: Mixing 5x with 20µL 
            mix_vol = 20
            number_of_mixes = 5
            destination = PCR_plate[56:64]  
        elif mix_method == 6:
            ## 7: Mixing 7x with 20µL 
            mix_vol = 20
            number_of_mixes = 7
            destination = PCR_plate[64:72]              
        elif mix_method == 7:
            ## 8: Mixing 10x with 20µL 
            mix_vol = 20
            number_of_mixes = 10
            destination = PCR_plate[72:80]     

        


        #### diluting sample                                                    ##
        p20.pick_up_tip()
          ## p20 picks up tip from location of specified starting_tip or        ##
          ## the following.                                                     ##
        p20.aspirate(sample_vol_dil, sample)
          ## aspirate sample_volume_dil = volume for dil. from sample_mix       ##
        p20.dispense(sample_vol_dil, dilution)
          ## dispense sample_volume_dil = volume for dilution into dil_well     ##
        
          ## Set volume for mixing up and down.                                 ##
        for i in range (number_of_mixes):
            p20.aspirate(mix_vol, dilution)
            p20.dispense(mix_vol, dilution)
              ## Mix 3 times up and down with sample volume +3.                 ##
        p20.drop_tip()
        
        #### Distribute from dilution to PCR plate                              ##
        for well in destination:
            p20.pick_up_tip()
            p20.aspirate(sample_vol_pcr, dilution)
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
            
        
              
               
    