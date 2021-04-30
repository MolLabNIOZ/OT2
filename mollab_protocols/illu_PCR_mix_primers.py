
# =============================================================================
# Author(s): Maartje Brouwer & Sanne Vreugdenhil
# Creation date: 210419
# Description: protocol to aliquot PCR mix into PCR strips
#   and then add barcoded primers to them.
# =============================================================================

##### Import statements
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##

import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##


# =============================================================================
# Volume Tracking Module
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
    elif container == 'tube_15mL':
        diameter_top =  13.35       #diameter of the top of the tube in mm
        diameter_tip = 2.16         #diameter of the tip of the tube in mm
        height_conical_tip = 22.1   #height conical part
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
            'tube_15mL'
            'tube_2mL'
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
    elif container == 'tube_1.5mL':
        diameter = 8.7       #diameter of the top of the tube in mm
    elif container == 'tube_15mL':
        diameter = 13.35       #diameter of the tipstart in mm
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

##### Metadata
metadata = {
    'protocolName': 'illu_PCR_mix_primers',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('Illumina PCR - aliquoting mix and primers'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting Phusion mastermix from a 2 mL tube to 6 PCR strips in 
    2 96-wells plates; using volume tracking so that the pipette starts 
    aspirating at the starting height of the liquid and goes down as the 
    volume decreases.
    Adding primers from PCR strips (with 10 uM primer F&R primer mix)
    to PCR strips (with mastermix).
    """
      
# =============================================================================
    ##### Loading labware
    ## For available labware see "labware/list_of_available_labware".       ##
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        3,                                  #deck position
        '200tips')                          #custom name
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        4,                                 #deck position
        '20tips')                           #custom name
    tubes_2mL = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',#labware def
        5,                                                     #deck position
        '2 mL tubes')                                          #custom name
    ##### !!! OPTION 1: ROBOT      
    # primer_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     6,                                 #deck position
    #     'primer strips 1')                 #custom name
    # primer_strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     7,                                #deck position
    #     'primer strips 2')                 #custom name                  
    # mix_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     8,                                 #deck position
    #     'mix strips 1')                    #custom name    
    # mix_strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     9,                                 #deck position
    #     'mix strips 2')                    #custom name                      
    ##### !!! OPTION 2: SIMULATOR      
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
    primer_strips_1 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        6,                     #deck position
        'primer_strips_1')     #custom name  
    primer_strips_2 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        7,                     #deck position
        'primer_strips_2')     #custom name                            
    mix_strips_1 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        8,                     #deck position
        'mix_strips_1')        #custom name   
    mix_strips_2 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        9,                     #deck position
        'mix_strips_1')        #custom name                  
    
    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1])     #assigned tiprack
# =============================================================================

# =============================================================================
    ##### !!! Variables to set    
    start_vol = 1800 
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##
    dispension_vol = 39 
      ## The dispension_vol is the volume (ul) that needs to be aliquoted   ##
      ## into the destination wells/tubes.                                  ##
    primer_vol = 6 
      ## The sample_vol is the volume (ul) of sample added to the PCR       ##
      ## reaction.                                                          ##
    p300.starting_tip = tips_200.well('A1')
    p20.starting_tip = tips_20_1.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##
# =============================================================================  
# =============================================================================
    ##### Predifined variables 
    container = 'tube_2mL'
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
      ## There are several options to choose from:                          ##
      ## 'tube_1.5ml', 'tube_2mL', 'tube_5mL', 'tube_15mL', 'tube_50mL'   	##
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
      ## The aspiration_vol is the volume (ul) that is aspirated from the   ##
      ## container.                                                         ##
    destination_wells_1 = (
        [mix_strips_1.wells_by_name()[well_name] for well_name in 
         ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
          'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
          'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11'
          ]])
    destination_wells_2 = (
        [mix_strips_2.wells_by_name()[well_name] for well_name in 
         ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
          'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
          'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11'
          ]]
        )
# =============================================================================       
# =============================================================================
    ##### Variables for volume tracking
    start_height = cal_start_height(container, start_vol)
      ## Call start height calculation function from volume tracking module.##
    current_height = start_height
      ## Set the current height to start height at the beginning of the     ##
      ## protocol.                                                          ##
# =============================================================================

# =============================================================================
    ##### Aliquoting the mix
    p300.pick_up_tip()
      ## p300 picks up tip from location specified in variable starting_tip ##
    for well in destination_wells_1 + destination_wells_2:
      ## Name all the wells in the plate 'well', for all these do:          ##  
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
            aspiration_location = tubes_2mL['A1'].bottom(z=1) #!!!
            protocol.comment("You've reached the bottom!")
        else:
            aspiration_location = tubes_2mL['A1'].bottom(pip_height) #!!!
          ## If the level of the liquid in the next run of the loop will be ##
          ## smaller than 1 we have reached the bottom of the tube. To      ##
          ## prevent the pipette from crashing into the bottom, we tell it  ##
          ## to go home and pause the protocol so that this can never happen##
          ## Set the location of where to aspirate from. Because we put this##
          ## in the loop, the location will change to the newly calculated  ##
          ## height after each pipetting step.                              ##
        well_c = str(well) #set location of the well to str (if takes only str)
        if (well_c == 'A3 of 96well_plate on 9' or 
            well_c == 'A5 of 96well_plate on 9' or 
            well_c == 'A7 of 96well_plate on 9' or
            well_c == 'A9 of 96well_plate on 9' or
            well_c == 'A11 of 96well_plate on 9'):
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