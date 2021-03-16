# =============================================================================
# Author(s): Maartje Brouwer & Sanne Vreugdenhil
# Creation date: 210312
# Description: Script to test if we can implement volume tracking.
# =============================================================================

##### Import statements
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
from modules import disposal_volume as dv
  ## Import module that calculates 2% disposal on top of aspiration volume. ##
from modules import volume_tracking as vol_track
  ## Import module that calculates how much the pipette should decrease     ##
  ## it's height before each aspiration-dispension step.                    ##

##### Metadata
metadata = {
    'protocolName': 'test_volume_tracking.py',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('Testing the volume_tracking module by aliquoting liquid'
                    'from a 5mL tube to an entire 96-wells plate'),
    'apiLevel': '2.9'}

##### Define function
def run(protocol: protocol_api.ProtocolContext):
    """Aliquoting liquid from a 5 mL tube to an entire 96-wells plate; 
    using volume tracking so that the pipette starts aspirating at the
    starting height of the liquid and goes down as the volume decreases."""
    
    ##### !!! Loading labware
    ## For available labware see "labware/list_of_available_labware".       ##
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        1,                                  #deck position
        '200tips')                          #custom name
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        3,                                  #deck position
        '96well_plate')                     #custom name
    ## The 5mL tubes are custom labware, because the protocol simulator     ##
    ## handles the import of custom labware different than the robot does,  ##
    ## we have 2 options for handling this. Comment out the option that you ##
    ## are not using (in spyder: select + ctrl-1).                          ##
    #### !!! OPTION 1: ROBOT                                               ###
    # tubes_5mL = protocol.load_labware(
    #     'eppendorf_15_tuberack_5000ul',     #labware definition
    #     2,                                  #deck position
    #     '5mL_tubes')                        #custom name
    #### !!! OPTION 2: SIMULATOR
    with open("labware/eppendorf_15_tuberack_5000ul/"
          "eppendorf_15_tuberack_5000ul.json") as labware_file:
        labware_def_5mL = json.load(labware_file)
      ## Import the file that contains all the information about the custom ##
      ## labware. Load the file using json, store it in a variable.         ##
    tubes_5mL = protocol.load_labware_from_definition( 
        labware_def_5mL,                    #labware definition
        2,                                  #deck position
        '5mL_tubes')                        #custom name
      ## Load the labware using load_labware_from_definition() instead of   ##
      ## load_labware(). Then use the variable you just set with the opened ##
      ## json file to define which labware to use.                          ##
    
    ##### !!! Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack
    
    ##### !!! Variables to set 
    container = 'tube_5mL'
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
      ## There are several options to choose from:                          ##
      ## 'tube_1.5ml', 'tube_2mL', 'tube_5mL', 'tube_15mL', 'tube_50mL'   	##
    start_vol = 2600 
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##
    dispension_vol = 24 
      ## The dispension_vol is the volume (ul) that needs to be aliquoted   ##
      ## into the destination wells/tubes.                                  ##
    aspiration_vol = dv.disposal_volume_p300_200(dispension_vol) 
      ## The aspiration_vol is the volume (ul) that is aspirated from the   ##
      ## container. For aliquoting liquids it may be nice to aspirate a bit ##
      ## more volume than you want to dispense (mimicking reverse           ##
      ## pipetting). For this you can use the disposal_volume module,       ##
      ## containing functions (for both pipettes) that calculate a 2% extra ##
      ## aspiration volume. The functions for these are:                    ##
      ##   dv.disposal_volume_p300(dispension_vol)                          ##
      ##   dv.disposal_volume_p20(dispension_vol)                           ##
      ## NOTE: the aspiration volume can not be higher than the pipette or  ##
      ## pipette tip limit!!!                                               ##
      ## When NOT using a disposal volume:                                  ##
      ##   aspiration_vol = dispension_vol                                  ##
    p300_tip_loc = tips_200['A3'] 
      ## The p300_tip_loc is the location of first pipette tip in the box   ##
      ## at the start of the protocol. Check the pipette tip box where the  ##
      ## next available tip is. The robot takes tips column by column.      ##
   
    ##### Volume tracking
    current_vol = start_vol
      ## The current_vol is a variable that is used in the volume_tracking  ##
      ## module. At the start of the protocol, the current_vol is equal to  ## 
      ## the start_vol.                                                     ##
    
    ##### The actual protocol
    protocol.set_rail_lights(True)
      ## Start by turning the lights on                                     ##
    p300.pick_up_tip(p300_tip_loc)
      ## p300 picks up tip from location specified in variable p300_tip_loc ##
    for well in plate_96.wells():
      ## Name all the wells in the plate 'well', for all these do:          ##  
        tv = vol_track.volume_tracking(container, current_vol, aspiration_vol)  
        current_height, current_vol, delta_height = tv
          ## The volume_tracking function needs the arguments container,    ##
          ## current_vol and the aspiration_vol which we have set in this   ##
          ## protocol. With those variables, the function calculates the    ##
          ## current_height, current_vol and delta_height of the liquid     ##
          ## after the next aspiration step. The outcome is stored as tv and##
          ## then the specific variables are updated.                       ##
        current_height = current_height - 1
          ## Make sure that the pipette tip is always submerged by setting  ##
          ## the current height 1 mm below its actual height                ##
        aspiration_location = tubes_5mL['A1'].bottom(current_height) 
          ## Set the location of where to aspirate from. Because we put this##
          ## in the loop, the location will change to the newly calculated  ##
          ## height after each pipetting step.                              ##
        p300.aspirate(aspiration_vol, aspiration_location)
         ## Aspirate the amount specified in aspiration_vol from the        ##
         ## location specified in aspiration_location.                      ##
        p300.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the location##
          ## specified in well (so a new well every time the loop restarts) ##
        p300.blow_out(tubes_5mL['A1'])
          ## Blow out any remaining liquid (disposal volume) in the source  ##
          ## tube before we want to aspirate again.                         ##
        if current_height - delta_height <= 1: #make sure bottom is never reached
            protocol.home()
            protocol.pause('Your mix is finished.')
          ## If the level of the liquid in the next run of the loop will be ##
          ## smaller than 1 we have reached the bottom of the tube. To      ##
          ## prevent the pipette from crashing into the bottom, we tell it  ##
          ## to go home and pause the protocol so that this can never happen##
    p300.drop_tip()
      ## Drop the tip in the trash bin.                                     ##
    protocol.set_rail_lights(False)
      ## Finish by turning the lights off.                                  ##
    
##### We have now filled an entire plate, hopefully with volume tracking :D!
