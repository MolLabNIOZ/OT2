well# =============================================================================
# Author(s): Maartje Brouwer
# Creation date: 210616
# Description: qPCR protocol. First qPCR of a batch, including 3x std curve
# =============================================================================


# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
  ## Import volume_tracking module that is on the OT2                       ##
from mollab_modules import volume_tracking_v1 as vt
 ## Import volume_tracking module for simulator                             ##
# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': '210622-515F_806RB_qPCR1_DINA_EVE',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('16S qPCR - aliquoting mix and primers,'
                    'then diluting + adding sample'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    First qPCR of a batch
    Aliquoting Phusion PCRmix with EvaGreen added from a 5 mL tube to a 
    96-wells plate; using volume tracking so that the pipette starts 
    aspirating at the starting height of the liquid and goes down as the 
    volume decreases.
    After that, dilute samples 100x and add to PCR mix.
    Also include a standard sample mix and 3x standard curve
    """
# =============================================================================


# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading labware
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        3,                                 #deck position
        'tips_200')                         #custom name
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                 #deck position
        'tips_20')                          #custom name       
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        7,                                 #deck position
        'tips_20')                          #custom name       
    plate_96_qPCR = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        5,                                  #deck position
        'plate_96_qPCR')                     #custom name
    plate_96_dil = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        4,                                  #deck position
        'plate_96_dil')                     #custom name   

    # ##### !!! FOR ROBOT      
    # sample_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',     #labware definition
    #     1,                                  #deck position
    #     'sample_strips_1')                  #custom name
    # sample_strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',     #labware definition
    #     2,                                  #deck position
    #     'sample_strips_2')                  #custom name
    # tubes_5mL = protocol.load_labware(
    #     'eppendorf_15_tuberack_5000ul',     #labware definition
    #     6,                                  #deck position
    #     'tubes_5mL')                        #custom name    
    
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
    with open("labware/eppendorf_15_tuberack_5000ul/"
              "eppendorf_15_tuberack_5000ul.json") as labware_file:
            labware_def_5mL = json.load(labware_file)
            tubes_5mL = protocol.load_labware_from_definition( 
            labware_def_5mL, #variable derived from opening json
            6, 
            'tubes_5mL')        

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
    p300.starting_tip = tips_200.well('A1')
    p20.starting_tip = tips_20_1.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##
      
    #### Which wells / tubes are present / used 
    PCR_plate = plate_96_qPCR.wells()
    dilution_plate = plate_96_dil.wells()
    aliquots = ['dilution_plate', 'PCR_plate']
      ## Which wells are used (in this case entire plates)
    mastermix = tubes_5mL['C1']
    H2O = ([tubes_5mL.wells_by_name()[well_name] for well_name in
         ['B1', 'B2', 'B3']])
    samples = (                                                           
        ([sample_strips_1.columns_by_name()[collumn_name] 
          for collumn_name in ['1','3', '5', '7', '9', '11']]) 
        + 
        ([sample_strips_2.columns_by_name()[collumn_name] 
          for collumn_name in ['1','3']]) 
        # for 88 samples to 9, for 64 samples to 3
        )
    sample_mix = sample_strips_2['A11']
    sample_dest = (
        [plate_96_qPCR.collumns_by_name()[collumn_name] for collumn_name in
         ['5','6', '7', '8', '9', '10', '11', '12']
        ])
        # For PCR with std dilution series, start at 5, otherwise at 2
    sample_mix_dest = plate_96_qPCR.collumns_by_name()['4']
      ## Placement of different tubes on deck
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
    for aliquot in aliquots:
        if aliquot == 'PCR_plate':
            source = mastermix
            destination = PCR_plate
            current_height = start_height_mix
            container = container_mix
            dispension_vol = dispension_vol_mix
        
        elif aliquot == 'dilution_plate':
            counter = 0 # how many tubes emptied
            source = H2O[counter]
            destination = dilution_plate
            current_height = start_height_water
            container = container_water
            dispension_vol = dispension_vol_water
            
          ## current height of mix in the mix tube is calculated start_height_mix
        for i, well in enumerate(destination):
          ## aliquot mix in entire qPCR plate, for each well do the following:  
           
            aspiration_vol = dispension_vol + (dispension_vol/100*2)
              ## Set correct variables for volume_tracking
            
            if i == 0: 
                p300.pick_up_tip()
                  ## If we are at the first well, start by picking up a tip.    ##
            elif i % 8 == 0:
                p300.drop_tip()
                p300.pick_up_tip()
                  ## Then, after every 8th well, drop tip and pick up a new one.##
            
            current_height, pip_height, bottom_reached = vt.volume_tracking(
                container, dispension_vol, current_height)
                  ## call volume_tracking function, obtain current_height,      ##
                  ## pip_height and whether bottom_reached.                     ##
            
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
                    protocol.comment("You've reached the bottom of the MM-tube!")
            
            else:
                aspiration_location = source.bottom(pip_height)
                  ## Set the location of where to aspirate from.                ##
                  ## Because we put this in the loop, the location will change  ##
                  ## to the newly calculated height after each pipetting step.  ##  
                  ## To prevent the pipette from crashing into the bottom, we   ##
                  ## tell it to keep pipetting from right above the bottom.     ##
    
            #### The actual aliquoting of mastermix
            p300.aspirate(aspiration_vol, aspiration_location)
              ## Aspirate the amount specified in aspiration_vol from the       ##
              ## location specified in aspiration_location.                     ##
            p300.dispense(dispension_vol, well)
              ## Dispense the amount specified in dispension_vol to the         ##
              ## location specified in well (looping through plate)             ##
            p300.dispense(10, aspiration_location)
              ## Alternative for blow-out, make sure the tip doesn't fill       ##
              ## completely when using a disposal volume by dispensing some     ##
              ## of the volume after each pipetting step. (blow-out too many    ##
              ## bubbles)                                                       ##
        p300.drop_tip()
          ## when entire plate is full, drop tip                                ##
# =============================================================================


# DILUTING AND DISTRIBUTING SAMPLES============================================
# =============================================================================
    for sample, dest_well, dilution_well in zip(
            samples, 
            sample_dest, 
            dilution_plate
            ):
      ## Combine each sample with a dilution_well,       
        
        
