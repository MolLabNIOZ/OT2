def cal_start_height(tube_type, start_volume):
    """
    """
    #### Import math module to allow using π in calculations
    import math 
    
    #### Defining tube_type dimensions, based on labware blueprints
    tube_dimensions = {
    '1.5mL_tubes': {
        'diameter_top': 8.7,
        'diameter_tip': 3.6,
        'height_conical_tip': 17.8},
    '5mL_screwcap_tubes': {
        'diameter_top': 13,
        'diameter_tip': 3.3,
        'height_conical_tip': 66.1 - 43.6 - 1.3},
    '5mL_snapcap_tubes': {
        'diameter_top': 13.3,
        'diameter_tip': 3.3,
        'height_conical_tip': 55.4 - 2.2 - 34.12},
    '15mL_tubes': {
        'diameter_top': 15.16,
        'diameter_tip': 2.16,
        'height_conical_tip': 22.1},
    '50mL_tubes': {
        'diameter_top': 27.48,
        'diameter_tip': 4.7,
        'height_conical_tip': 15.3}} 
    
    #### Calculate radiuses (diameter / 2)
    radius_top = tube_dimensions[tube_type]['diameter_top']/ 2
    radius_tip = tube_dimensions[tube_type]['diameter_tip']/ 2
    
    #### Calculate the volume of the conical tip v = (1/3)*π*h*(r²+r*R+R²)
    vol_conical_tip = ((1/3)*math.pi*tube_dimensions[tube_type]['diameter_tip']*
                       ((radius_tip**2) + (radius_tip*radius_top) +
                        (radius_top**2)))

    #### Calculating start height
    cylinder_vol = start_volume - vol_conical_tip
    start_height = (tube_dimensions[tube_type]['diameter_tip'] +
                    (cylinder_vol / (math.pi*((radius_top)**2))))
        # start_height = height_conical_tip + height_cylindrical_part
    
    #### Some tweaks
    if tube_type == '50mL_tubes':
        start_height = start_height + 1.7
    elif tube_type == '15mL_tubes':
        start_height = start_height + 12.5
    elif tube_type == '5mL_screwcap_tubes':
        start_height = start_height + 4
    elif tube_type == '5mL_snapcap_tubes':
        start_height = start_height + 4    
    elif tube_type == '1.5mL_tubes':
        start_height = start_height + 7  
    
    return start_height  

def volume_tracking(tube_type, dispension_vol, current_height, direction):  
    """
    """
    #### Import math module to allow using π in calculations
    import math
    #### Defining tube_type dimensions, based on labware blueprints
    tube_dimensions = {
    '1.5mL_tubes': {
        'diameter_top': 8.7,
        'height': 37.8,
        'max_fill_height': 35},
    '5mL_screwcap_tubes': {
        'diameter_top': 13,
        'height': 64.8,
        'max_fill_height': 60},
    '5mL_snapcap_tubes': {
        'diameter_top': 13.3,
        'height': 55.4,
        'max_fill_height': 50},
    '15mL_tubes': {
        'diameter_top': 15.16,
        'height': 118.1,
        'max_fill_height': 100},
    '50mL_tubes': {
        'diameter_top': 27.48,
        'height': 113.3,
        'max_fill_height': 100}} 

 
    #### Calculate delta_height of the specified volume      
    radius = tube_dimensions[tube_type]['diameter_top'] / 2
    delta_height =  (dispension_vol/(math.pi*((radius)**2))) #h = v/(π*r²)
    
    #### Update current_height 
    if direction == 'emptying': 
        current_height = current_height - delta_height
    elif direction == 'filling': 
        current_height = current_height + delta_height
        print("start")
        print(current_height)

        ## The current_height (after aspiration) must be updated before the
        ## actual aspiration, because during aspiration the liquid will reach 
        ## that level.

    #### Tweaks
    if tube_type == '15mL_tubes':
        height_conical_tip = 22.1   #tube - straight part
        offset_height = height_conical_tip + 18 
        ## offset_height = height from where to start using
        ## current_height - 1 so that the pipette tip stays submerged
        if current_height < offset_height:
            current_height = current_height - 1
    ## Volume tracking when assuming the entire tube is cylindrical doesn't
    ## work very well with a 15 mL tube. Therefore, we need to adjust some
    ## values so that we do the volume tracking as good as possible.       
    ## start_height is already adjusted so that we start a little heigher,
    ## however at the offset_height the pipette didn't reach the liquid     
    ## anymore. So we lower the current_height with 1 so that the pipette   
    ## tip is always submerged and the entire tube is emptied.              

    #### Determine the height at which to pipette
    pip_height = current_height - 5
    ## Make sure that the pipette tip is always submerged by       
    ## setting the current height 5 mm below the reagent surface   

    #### Determine whether the pipette is reaching the bottom of the tube
    if direction == 'emptying':
        bottom_reached = False
        if pip_height - delta_height <= 2:
            bottom_reached = True
        # not thoroughly tested yet for other tubes then tubes_5mL!!!
    elif direction == 'filling':
        bottom_reached = False
        if pip_height + delta_height > tube_dimensions[tube_type]['max_fill_height']:
            bottom_reached = True
    
        print("end")
        print(current_height)
    
    return current_height, pip_height, bottom_reached

