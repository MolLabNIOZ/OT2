# =============================================================================
# Author(s): Maartje Brouwer & Sanne Vreugdenhil
# Creation date: 210512
# Description: Protocol to check if the volume tracking works for 15mL and 50mL 
#              tubes. Distributes water from those tubes to 1.5mL tubes
#              consists of 2 parts (15 and 50mL). Will empty the 15mL tube and
#              pauses. Then reload protocol, comment out the 15mL part and
#              change starting tip to continue with testing the 50mL tube. 
# =============================================================================


# ===========================IMPORT STATEMENTS=================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
from mollab_modules import volume_tracking as vt
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': 'volume tracking test',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('distribute water from a 15mL and 50mL tube'),
    'apiLevel': '2.9'}
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):
    """
    Pick up 200µL filter tip. Aspirate 200µL from 2mL tube, 15mL tube and
    50mL tube and transfer 5x to 1.5mL tube (1mL aliquots)
    """      
# =============================================================================
    

# =====================LOADING LABWARE AND PIPETTES============================
# =============================================================================
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',                      #labware def
        10,                                                      #deck position
        '200tips')                                               #custom name
    stock_tubes = protocol.load_labware(
        'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical',    #labware def
        1,                                                       #deck position
        '15mL_50mL_tubes')                                       #custom name   
    aliquot_tubes_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        2,                                                       #deck position
        'aliquot_tubes_1')                                       #custom name
    aliquot_tubes_2 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        5,                                                       #deck position
        'aliquot_tubes_2')                                       #custom name
    aliquot_tubes_3 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        8,                                                       #deck position
        'aliquot_tubes_3')                                       #custom name
    aliquot_tubes_4 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        11,                                                      #deck position
        'aliquot_tubes_4')                                       #custom name
    
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


# Check volume tracking in 15mL tube===========================================
# ==========================VARIABLES TO SET 15mL#!!!==========================
# =============================================================================
    start_vol = 14000 
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##
    source_well = stock_tubes['C1']
      ## Where do you place the 15mL tube
# =============================================================================

  
# ==========================PREDIFINED VARIABLES 15mL===========================
# =============================================================================
    container = 'tube_15mL'
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
# =============================================================================
    ##### Variables for volume tracking
    start_height = vt.cal_start_height(container, start_vol)
      ## Call start height calculation function from volume tracking module.##
    current_height = start_height
      ## Set the current height to start height at the beginning of the     ##
      ## protocol.                                                          ##
# =============================================================================


# ===============================PROTOCOL 15mL=================================
# =============================================================================
    p300.pick_up_tip()
    
    for well in aliquot_tubes_1.wells():
        for i in range(5): # pipette 5 x 200µL for 1mL aliquots
            current_height, delta_height = vt.volume_tracking(
                container, 200, current_height)
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
                protocol.pause("the 15mL tube is empty!")
            else:
                aspiration_location = source_well.bottom(pip_height)
          ## Set the location of where to aspirate from. Because we put this##
          ## in the loop, the location will change to the newly calculated  ##
          ## height after each pipetting step.                              ##
          ## If the level of the liquid in the next run of the loop will be ##
          ## smaller than 1 we have reached the bottom of the tube.         ##
                p300.aspirate(200, aspiration_location)
          ## Aspirate 200µL from the set aspiration location                ##
                p300.dispense(200, well.top(z=-2))
          ## Dispense 200µL in the destination well
    p300.drop_tip()
# =============================================================================


# Check volume tracking in 50mL tube===========================================
# ==========================VARIABLES TO SET 50mL#!!!==========================
# =============================================================================
    start_vol = 50000 
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##
    source_well = stock_tubes['B3']
      ## Where do you place the 50mL tube
# =============================================================================

  
# ==========================PREDIFINED VARIABLES 50mL==========================
# =============================================================================
    container = 'tube_50mL'
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
# =============================================================================
    ##### Variables for volume tracking
    start_height = vt.cal_start_height(container, start_vol)
      ## Call start height calculation function from volume tracking module.##
    current_height = start_height
      ## Set the current height to start height at the beginning of the     ##
      ## protocol.                                                          ##
# =============================================================================


# ===============================PROTOCOL 50mL=================================
# =============================================================================
    p300.pick_up_tip()
    for well in aliquot_tubes_2.wells():
        for i in range(5): 
          ## Pipette 5 x 200µL for 1mL aliquots
            current_height, delta_height = vt.volume_tracking(
                container, 200, current_height)
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
                p300.aspirate(200, aspiration_location)
          ## Aspirate 200µL from the set aspiration location                ##
                p300.dispense(200, well.top(z=-2))
          ## Dispense 200µL in the destination well     
    p300.drop_tip()
   
    start_height = current_height
   
    p300.pick_up_tip()
    for well in aliquot_tubes_3.wells():
        for i in range(5): 
          ## Pipette 5 x 200µL for 1mL aliquots
            current_height, delta_height = vt.volume_tracking(
                container, 200, current_height)
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
                p300.aspirate(200, aspiration_location)
          ## Aspirate 200µL from the set aspiration location                ##
                p300.dispense(200, well.top(z=-2))
          ## Dispense 200µL in the destination well         
    p300.drop_tip()
   
    start_height = current_height
   
    p300.pick_up_tip()
    for well in aliquot_tubes_4.wells():
        for i in range(5): 
          ## Pipette 5 x 200µL for 1mL aliquots
            current_height, delta_height = vt.volume_tracking(
                container, 200, current_height)
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
                p300.aspirate(200, aspiration_location)
          ## Aspirate 200µL from the set aspiration location                ##
                p300.dispense(200, well.top(z=-2))
          ## Dispense 200µL in the destination well         
    p300.drop_tip()
    
    protocol.set_rail_lights(False)   
# =============================================================================