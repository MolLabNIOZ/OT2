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
# from data.user_storage.mollab_modules import volume_tracking as vt #!!!
  ## Import volume tracking module for robot.                               ##
from mollab_modules import volume_tracking as vt #!!!
  ## Import volume tracking module for simulator.                           ##
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
    start_height = vt.cal_start_height(container, start_vol)
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
              ## Pipette 2 x 180µL for 360µL aliquots
                current_height, delta_height = vt.volume_tracking(
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
                    p300.blow_out(well.top(z=-2))
              ## Dispense 200µL in the destination well     
        p300.drop_tip()
           
        start_height = current_height

# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================