def pooling_varying_volumes(source_wells,
                            pool_volumes,
                            pool_tube,
                            pool_tube_type,
                            start_volume,
                            pool_volume_per_tube,
                            airgap,
                            mix,
                            p20,
                            p300,
                            protocol):
    """
    Parameters
    ----------
    source_wells : list
        List of tube(s)/well(s) to get pool from
    pool_volumes : list
        volumes in µL that you want to pool
    pool_tube : list
        List of tube(s)/well(s) to pool in
    pool_tube_type : string
        'tube_1.5mL' / 'tube_5mL' / 'tube_15mL' / 'tube_50mL'
    start_volume : float
        exact volume in µL that is already present in the pool tube(s)
    pool_volume_per_tube, : float
        exact volume in µL that is max pooled in 1 tube
    airgap : Boolean True or False
        Do you want an airgap after aspiration and after dispensing
    mix : Boolean True or False
        Do you want to mix (pipette up and down) after dispensing
    p20 : labware definition
    p300 : labware definition
    protocol : def run(protocol: protocol_api.ProtocolContext)

    Returns
    -------
    None.

    """
    #### Import volume tracking module

    
    #### Determine start_height (at the start, current_height = start_height)
    current_height = cal_start_height(pool_tube_type, start_volume)
    
    #### Variables for volume tracking and aliquoting        
    pooled_volume = 0
    counter = 0
    pool = pool_tube[counter]
    
    #### If only 1 volume is provided, 
    if not isinstance(pool_volumes, list):
        raise Exception("This protocol only works with a list of volumes.")
             
    #### First small volumes, then large volumes
    for pipette in [p20,p300]:
        ### Set airgap size, depending on pipette size
        if pipette  == p20:
            min_volume = 0
            max_volume = 19
            gap = 1
            push_out_volume = 2
                
        elif pipette == p300:
            min_volume = 19
            max_volume = 190
            gap = 5
            push_out_volume = 5
                
        ### Loop through list of volumes and destinations
        for well, pool_volume in zip(source_wells, pool_volumes):
            ## Aspirate a little more for reverse pipetting
            
            ## Determine which wells to fill with which pipette
            if min_volume < pool_volume <= max_volume:

                #### Call volume_tracking function
                current_height, pip_height, bottom_reached = (
                    volume_tracking(pool_tube_type,
                                       pool_volume, 
                                       current_height,
                                       'filling'))
                pooled_volume += pool_volume
                
                # ### If necesarry, continue with next tube
                # if bottom_reached or pooled_volume > pool_volume_per_tube:
                #     # Continue with next tube, reset volume_tracking
                #     current_height = start_height
                #     current_height, pip_height, bottom_reached = (
                #         VT.volume_tracking(pool_tube_type,
                #                             pool_volume, 
                #                             current_height,
                #                             'filling'))
                #     pooled_volume = 0
                #     counter += 1
                #     pool = pool_tube[counter]

                #### The actual pipetting                
                # Pick up a tip
                pipette.pick_up_tip()
                
                # Take up the specified volume per sample       
                pipette.aspirate(pool_volume, well)
                # Take an air gap, to prevent cross_contamination
                if airgap:
                    pipette.air_gap(gap)
                    dispense_volume = pool_volume + gap
                else:
                    dispense_volume = pool_volume
                    
                # Dispense in the pool_tube
                pipette.dispense(dispense_volume, pool.bottom(pip_height), push_out=push_out_volume)
                # Mix by pipetting up and down 3x
                if pool_tube_type == 'tube_1.5mL':
                    mix_height = 1
                else:
                    mix_height = 5
                pipette.mix(3, pool_volume, pool.bottom(pip_height + mix_height))
                # Blow out
                pipette.blow_out()
                              
                # drop tip
                pipette.drop_tip()



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
sys.path.append("O:/")
sys.path.append("/mnt/c/Program files/Opentrons")
#### Import mollab protocol module
# from data.user_storage.mollab_modules import Pipetting_Modules_V1_2 as PM
from data.user_storage.mollab_modules import LabWare_v2 as LW2
# =============================================================================

# TEMPLATE DATA================================================================
# This region contains template data that will be replaced by the TapeStation 
# calculating protocol
# =============================================================================
DNA_µL_list = [65, 42.28, 10.0, 10.0, 10.0, 10.0, 10.0, 65, 65]
bead_ratio = 1
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {
            'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Equimolar pooling protocol for NIOZ427_16s V2.1',
            'description': 'Pools your sample equimolar after running the tapestation calculation protocol and sample diluting protocol.'
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
                           {"display_name": "F", "value": "this_is_not_false"},
                           {"display_name": "G", "value": "G"},
                           {"display_name": "H", "value": "H"}
                           ],
                       default="A")
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
                       default=1)
    
    #### Lights/Pause
    parameters.add_bool(variable_name="lights_on",
                        display_name="lights on",
                        description="Do you want the lights turned ON?",
                        default=True)

