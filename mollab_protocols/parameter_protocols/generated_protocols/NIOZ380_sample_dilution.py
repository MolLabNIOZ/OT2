# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
simulate = True
#### Import opentrons protocol API v2
from opentrons import protocol_api
#### Import math 
import math ## To do some calculations
#### For simulating in the app, set pathway to modules
import sys
sys.path.append("C:/Program files/Opentrons")
sys.path.append("/mnt/c/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# TEMPLATE DATA================================================================
# This region contains template data that will be replaced by the TapeStation 
# calculating protocl
# =============================================================================
#How much sample volume (µL) do you want to use for the dilution?
sample_volume = [20, 10, 45, 45, 10, 10, 10, 20, 10, 10, 45, 45, 10, 10, 45, 10, 40, 45, 45, 10, 40, 10, 20, 45, 30, 20, 10, 45, 10, 20, 10, 10, 40, 10, 40, 45, 20, 10, 10, 10, 45, 20, 30, 45, 20, 10, 45, 45, 10, 45, 45, 45, 45, 20, 10, 10, 45, 45, 45, 45, 40, 10, 10, 10, 10, 30, 10, 20, 30, 10, 45, 45, 10, 10, 10, 45, 20, 10, 30, 45, 20, 45, 10, 45, 45, 10, 10, 30, 20, 45, 45, 20, 20, 45, 10, 45]
  ## Can be one volume or a list of volumes
  
water_volume = [41.85, 54.08, 0.0, 0.0, 43.64, 41.12, 61.64, 62.08, 55.16, 80.36, 0.0, 0.0, 62.72, 36.44, 0.0, 47.24, 2.34, 0.0, 0.0, 54.44, 9.68, 49.76, 25.14, 0.0, 22.27, 25.86, 63.44, 0.0, 45.44, 54.16, 62.0, 58.4, 7.95, 58.76, 9.97, 0.0, 67.84, 87.92, 65.24, 86.48, 0.0, 38.32, 17.74, 0.0, 27.88, 50.48, 0.0, 0.0, 58.04, 0.0, 0.0, 0.0, 0.0, 45.09, 92.96, 70.28, 0.0, 0.0, 0.0, 0.0, 7.95, 75.32, 110.6, 46.52, 52.64, 17.63, 88.28, 30.83, 16.22, 35.36, 0.0, 0.0, 54.44, 50.84, 88.64, 0.0, 39.98, 53.36, 18.49, 0.0, 42.42, 0.0, 41.12, 0.0, 0.0, 56.96, 42.2, 36.74, 39.54, 0.0, 0.0, 34.86, 61.36, 0.0, 103.76, 0.0]#,11,12,13,14,15,16,17,18,19,20]
#[41.85, 54.08, 0.0, 0.0, 43.64, 41.12, 61.64, 62.08, 55.16, 80.36, 0.0, 0.0, 62.72, 36.44, 0.0, 47.24, 2.34, 0.0, 0.0, 54.44, 9.68, 49.76, 25.14, 0.0, 22.27, 25.86, 63.44, 0.0, 45.44, 54.16, 62.0, 58.4, 7.95, 58.76, 9.97, 0.0, 67.84, 87.92, 65.24, 86.48, 0.0, 38.32, 17.74, 0.0, 27.88, 50.48, 0.0, 0.0, 58.04, 0.0, 0.0, 0.0, 0.0, 45.09, 92.96, 70.28, 0.0, 0.0, 0.0, 0.0, 7.95, 75.32, 110.6, 46.52, 52.64, 17.63, 88.28, 30.83, 16.22, 35.36, 0.0, 0.0, 54.44, 50.84, 88.64, 0.0, 39.98, 53.36, 18.49, 0.0, 42.42, 0.0, 41.12, 0.0, 0.0, 56.96, 42.2, 36.74, 39.54, 0.0, 0.0, 34.86, 61.36, 0.0, 103.76, 0.0]
  # Can be one volume or a list of volumes.
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {
            'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Sample dilution protocol V1.0',
            'description': 'Dilute your samples after running the TapeStation calculating protocol.'
            }
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    #### Starting tips
    # P20
    parameters.add_str(variable_name="starting_tip_p20_row",    
                       display_name="starting tip p20 row",
                       choices=[
                           {"display_name": "A", "value": "A"},
                           {"display_name": "B", "value": "B"},
                           {"display_name": "C", "value": "C"},
                           {"display_name": "D", "value": "D"},
                           {"display_name": "E", "value": "E"},
                           {"display_name": "F", "value": "F"},
                           {"display_name": "G", "value": "G"},
                           {"display_name": "H", "value": "H"}
                           ],
                       default="A")
    parameters.add_str(variable_name="starting_tip_p20_column",    
                       display_name="starting tip p20 column",
                       choices=[
                           {"display_name": "1", "value": "this_is_not_an_int1"},
                           {"display_name": "2", "value": "this_is_not_an_int2"},
                           {"display_name": "3", "value": "this_is_not_an_int3"},
                           {"display_name": "4", "value": "this_is_not_an_int4"},
                           {"display_name": "5", "value": "this_is_not_an_int5"},
                           {"display_name": "6", "value": "this_is_not_an_int6"},
                           {"display_name": "7", "value": "this_is_not_an_int7"},
                           {"display_name": "8", "value": "this_is_not_an_int8"},
                           {"display_name": "9", "value": "this_is_not_an_int9"},
                           {"display_name": "10", "value": "this_is_not_an_int10"},
                           {"display_name": "11", "value": "this_is_not_an_int11"},
                           {"display_name": "12", "value": "this_is_not_an_int12"}
                           ],
                       default="this_is_not_an_int1")
    
    #### Starting tips
    # P300
    parameters.add_str(variable_name="starting_tip_p300_row",    
                       display_name="starting tip p300 row",
                       choices=[
                           {"display_name": "A", "value": "A"},
                           {"display_name": "B", "value": "B"},
                           {"display_name": "C", "value": "C"},
                           {"display_name": "D", "value": "D"},
                           {"display_name": "E", "value": "E"},
                           {"display_name": "F", "value": "F"},
                           {"display_name": "G", "value": "G"},
                           {"display_name": "H", "value": "H"}
                           ],
                       default="A")
    parameters.add_str(variable_name="starting_tip_p300_column",    
                       display_name="starting tip p300 column",
                       choices=[
                           {"display_name": "1", "value": "this_is_not_an_int1"},
                           {"display_name": "2", "value": "this_is_not_an_int2"},
                           {"display_name": "3", "value": "this_is_not_an_int3"},
                           {"display_name": "4", "value": "this_is_not_an_int4"},
                           {"display_name": "5", "value": "this_is_not_an_int5"},
                           {"display_name": "6", "value": "this_is_not_an_int6"},
                           {"display_name": "7", "value": "this_is_not_an_int7"},
                           {"display_name": "8", "value": "this_is_not_an_int8"},
                           {"display_name": "9", "value": "this_is_not_an_int9"},
                           {"display_name": "10", "value": "this_is_not_an_int10"},
                           {"display_name": "11", "value": "this_is_not_an_int11"},
                           {"display_name": "12", "value": "this_is_not_an_int12"}
                           ],
                       default="this_is_not_an_int1")
    
    #### Lights/Pause
    parameters.add_bool(variable_name="lights_on",
                        display_name="lights on",
                        description="Do you want the lights turned ON?",
                        default=True)

def run(protocol: protocol_api.ProtocolContext):
    # Sets p as variable for protocol.params, this will make it all shorter
    plankton = protocol.params 
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
    # Sets variables for the starting tips
    starting_tip_p20 = plankton.starting_tip_p20_row + plankton.starting_tip_p20_column.strip("this_is_not_an_int")
    starting_tip_p300 = plankton.starting_tip_p300_row + plankton.starting_tip_p300_column.strip("this_is_not_an_int")
    
    #### What tube type should be used for the dilution water?
    total_water = sum(water_volume) * 1.2 # +20%
    reagent_tube_type, number_of_tubes, max_volume = LW.which_tube_type(total_volume = total_water,
                                                                        tube_type = False)
    
    total_water = total_water / number_of_tubes
    
    #### How many tip racks should be loaded?
    # Calculates how many tips you need for pipetting all the sample volumes
    p20_tips_sample, p300_tips_sample = LW.amount_of_tips(volumes = sample_volume,
                                                          number_of_transfers = False,
                                                          tip_change = 1,
                                                          max_p20_volume = 15)
    
    # Calculates how many tips you need for pipetting all the water volumes
    p20_tips_water, p300_tips_water = LW.amount_of_tips(volumes = water_volume,
                                                        number_of_transfers = False,
                                                        tip_change = 16,
                                                        max_p20_volume = 19)
    
    # Calculates how many tips you need by adding the sample tips with the water tips
    p20_tips_needed = p20_tips_sample + p20_tips_water
    p300_tips_needed = p300_tips_sample + p300_tips_water
    
    # Calculates how many pipette boxes you need by using the function 'number_of_tipracks'
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip = starting_tip_p20,
                                                tips_needed = p20_tips_needed)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip = starting_tip_p300,
                                                 tips_needed = p300_tips_needed)
