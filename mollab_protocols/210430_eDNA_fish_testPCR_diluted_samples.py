# =============================================================================
# Author(s): Maartje Brouwer & Sanne Vreugdenhil
# Creation date: 210421
# Description: qPCR protocol - with dilution of sample included
# =============================================================================

# ==========================IMPORT STATEMENTS==================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
  
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# =============================================================================


# =====================VOLUME TRACKING FUNCTIONS===============================
# =============================================================================
## Because we could not manage to get the robot working with separate       ##
## modules and we do want to try-out the protocol, in this version the      ##
## module is integrated into the main protocol.                             ##

##### Import statements
import math
  ## Import math module to allow using π in calculations                    ##

##### Define function
def cal_start_height(container, start_vol):
    """Module to calculate the liquid height in a tube at the start"""
    ##### Defining container dimensions
    ## Depending on the type of container, these are the dimensions         ##
    if container == 'tube_5mL':
        diameter_top = 13.3         #diameter of the top of the tube in mm
        diameter_tip = 3.3          #diameter of the tip of the tube in mm
        height_conical_tip = 55.4 - 34.12 - 2.2 #tube - straight part - rim
    elif container == 'tube_1.5mL':
        diameter_top = 8.7          #diameter of the top of the tube in mm
        diameter_tip = 3.6          #diameter of the tip of the tube in mm
        height_conical_tip = 37.8 - 20          #tube - straight part
    elif container == 'tube_2mL':
        diameter_top = 8.8         #diameter of the tipstart in mm
        diameter_tip = 2.4         #diameter of the tip of the tube in mm
        height_conical_tip = 6.8    #height conical part
    
    radius_top = diameter_top / 2         #radius of the top of the tube in mm
    radius_tip = diameter_tip / 2         #radius of the tip of the tube in mm
    vol_conical_tip = ((1/3) * math.pi * height_conical_tip *
                    ((radius_tip**2) + (radius_tip*radius_top) +
                     (radius_top**2)))
    ## How much volume fills up the conical tip: v = (1/3)*π*h*(r²+r*R+R²)  ##
    
    ##### Calculating start height
    cylinder_vol = start_vol - vol_conical_tip    # vol in straight part
    start_height = (
            height_conical_tip +         
            (cylinder_vol / (math.pi*((radius_top)**2)))
            )
    # current_height = height conical part + height cylindrical part
    
    return start_height
    

