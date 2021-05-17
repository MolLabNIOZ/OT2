# =============================================================================
# Author(s): Maartje Brouwer & Sanne Vreugdenhil
# Creation date: 210517
# Description: Protocol for aliquoting 360 ul of T from a 50mL tube to 1.5mL
#              tubes.
# =============================================================================


# ===========================IMPORT STATEMENTS=================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
# =============================================================================


# =====================VOLUME TRACKING FUNCTIONS===============================
# =============================================================================
##### Import statements
import math
  ## Import math module to allow using π in calculations                    ##

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
    if container == 'tube_1.5mL':
        diameter = 8.7          #diameter of the top of the tube in mm
    elif container == 'tube_2mL':
        diameter = 9.85         #diameter of the top of the tube in mm
    elif container == 'tube_5mL':
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
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': 'Aliquot from 50mL tubes to 1.5 mL tubes',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('Protocol for aliquoting 360uL of Tris from a 50mL tube '
                    'to 1.5 mL tubes.' 
                    'One 50mL tube, 6x 24 1.5mL tubes.'),
    'apiLevel': '2.9'}
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):
    """
    Pick up 200µL filter tip.
    Aspirate 2x 180uL from 50mL tube and dispense in 1.5mL tube.
    Repeat for 24x 1.5mL tubes.
    Drop tip.
    Repeat untill 6 racks of 1.5mL tubes are filled.
    """      
# =============================================================================


# =====================LOADING LABWARE AND PIPETTES============================
# =============================================================================
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',                      #labware def
        10,                                                      #deck position
        '200tips')                                               #custom name
    stock_tubes = protocol.load_labware(
        'opentrons_6_tuberack_falcon_50ml_conical',              #labware def
        7,                                                       #deck position
        '50mL_tubes')                                            #custom name   
    aliquot_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        4,                                                       #deck position
        'aliquot_tubes_1')                                       #custom name
    aliquot_tubes_2 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        1,                                                       #deck position
        'aliquot_tubes_2')                                       #custom name
    aliquot_tubes_3 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        11,                                                       #deck position
        'aliquot_tubes_3')                                       #custom name
    aliquot_tubes_4 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        8,                                                      #deck position
        'aliquot_tubes_4')                                       #custom name
    aliquot_tubes_5 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        5,                                                       #deck position
        'aliquot_tubes_5')                                       #custom name
    aliquot_tubes_6 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        2,                                                       #deck position
        'aliquot_tubes_6')                                       #custom name

    
    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                              #instrument definition
        'right',                                         #mount position
        tip_racks=[tips_200])                            #assigned tiprack
# =============================================================================
    
    
# ===================================INITIALIZING==============================
# =============================================================================
    protocol.set_rail_lights(True)
    p300.starting_tip = tips_200.well('C1')#!!!
    p300.flow_rate.aspirate = 300
    p300.flow_rate.dispense = 300
# =============================================================================


# =============================VARIABLES TO SET#!!!============================
# =============================================================================
    start_vol = 51840 
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##
    source_well = stock_tubes['A1']
      ## Where do you place the 50mL tube
# =============================================================================

  
# ==========================PREDIFINED VARIABLES===============================
# =============================================================================
    container = 'tube_50mL'
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
    dest_racks = [aliquot_tubes_1, aliquot_tubes_2, aliquot_tubes_3,
                  aliquot_tubes_4, aliquot_tubes_5, aliquot_tubes_6]
# =============================================================================
    ##### Variables for volume tracking
    start_height = cal_start_height(container, start_vol)
      ## Call start height calculation function from volume tracking module.##
    current_height = start_height
      ## Set the current height to start height at the beginning of the     ##
      ## protocol.                                                          ##
# =============================================================================


# ===================================PROTOCOL==================================
# =============================================================================

    for rack in dest_racks:
        p300.pick_up_tip()
        for well in rack.wells():
            for i in range(2): 
              ## Pipette 5 x 200µL for 1mL aliquots
                current_height, delta_height = volume_tracking(
                    container, 180, current_height)
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
                    protocol.pause("the 50mL tube is empty!")
                else:
                    aspiration_location = source_well.bottom(pip_height)
              ## Set the location of where to aspirate from. Because we put this##
              ## in the loop, the location will change to the newly calculated  ##
              ## height after each pipetting step.                              ##
              ## If the level of the liquid in the next run of the loop will be ##
              ## smaller than 1 we have reached the bottom of the tube.         ##
                    p300.aspirate(180, aspiration_location)
              ## Aspirate 200µL from the set aspiration location                ##
                    p300.dispense(180, well.top(z=-2))
              ## Dispense 200µL in the destination well     
        p300.drop_tip()
           
        start_height = current_height

# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================