# =============================================================================
## LIGHTS & COMMENT------------------------------------------------------------
    protocol.set_rail_lights(plankton.lights_on)
    protocol.comment(f"You need {number_of_tubes} {reagent_tube_type}(s) filled to {math.ceil(total_water)} μL with PCR grade water")
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================    
    #### Pipette tips
    # Loading p20 tips
    tips_20 = LW.loading_tips(simulate = simulate, 
                              tip_type = 'tipone_20uL', 
                              amount = tip_racks_p20, 
                              deck_positions = [7,10,11,8], 
                              protocol = protocol)
    
    # Loading p300 tips
    tips_300 = LW.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               amount = tip_racks_p300,
                               deck_positions = [8,11,10,7],
                               protocol = protocol)
                               
    ### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20 = P20, 
                                    tips_20 = tips_20,
                                    starting_tip_p20 = starting_tip_p20,
                                    P300 = P300, 
                                    tips_300 = tips_300,
                                    starting_tip_p300 = starting_tip_p300,
                                    protocol = protocol)
    
    #### Loading labware
    # Loading water tube rack
    water_rack = LW.loading_tube_racks(simulate = simulate, 
                                       tube_type = reagent_tube_type, 
                                       reagent_type = 'Water', 
                                       amount = 1, 
                                       deck_positions = [3], 
                                       protocol = protocol)
    
    # Spefifying location of the water tube
    water_tubes = LW.tube_locations(source_racks = water_rack,
                                    specific_columns = False,
                                    skip_wells = False,
                                    number_of_tubes = number_of_tubes,
                                    reagent_type = 'water',
                                    volume = total_water,
                                    protocol = protocol)

    # Loading source plate
    source_plate = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = 'plate_96_NIOZholder',
                                         reagent_type = 'source_plate',
                                         amount = 1,
                                         deck_positions = [1],
                                         protocol = protocol)

    # Loading destination plate
    destination_plate = LW.loading_tube_racks(simulate = simulate,
                                              tube_type = 'plate_96_NIOZholder',
                                              reagent_type = 'destination_plate',
                                              amount = 1,
                                              deck_positions = [2],
                                              protocol = protocol)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Settings for aliquoting of the water volumes in the destination plate
    PM.aliquoting_varying_volumes(reagent_source = water_tubes, 
                                  reagent_tube_type = reagent_tube_type, 
                                  reagent_startvolume = total_water,
                                  aliquot_volumes = water_volume,
                                  destination_wells = destination_plate[0].wells(),
                                  p20 = p20,
                                  p300 = p300,
                                  tip_change = 16,
                                  action_at_bottom = 'next_tube',
                                  pause = False,
                                  protocol = protocol)
    
    # Settings for transfering the sample volumes in the destination plate
    # PM.transferring_varying_volumes(source_wells = source_plate[0].wells(),
    #                                 destination_wells = destination_plate[0].wells(),
    #                                 transfer_volumes = sample_volume,
    #                                 airgap = True,
    #                                 mix = True,
    #                                 p20 = p20,
    #                                 p300 = p300,
    #                                 protocol = protocol)
## LIGHTS & COMMENT------------------------------------------------------------
    protocol.set_rail_lights(False)