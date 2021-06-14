# =============================================================================
# Author(s): Sanne Vreugdenhil & Maartje Brouwer
# Creation date: 210614
# Description: protocol to test volume tracking in 5mL screw_cap tubes 
# =============================================================================

# ==========================IMPORT STATEMENTS==================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
import math
## Import math module to allow using π in calculations                      ##
# =============================================================================

def cal_start_height(container, start_vol):
    """Module to calculate the liquid height in a tube at the start"""
    ##### Defining container dimensions
    ## Depending on the type of container, these are the dimensions         ##
    if container == 'tube_1.5mL':
        diameter_top = 8.7          #diameter of the top of the tube in mm
        diameter_tip = 3.6          #diameter of the tip of the tube in mm
        height_conical_tip = 17.8   #tube - straight part
    elif container == 'tube_2mL':
        diameter_top = 9.85         #diameter of the top of the tube in mm
        diameter_tip = 2.4          #diameter of the tip of the tube in mm
        height_conical_tip = 6.8    #tube - straight part
    elif container == 'tube_5mL':
        diameter_top = 13           #diameter of the top of the tube in mm
        diameter_tip = 3.3          #diameter of the tip of the tube in mm
        height_conical_tip = 66.1 - 43.6 - 1.3 #tube - straight part - bottom wall
    elif container == 'tube_5mL_snap':
        diameter_top = 13.3         #diameter of the top of the tube in mm
        diameter_tip = 3.3          #diameter of the tip of the tube in mm
        height_conical_tip = 55.4 - 2.2 - 34.12 #tube - straight part - rim
    elif container == 'tube_15mL':
        diameter_top = 15.16        #diameter of the top of the tube in mm
        diameter_tip = 2.16         #diameter of the tip of the tube in mm
        height_conical_tip = 22.1   #tube - straight part
    elif container == 'tube_50mL':
        diameter_top = 27.48        #diameter of the top of the tube in mm
        diameter_tip = 4.7          #diameter of the tip of the tube in mm
        height_conical_tip = 15.3   #tube - straight part
        
    
    radius_top = diameter_top / 2         #radius of the top of the tube in mm
    radius_tip = diameter_tip / 2         #radius of the tip of the tube in mm
    vol_conical_tip = ((1/3) * math.pi * height_conical_tip *
                    ((radius_tip**2) + (radius_tip*radius_top) +
                     (radius_top**2)))
    ## How much volume fills up the conical tip: v = (1/3)*π*h*(r²+r*R+R²)  ##
    
    ##### Calculating start height
    cylinder_vol = start_vol - vol_conical_tip    # vol in straight part
    start_height = (
            height_conical_tip +        # current_height = height conical part 
            (cylinder_vol /             # + height cylindrical part
            (math.pi*((radius_top)**2)))
            )
    ## Initially start higher in a 15mL tube. Due to the shape of the tube, ##
    ## volume tracking doesn't work perfect when assuming that the entire   ##
    ## tube is cylindrical. This is partly solved by adding 7 mm to the     ##
    ## start_height.                                                        ##
    if container == 'tube_15mL':
        start_height = start_height + 7
    
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
            'tube_1.5mL'
            'tube_2mL'
            'tube_5mL'
            'tube_5mL_snap'
            'tube_15mL'
            'tube_50mL'
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
    if container == 'tube_1.5mL':
        diameter = 8.7          #diameter of the top of the tube in mm
    elif container == 'tube_2mL':
        diameter = 9.85         #diameter of the top of the tube in mm
    elif container == 'tube_5mL':
        diameter = 13           #diameter of the top of the tube in mm
    elif container == 'tube_5mL_snap':
        diameter = 13.3         #diameter of the top of the tube in mm
    elif container == 'tube_15mL':
        diameter = 15.16        #diameter of the top of the tube in mm
        height_conical_tip = 22.1   #tube - straight part
        offset_height = height_conical_tip + 18 
        ## offset_height = height from where to start using                 ##
        ## current_height - 1 so that the pipette tip stays submerged.      ##
    elif container == 'tube_50mL':
        diameter = 27.48        #diameter of the top of the tube in mm
    
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
    if container == 'tube_15mL' and current_height < offset_height:
        current_height = current_height - 1
    ## Volume tracking when assuming the entire tube is cylindrical doesn't ##
    ## work very well with a 15 mL tube. Therefore, we need to adjust some  ##
    ## values so that we do the volume tracking as good as possible.        ##
    ## start_height is already adjusted so that we start a little heigher,  ##
    ## however at the offset_height the pipette didn't reach the liquid     ##
    ## anymore. So we lower the current_height with 1 so that the pipette   ##
    ## tip is always submerged and the entire tube is emptied.              ##
    
    return current_height, delta_height

# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': '210608_eDNA_fish_test_PCR_WALL-E',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>, MB <maartje.brouwer@nioz.nl>',
    'description': ('5mL screwcap volume tracking test'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting water from a 5mL screwcap tube into a 96wells plate
    """
# =============================================================================

# ======================LOADING LABWARE AND PIPETTES===========================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',     #labware definition
        3,                                      #deck position
        'tips_200')                             #custom name
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',        #labware definition
        4,                                      #deck position
        'plate_96')                             #custom name
   ##### !!! OPTION 1: ROBOT      
    # tubes_5mL = protocol.load_labware(
    #     'eppendorfscrewcap_15_tuberack_5000ul', #labware def
    #     2,                                      #deck position
    #     '5mL_tubes')                            #custom name
   ##### !!! OPTION 2: SIMULATOR      
    with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
              "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
            labware_def_5mL = json.load(labware_file)
    tubes_5mL = protocol.load_labware_from_definition( 
            labware_def_5mL,   #variable derived from opening json
            2,                 #deck position
            '5mL_tubes')       #custom name
    
    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack
# =============================================================================   

# ==========================VARIABLES TO SET#!!!===============================
# =============================================================================
    start_vol_1 = 5000
    start_vol_2 = 2200
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##

    p300.starting_tip = tips_200.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##
# =============================================================================

# ==========================PREDIFINED VARIABLES===============================
# =============================================================================
    container = 'tube_5mL'
# =============================================================================
    ##### Variables for volume tracking
    start_height_1 = cal_start_height(container, start_vol_1)
    start_height_2 = cal_start_height(container, start_vol_2)
    
# =============================================================================
    
# ===============================PROTOCOL======================================
# =============================================================================
    # Full 5mL tube
    current_height = start_height_1
    for i, well in enumerate(plate_96.wells()):
        if i == 0: 
            p300.pick_up_tip()
            ## Then, after every 8th well, drop tip and pick up a new one.   ##
        elif i % 8 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
    
        current_height, delta_height = volume_tracking(
                container, 100, current_height)
        ## then the specific variables are updated.                          ##
        pip_height = current_height - 2
          ## Make sure that the pipette tip is always submerged by setting   ##
          ## the current height 2 mm below its actual height                 ##
        if current_height - delta_height <= 1:
            protocol.pause("the tube is empty!")
        else:
            aspiration_location = tubes_5mL['C1'].bottom(pip_height)
          ## Set the location of where to aspirate from. Because we put this ##
          ## in the loop, the location will change to the newly calculated   ##
          ## height after each pipetting step.                               ##
          ## If the level of the liquid in the next run of the loop will be  ##
          ## smaller than 1 we have reached the bottom of the tube.          ##
        p300.aspirate(100, aspiration_location)
          ## Aspirate 200µL from the set aspiration location                 ##
        p300.dispense(100, well.top(z=-2))
          ## Dispense 200µL in the destination well                          ##
    p300.drop_tip()

    protocol.pause('change plate')


    # 2200µL in  5mL tube
    current_height = start_height_2
    for i, well in enumerate(plate_96.wells()):
        if i == 0: 
            p300.pick_up_tip()
            ## Then, after every 8th well, drop tip and pick up a new one.   ##
        elif i % 8 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
    
        current_height, delta_height = volume_tracking(
                container, 100, current_height)
        ## then the specific variables are updated.                          ##
        pip_height = current_height - 2
          ## Make sure that the pipette tip is always submerged by setting   ##
          ## the current height 2 mm below its actual height                 ##
        if current_height - delta_height <= 1:
            protocol.pause("the tube is empty!")
        else:
            aspiration_location = tubes_5mL['C2'].bottom(pip_height)
          ## Set the location of where to aspirate from. Because we put this ##
          ## in the loop, the location will change to the newly calculated   ##
          ## height after each pipetting step.                               ##
          ## If the level of the liquid in the next run of the loop will be  ##
          ## smaller than 1 we have reached the bottom of the tube.          ##
        p300.aspirate(100, aspiration_location)
          ## Aspirate 200µL from the set aspiration location                 ##
        p300.dispense(100, well.top(z=-2))
          ## Dispense 200µL in the destination wel                           ##
    p300.drop_tip()
    
    