def run(protocol: protocol_api.ProtocolContext):
    # Sets p as variable for protocol.params, this will make it all shorter
    plankton = protocol.params 
# =============================================================================

# PARAMETER VARIABLES==========================================================
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
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
    #### Calculate the total pool volume
    total_pool_volume = sum(DNA_µL_list)
    
    #### calculate total_pool_volume + buffer to add for clean-up 
    bead_volume = total_pool_volume * float(bead_ratio)
    total_cleanup_volume = total_pool_volume + bead_volume
    
    # Determine what tube type you need to pool everything
    pool_tube_type, number_of_tubes, max_volume = LW2.which_tube_type(total_volume = total_cleanup_volume,
                                                                     tube_type = False)
    
    # For very large quantities, determine volume to pool per tube
    pool_volume_per_tube = total_cleanup_volume / number_of_tubes / 2
    
    #### Calculates how many tips are needed for pipetting all the DNA volumes
    p20_tips_needed, p300_tips_needed = LW2.amount_of_tips(volumes = DNA_µL_list,
                                                          number_of_transfers = False,
                                                          tip_change = 1,
                                                          max_p20_volume = 15)
    
    # Calculates how many pipette boxes you need by using the function 'number_of_tipracks'
    tip_racks_p20, P20 = LW2.number_of_tipracks(starting_tip = starting_tip_p20,
                                                tips_needed = p20_tips_needed)
    tip_racks_p300, P300 = LW2.number_of_tipracks(starting_tip = starting_tip_p300,
                                                 tips_needed = p300_tips_needed)
# =============================================================================
## LIGHTS & COMMENT------------------------------------------------------------
    protocol.set_rail_lights(plankton.lights_on)
    protocol.comment(f"You need {math.ceil(bead_volume/number_of_tubes)} μL of bead solution in {number_of_tubes} {pool_tube_type}")
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    # Loading p20 tips
    tips_20 = LW2.loading_tips(simulate = simulate, 
                              tip_type = 'tipone_20uL', 
                              amount = tip_racks_p20, 
                              deck_positions = [7,10,11,8], 
                              protocol = protocol)
    
    # Loading p300 tips
    tips_300 = LW2.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               amount = tip_racks_p300,
                               deck_positions = [8,11,10,7],
                               protocol = protocol)
    
    #### Loading pipettes
    p20, p300 = LW2.loading_pipettes(P20 = P20, 
                                    tips_20 = tips_20,
                                    starting_tip_p20 = starting_tip_p20,
                                    P300 = P300, 
                                    tips_300 = tips_300,
                                    starting_tip_p300 = starting_tip_p300,
                                    protocol = protocol)
    
    #### Loading labware
    # Loading source plate
    source_plate = LW2.loading_tube_racks(simulate = simulate,
                                         tube_type = 'plate_96_NIOZholder',
                                         reagent_type = 'source_plate',
                                         amount = 1,
                                         deck_positions = [1],
                                         protocol = protocol)
    
    # Spefifying location of the samples
    source_wells = LW2.tube_locations_varying_liquid(source_racks = source_plate,
                                                     specific_columns = False,
                                                     skip_wells = False,
                                                     number_of_tubes = len(DNA_µL_list),
                                                     reagent_type = 'samples',
                                                     volume_list = DNA_µL_list,
                                                     protocol = protocol)

    
    # Loading destination tube rack
    destination_rack = LW2.loading_tube_racks (simulate = simulate, 
                                              tube_type = pool_tube_type, 
                                              reagent_type = 'pool_tube', 
                                              amount = 1, 
                                              deck_positions = [2], 
                                              protocol = protocol)
    
    # Spefifying location of the destination tube
    destination_tube = LW2.tube_locations(source_racks = destination_rack,
                                         specific_columns = False,
                                         skip_wells = False,
                                         number_of_tubes = number_of_tubes,
                                         reagent_type = 'beads',
                                         volume = bead_volume/number_of_tubes/number_of_tubes,
                                         protocol = protocol)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Settings for transfering the sample volumes in the destination plate
    pooling_varying_volumes(source_wells = source_wells,
                               pool_volumes = DNA_µL_list,
                               pool_tube = destination_tube,
                               pool_tube_type = pool_tube_type,
                               start_volume = bead_volume,
                               pool_volume_per_tube = pool_volume_per_tube,
                               airgap = True,
                               mix = True,
                               p20 = p20,
                               p300 = p300,
                               protocol = protocol)
## ============================================================================    
    
# TURN RAIL LIGHT OFF==========================================================
# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================
                        