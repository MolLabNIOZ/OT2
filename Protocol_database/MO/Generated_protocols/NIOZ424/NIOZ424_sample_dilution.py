# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
simulate = False
#### Import opentrons protocol API v2
from opentrons import protocol_api
#### Import math 
import math ## To do some calculations
#### For simulating in the app, set pathway to modules
import sys
sys.path.append("O:/")
sys.path.append("/mnt/c/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules_V1_2 as PM
from data.user_storage.mollab_modules import LabWare as LW
from data.user_storage.mollab_modules import LabWare_v2 as LW2
# =============================================================================

# TEMPLATE DATA================================================================
# This region contains template data that will be replaced by the TapeStation 
# calculating protocl
# =============================================================================
#How much sample volume (µL) do you want to use for the dilution?
sample_volume = [5, 5, 5, 5, 5, 5, 42, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 42, 5, 5, 5, 5, 42, 5, 5, 5, 5, 5, 5, 5, 5, 5, 42, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 42, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 42, 5, 5, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 5, 10, 5, 5, 10, 5, 42, 42, 5, 42]
  ## Can be one volume or a list of volumes
  
water_volume = [10.07, 18.21, 16.89, 16.29, 13.54, 12.6, 0.0, 16.51, 15.24, 17.27, 17.11, 15.62, 14.86, 15.57, 14.64, 16.62, 19.37, 0.0, 18.27, 15.41, 18.1, 16.89, 0.0, 17.88, 17.27, 16.51, 14.2, 13.32, 15.19, 16.51, 15.24, 14.8, 0.0, 15.74, 15.19, 14.47, 11.94, 13.37, 13.98, 15.13, 13.7, 12.77, 13.54, 16.95, 14.64, 16.07, 14.69, 16.34, 0.0, 16.67, 16.45, 16.12, 13.43, 16.01, 14.75, 15.35, 13.98, 13.87, 13.64, 13.15, 13.43, 0.0, 14.86, 14.86, 18.05, 19.04, 16.67, 14.97, 14.14, 13.54, 14.86, 13.64, 12.16, 14.09, 13.87, 13.04, 12.93, 13.32, 13.32, 12.16, 14.53, 10.18, 11.34, 10.4, 19.81, 10.62, 11.28, 19.59, 10.9, 0.0, 0.0, 13.32, 0.0]
  # Can be one volume or a list of volumes.
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {
            'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Sample dilution protocol for NIOZ424 V2.0',
            'description': 'Dilute your samples after running the TapeStation calculating protocol.'
            }
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    #### Bullsh*t
    parameters.add_str(variable_name="Who_is_your_favourite_robot",    
                       display_name="Who is your favourite robot",
                       choices=[
                           {"display_name": "WALL-E", "value": "WALL-E"},
                           {"display_name": "EVE", "value": "EVE"},
                           {"display_name": "MO", "value": "MO"},
                           ],
                       default="MO")
    
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
                           {"display_name": "F", "value": "this_is_not_false"},
                           {"display_name": "G", "value": "G"},
                           {"display_name": "H", "value": "H"}
                           ],
                       default="H")
    parameters.add_int(variable_name="starting_tip_p20_column",    
                       display_name="starting tip p20 column",
                       choices=[
                           {"display_name": "1", "value": 1},
                           {"display_name": "2", "value": 2},
                           {"display_name": "3", "value": 3},
                           {"display_name": "4", "value": 4},
                           {"display_name": "5", "value": 5},
                           {"display_name": "6", "value": 6},
                           {"display_name": "7", "value": 7},
                           {"display_name": "8", "value": 8},
                           {"display_name": "9", "value": 9},
                           {"display_name": "10", "value": 10},
                           {"display_name": "11", "value": 11},
                           {"display_name": "12", "value": 12}
                           ],
                       default=12)
    
    parameters.add_str(variable_name="starting_tip_p300_row",    
                       display_name="starting tip p300 row",
                       choices=[
                           {"display_name": "A", "value": "A"},
                           {"display_name": "B", "value": "B"},
                           {"display_name": "C", "value": "C"},
                           {"display_name": "D", "value": "D"},
                           {"display_name": "E", "value": "E"},
                           {"display_name": "F", "value": "this_is_not_false"},
                           {"display_name": "G", "value": "G"},
                           {"display_name": "H", "value": "H"}
                           ],
                       default="H")
    parameters.add_int(variable_name="starting_tip_p300_column",    
                       display_name="starting tip p300 column",
                       choices=[
                           {"display_name": "1", "value": 1},
                           {"display_name": "2", "value": 2},
                           {"display_name": "3", "value": 3},
                           {"display_name": "4", "value": 4},
                           {"display_name": "5", "value": 5},
                           {"display_name": "6", "value": 6},
                           {"display_name": "7", "value": 7},
                           {"display_name": "8", "value": 8},
                           {"display_name": "9", "value": 9},
                           {"display_name": "10", "value": 10},
                           {"display_name": "11", "value": 11},
                           {"display_name": "12", "value": 12}
                           ],
                       default=12)
    
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
    #### Starting tips
    if plankton.starting_tip_p20_row == 'this_is_not_false':
        starting_tip_p20_row = 'F'
    else:
        starting_tip_p20_row = plankton.starting_tip_p20_row
    if plankton.starting_tip_p300_row == 'this_is_not_false':
        starting_tip_p300_row = 'F'
    else:
        starting_tip_p300_row = plankton.starting_tip_p300_row
    
    # Combining the row-variable with the column-variable to create starting tip
    starting_tip_p20 = starting_tip_p20_row + str(plankton.starting_tip_p20_column)
    starting_tip_p300 = starting_tip_p300_row + str(plankton.starting_tip_p300_column)
    
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
    
    source_wells = LW2.tube_locations_varying_liquid(source_racks = source_plate,
                                                     specific_columns= False,
                                                     skip_wells = False,
                                                     number_of_tubes= len(sample_volume),
                                                     reagent_type = "samples",
                                                     volume_list = sample_volume,
                                                     protocol = protocol)

    # Loading destination plate
    destination_plate = LW.loading_tube_racks(simulate = simulate,
                                              tube_type = 'plate_96_NIOZholder',
                                              reagent_type = 'destination_plate',
                                              amount = 1,
                                              deck_positions = [2],
                                              protocol = protocol)
    
    destination_wells = LW2.tube_locations_varying_liquid(source_racks = destination_plate,
                                                          specific_columns= False,
                                                          skip_wells = False,
                                                          number_of_tubes= len(sample_volume),
                                                          reagent_type = "samples",
                                                          volume_list = sample_volume,
                                                          protocol = protocol)
    
    # Give the destination wells also the color for the water
    water_color = protocol.define_liquid(
        name= "Water",
        description = "Wells containing water",
        display_color = "#0000FF")
    
    for well,volume in zip(destination_wells,water_volume):
        well.load_liquid(liquid=water_color, volume = volume)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Settings for aliquoting of the water volumes in the destination plate
    PM.aliquoting_varying_volumes(reagent_source = water_tubes, 
                                  reagent_tube_type = reagent_tube_type, 
                                  reagent_startvolume = total_water,
                                  aliquot_volumes = water_volume,
                                  destination_wells = destination_wells,
                                  p20 = p20,
                                  p300 = p300,
                                  tip_change = 16,
                                  action_at_bottom = 'next_tube',
                                  pause = False,
                                  protocol = protocol)
    
    # Settings for transfering the sample volumes in the destination plate
    PM.transferring_varying_volumes(source_wells = source_wells,
                                    destination_wells = destination_wells,
                                    transfer_volumes = sample_volume,
                                    airgap = True,
                                    mix = True,
                                    p20 = p20,
                                    p300 = p300,
                                    protocol = protocol)
## LIGHTS & COMMENT------------------------------------------------------------
    protocol.set_rail_lights(False)