def volume_tracking(container, dispension_vol, current_height):
    """
    At this moment the OT-2 doesn't have a volume tracking function.
    By default, aspiration occurs from the bottom of a container. When a
    container is filled with liquid, this can cause the pipette to be 
    submurged beyond the pipette tip, possibly damaging the pipette. 
    Furthermore, when a container is already full, it will overflow when the 
    pipette is reaching for the bottom. Also, when the pipette goes far into 
    the liquid, a lot of liquid will stick to the outside of the pipette tip.
    This will make pipetting less acurate and increases the risk of cross-
    contamination.
    
    This module introduces calculations for liquid levels in tubes
    and allows for tracking the height of the liquid in a container 
    during a protocol.
    
    Input for this function is:
        container = type of container. Several options are available:
            'tube_5mL'
            'tube_1.5mL'
        current_vol = current volume during the run. At the start of the
        protocol this should be set at the start_vol of the protocol.
        aspiration_vol = the volume that will be aspirated in the tracked steps
    
    Output of this function is:
        current_height = the height of the current liquid level in mm from the 
        bottom of the container.
        delta_height = The height difference in mm of the liquid inside the 
        container between before and after aspiration. Delta_height is returned 
        so that in the main protocol a safety-step can be implemented:
        (if current_height - delta_height <= 1: some kind of error handling)
    """

    ##### Defining container dimensions
    ## Depending on the type of container, these are the dimensions         ##
    if container == 'tube_5mL':
        diameter = 13.3         #diameter of the top of the tube in mm
        height_conical_tip = 55.4 - 2.2 - 34.12 #tube - straight part - rim
    elif container == 'tube_1.5mL':
        diameter = 8.7       #diameter of the top of the tube in mm
        height_conical_tip = 37.8 - 20 #tube - straight part
    elif container == 'tube_2mL':
        diameter = 8.8         #diameter of the tipstart in mm
    ## volume of a cylinder is calculated as follows:                       ##
    ## v = π*r²*h  -->  h = v/(π*r²)                                        ##
    
    radius = diameter / 2         #radius of the top of the tube in mm
    
    ##### Calculate delta height per dispensed volume
    delta_height =  (dispension_vol/(math.pi*((radius)**2)))

    ##### Update current_height 
    current_height = current_height - delta_height
    ## The current_height (after aspiration) must be updated before the     ##
    ## actual aspiration, because during aspiration the liquid will reach   ## 
    ## that level.                                                          ##
    
    return current_height, delta_height
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': 'eDNA_fish_testPCR_diluted_samples',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('qPCR + diluting of samples before adding to mix'),
    'apiLevel': '2.9'}
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting water from a 2 mL tube to some wells in a 96-wells plate;
    using volume tracking so that the pipette starts aspirating at the 
    starting height of the liquid and goes down as the volume decreases.
    Aliquoting Phusion mastermix from a 5 mL tube to some wells in a 
    96-wells plate; using volume tracking so that the pipette starts 
    aspirating at the starting height of the liquid and goes down as the 
    volume decreases.
    Adding samples from 1.5 mL tubes to 96 wells plate with water,
    then transferring the dilutions to the plate with mix.
    """
# =============================================================================


# ======================LOADING LABWARE AND PIPETTES===========================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        3,                                  #deck position
        'tips_200')                          #custom name
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                 #deck position
        'tips_20_1')                           #custom name
    plate_96_dil = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        4,                                  #deck position
        'plate_96_dil')                     #custom name
    plate_96_mix = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        5,                                  #deck position
        'plate_96_mix')                     #custom name
    sample_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        7,                                                      #deck position
        'sample_tubes_1')                                        #custom name
    sample_tubes_2 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        1,                                                       #deck position
        'sample_tubes_2')                                        #custom name
    ##### !!!OPTION 1: ROBOT      
    tubes_5mL = protocol.load_labware(
        'eppendorf_15_tuberack_5000ul',     #labware definition
        2,                                  #deck position
        'tubes_5mL')                        #custom name
    #####    !!! OPTION 2: SIMULATOR
    # with open("labware/eppendorf_15_tuberack_5000ul/"
    #           "eppendorf_15_tuberack_5000ul.json") as labware_file: 
    #     labware_def_5mL = json.load(labware_file)
    #   # Import the file that contains all the information about the custom ##
    #   # labware. Load the file using json, store it in a variable.         ##
    # tubes_5mL = protocol.load_labware_from_definition(
    #     labware_def_5mL,                    #labware definition
    #     6,                                  #deck position
    #     'tubes_5mL')                        #custom name
        #Load the labware using load_labware_from_definition() instead of  ##
        #load_labware(). Then use the variable you just set with the opened##
        #json file to define which labware to use.                         ##
    
    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1])   #assigned tiprack
# =============================================================================


# ==========================VARIABLES TO SET#!!!===============================
# =============================================================================
    start_vol_m = 2790 
      ## The start_vol_m is the volume (ul) of mix that is in the source    ##
      ## labware at the start of the protocol.                              ##
    start_vol_w = 1000
      ## The start_vol_m is the volume (ul) of water that is in the source  ##
      ## labware at the start of the protocol.                              ##
    dispension_vol_m = 45 
      ## The dispension_vol is the volume (ul) that needs to be aliquoted   ##
      ## into the destination wells/tubes.                                  ##
    dispension_vol_w = 13.5
      ## The dil_vol_w is the volume of water to be pipetted for the        ##
      ## dilution.                                                          ##
    sample_vol_dil = 1.5
      ## The dil_vol_s is the volume of sample to be pipetted for the       ##
      ## dilution.                                                          ##
    sample_vol_mix = 5 
      ## The sample_vol is the volume (ul) of sample added to the PCR       ##
      ## reaction.                                                          ##
    p300.starting_tip = tips_200.well('B1')
    p20.starting_tip = tips_20_1.well('H1')
      ## The starting_tip is the location of first pipette tip in the box   ##
    destination_wells_w = (
        [plate_96_dil.wells_by_name()[well_name] for well_name in
         ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1',
          'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
          'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3',
          'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4',
          'A5', 'B5', 'C5', 'D5', 'E5', 'F5'
          ]])
    destination_wells_m = (
        [plate_96_mix.wells_by_name()[well_name] for well_name in
         ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1',
          'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
          'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3',
          'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4',
          'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5',
          'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6',
          'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
          ]]
        )
      ## set wells for where dilution_water and mastermix should end up in  ##
      ## the specified plates                                               ##
# =============================================================================        


# ==========================PREDIFINED VARIABLES===============================
# =============================================================================
    container_m = 'tube_5mL'
    container_w = 'tube_1.5mL'
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
      ## There are several options to choose from:                          ##
      ## 'tube_1.5ml', 'tube_2mL', 'tube_5mL', 'tube_15mL', 'tube_50mL'   	##
    aspiration_vol_m = dispension_vol_m + (dispension_vol_m/100*2)
    aspiration_vol_w = dispension_vol_w + (dispension_vol_w/100*2)
      ## The aspiration_vol is the volume (ul) that is aspirated from the   ##
      ## container.                                                         ##      
# =============================================================================

    protocol.pause('Open lids of dilution plate on 4, sample tubes 2 on 1'
                    ' and tips 200 on 3.')

# ===================== ALIQUOTING WATER FOR DILUTIONS ========================
# =============================================================================
    start_height = cal_start_height(container_w, start_vol_w)
      ## Call start height calculation function from volume tracking module.##
    current_height = start_height
      ## Set the current height to start height at the beginning of the     ##
      ## protocol.  
    p300.pick_up_tip()
      ## p300 picks up tip from location specified in variable starting_tip ##
    for well in destination_wells_w:
      ## Name all the wells in the plate 'well', for all these do:          ##  
        container = container_w 
        dispension_vol = dispension_vol_w 
        aspiration_vol = aspiration_vol_w
          ## Set variables to correct volumes.                              ##
        tv = volume_tracking(
            container, dispension_vol, current_height)  
        current_height, delta_height = tv
          ## The volume_tracking function needs the arguments container,    ##
          ## dispension_vol and the current_height which we have set in this##
          ## protocol. With those variables, the function updates the       ##
          ## current_height and calculates the delta_height of the liquid   ##
          ## after the next aspiration step. The outcome is stored as tv and##
          ## then the specific variables are updated.                       ##
        pip_height = current_height - 2
          ## Make sure that the pipette tip is always submerged by setting  ##
          ## the current height 2 mm below its actual height                ##
        if current_height - delta_height <= 1: 
            aspiration_location = sample_tubes_2['D3'].bottom(z=1) #!!!
            protocol.comment("You've reached the bottom!")
        else:
            aspiration_location = sample_tubes_2['D3'].bottom(pip_height) #!!!
          ## If the level of the liquid in the next run of the loop will be ##
          ## smaller than 1 we have reached the bottom of the tube. To      ##
          ## prevent the pipette from crashing into the bottom, we tell it  ##
          ## to go home and pause the protocol so that this can never happen##
          ## Set the location of where to aspirate from. Because we put this##
          ## in the loop, the location will change to the newly calculated  ##
          ## height after each pipetting step.                              ##
        well_c = str(well) #set location of the well to str (if takes only str)
        if (well_c == 'A2 of plate_96_dil on 4' or 
            well_c == 'A3 of plate_96_dil on 4' or
            well_c == 'A4 of plate_96_dil on 4' or
            well_c == 'A5 of plate_96_dil on 4'):
            p300.drop_tip()
            p300.pick_up_tip()
          ## Pick up a new tip every two rows.                              ##
        p300.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the        ##
          ## location specified in aspiration_location.                      ##
        p300.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the location##
          ## specified in well (so a new well every time the loop restarts) ##
        p300.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill       ##
          ## completely when using a disposal volume by dispensing some     ##
          ## of the volume after each pipetting step. (blow-out to many     ##
          ## bubbles)                                                       ##
    p300.drop_tip()                    
      ## Drop the final tip in the trash bin.                               ##
    water_height = current_height - 2
      ## set a variable for current height of the water, to be able to use  ##
      ## this height later on, for aspirating Negative Controls             ##
# =============================================================================

    protocol.pause('Close lids of dilution plate on 4, sample tubes 2 on 1'
                   ' and open lids of mix plate on 5 and 5 ml tubes on 2.')

# ===============================ALIQUOTING MIX================================
# =============================================================================
    start_height = cal_start_height(container_m, start_vol_m)
      ## Call start height calculation function from volume tracking module.##
    current_height = start_height
      ## Set the current height to start height at the beginning of the     ##
      ## protocol.                                                          ##
    p300.pick_up_tip()
      ## p300 picks up tip from location specified in variable starting_tip ##
    for well in destination_wells_m:
      ## Name all the wells in the plate 'well', for all these do:          ##
        container = container_m
        dispension_vol = dispension_vol_m 
        aspiration_vol = aspiration_vol_m
          ## Set variables to correct volumes.                              ##
        tv = volume_tracking(
            container, dispension_vol, current_height)  
        current_height, delta_height = tv
          ## The volume_tracking function needs the arguments container,    ##
          ## dispension_vol and the current_height which we have set in this##
          ## protocol. With those variables, the function updates the       ##
          ## current_height and calculates the delta_height of the liquid   ##
          ## after the next aspiration step. The outcome is stored as tv and##
          ## then the specific variables are updated.                       ##
        pip_height = current_height - 2
          ## Make sure that the pipette tip is always submerged by setting  ##
          ## the current height 2 mm below its actual height                ##
        if current_height - delta_height <= 1: 
            aspiration_location = tubes_5mL['C3'].bottom(z=1) #!!!
            protocol.comment("You've reached the bottom!")
        else:
            aspiration_location = tubes_5mL['C3'].bottom(pip_height) #!!!
          ## If the level of the liquid in the next run of the loop will be ##
          ## smaller than 1 we have reached the bottom of the tube. To      ##
          ## prevent the pipette from crashing into the bottom, we tell it  ##
          ## to go home and pause the protocol so that this can never happen##
          ## Set the location of where to aspirate from. Because we put this##
          ## in the loop, the location will change to the newly calculated  ##
          ## height after each pipetting step.                              ##
        well_c = str(well) #set location of the well to str (if takes only str)
        if (well_c == 'A2 of plate_96_mix on 5' or 
            well_c == 'A3 of plate_96_mix on 5' or
            well_c == 'A4 of plate_96_mix on 5' or
            well_c == 'A5 of plate_96_mix on 5' or
            well_c == 'A6 of plate_96_mix on 5' or
            well_c == 'A7 of plate_96_mix on 5'):
            p300.drop_tip()
            p300.pick_up_tip()
          ## Pick up a new tip every two rows.                              ##
        p300.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the        ##
          ## location specified in aspiration_location.                      ##
        p300.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the location##
          ## specified in well (so a new well every time the loop restarts) ##
        p300.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill       ##
          ## completely when using a disposal volume by dispensing some     ##
          ## of the volume after each pipetting step. (blow-out to many     ##
          ## bubbles)                                                       ##
    p300.drop_tip()                    
      ## Drop the final tip in the trash bin.                               ##
# =============================================================================

    protocol.pause('Close lids of tips 200 on 3 and open all other labware.')

# =====================DILUTING AND DISTRIBUTING SAMPLES=======================
# =============================================================================
    ##### Lists for locations
    dest_sample_tubes_1_dil = (
        [plate_96_dil.wells_by_name()[well_name] for well_name in
         ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1',
          'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
          'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3',
          ]])
      ## dest_sample_tubes_1_dil = the list of wells with water where the   ##
      ## samples from sample_tubes_1 should go                              ##
    dest_sample_tubes_1_mix = (
         [plate_96_mix.wells_by_name()[well_name] for well_name in
         ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1',
          'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
          'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3',
          ]])
      ## dest_sample_tubes_1_mix = the list of wells with mix where the     ##
      ## samples from dest_sample_tubes_1_dil should go                     ##
    
    sample_tubes_2 = (
        [sample_tubes_2.wells_by_name()[well_name] for well_name in
        ['A1', 'B1', 'C1', 'D1',
         'A2', 'B2', 'C2', 'D2',
         'A3', 'B3', 'C3', 'D3', 'D3', 'D3'          
         ]])
         ## D3 = dilution water, used as NegContr (3x)                      ##
    dest_sample_tubes_2_dil = (
        [plate_96_dil.wells_by_name()[well_name] for well_name in
         ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4',
          'A5', 'B5', 'C5', 'D5', 'E5', 'F5'
          ]])
      ## dest_sample_tubes_2_dil = the list of wells with water where the   ##
      ## samples from sample_tubes_2 should go                              ##
    dest_sample_tubes_2_mix = (
         [plate_96_mix.wells_by_name()[well_name] for well_name in
         ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4',
          'A5', 'B5', 'C5', 'D5', 'E5', 'F5'
          ]])
      ## dest_sample_tubes_2_mix = the list of wells with mix where the     ##
      ## samples from dest_sample_tubes_2_dil should go                     ##
    
    for sample_tube, dil_well, mix_well in zip(
            sample_tubes_1.wells(), 
            dest_sample_tubes_1_dil,
            dest_sample_tubes_1_mix,
            ):
          ## for the all the wells in sample_tubes_1, specified wells in    ##
          ## dest_sample_tubes_1 dil and mix, call each separate well       ##
          ## sample tube (sample_tubes_1), dil_well                         ##
          ## (dest_sample_tubes_1_dil), mix_well                            ##
          ## (dest_sample_tubes_1_mix) and do the following:                ##
        p20.pick_up_tip()
          ## p20 picks up tip from location of specified starting_tip       ##
          ## or following                                                   ##
        p20.aspirate(sample_vol_dil, sample_tube)
          ## aspirate sample_volume_dil = volume for dilution from sample_tube
        p20.dispense(sample_vol_dil, dil_well)
          ## dispense sample_volume_dil = volume for dilution into dil_well
        mix_vol = sample_vol_dil + 3
          ## Set volume for mixing up and down.                             ##
        for i in range (3):
            p20.aspirate(mix_vol, dil_well)
            p20.dispense(mix_vol, dil_well)
              ## Mix 3 times up and down with sample volume +3.             ##
        p20.aspirate(sample_vol_mix, dil_well)
          ## aspirate sample_vol_mix = volume for in mastermix from dill_well
        p20.dispense(sample_vol_mix, mix_well)
          ## dispense sample_vol_mix = volume for in mastermix into mix_well##
        mix_vol = sample_vol_mix + 3
          ## Set volume for mixing up and down.                             ##
        for i in range (3):
            p20.aspirate(mix_vol, mix_well)
            p20.dispense(mix_vol, mix_well)
              ## Mix 3 times up and down with sample volume +3.             ##
        sample_dispense = mix_vol + 3
          ## Set extra dispension volume after mixing to mix volume +3.     ##
        p20.dispense(sample_dispense, mix_well)
          ## Dispese the mix volume + 3 in the well.                        ##
        p20.drop_tip()
          ## Drop tip in trashbin on 12.                                    ##

    for sample_tube, dil_well, mix_well in zip(
            sample_tubes_2, 
            dest_sample_tubes_2_dil,
            dest_sample_tubes_2_mix,
            ):
          ## for specified wells in sample_tubes_2, dest_sample_tubes_2 dil ##
          ## and mix, call each separate well                               ##
          ## sample tube (sample_tubes_2), dil_well                         ##
          ## (dest_sample_tubes_2_dil), mix_well                            ##
          ## (dest_sample_tubes_2_mix) and do the following:                ##
        p20.pick_up_tip()
          ## p20 picks up tip from location of specified starting_tip       ##
          ## or following
        sample_tube_string = str(sample_tube)                                                   ##
        if sample_tube_string == 'D3 of sample_tubes_2 on 1':
            sample_tube = sample_tubes_2[11].bottom(water_height)
        p20.aspirate(sample_vol_dil, sample_tube)
          ## aspirate sample_volume_dil = volume for dilution from sample_tube
        p20.dispense(sample_vol_dil, dil_well)
          ## dispense sample_volume_dil = volume for dilution into dil_well
        mix_vol = sample_vol_dil + 3
          ## Set volume for mixing up and down.                             ##
        for i in range (3):
            p20.aspirate(mix_vol, dil_well)
            p20.dispense(mix_vol, dil_well)
              ## Mix 3 times up and down with sample volume +3.             ##
        p20.aspirate(sample_vol_mix, dil_well)
          ## aspirate sample_vol_mix = volume for in mastermix from dill_well
        p20.dispense(sample_vol_mix, mix_well)
          ## dispense sample_vol_mix = volume for in mastermix into mix_well##
        mix_vol = sample_vol_mix + 3
          ## Set volume for mixing up and down.                             ##
        for i in range (3):
            p20.aspirate(mix_vol, mix_well)
            p20.dispense(mix_vol, mix_well)
              ## Mix 3 times up and down with sample volume +3.             ##
        sample_dispense = mix_vol + 3
          ## Set extra dispension volume after mixing to mix volume +3.     ##
        p20.dispense(sample_dispense, mix_well)
          ## Dispese the mix volume + 3 in the well.                        ##
        p20.drop_tip()
          ## Drop tip in trashbin on 12.                                    ##
                
# =============================================================================
