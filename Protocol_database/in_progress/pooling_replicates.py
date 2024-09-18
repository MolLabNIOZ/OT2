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
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================
# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'pooling_replicate_plates',
            'description': 'pooling replicate PCRs into one of the plates'}
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### PCR reactions
    parameters.add_str(variable_name="sample_tube_type",    
                       display_name="sample tube type",
                       choices=[
                               {"display_name": "skirted plate", "value": "skirted_plate_96"},
                               {"display_name": "nonskirted plate", "value": "non_skirted_plate_96"},
                               {"display_name": "PCR strips", "value": "PCR_strips"}
                               ],
                       default="skirted_plate_96")
    parameters.add_int(variable_name="number_of_samples",
                       display_name="How many samples do you have?",
                       description="Number of samples including all controls.",
                       default=96,
                       minimum=0,
                       maximum=96,
                       unit="samples")
    parameters.add_int(variable_name="PCR_volume",
                       display_name="PCR volume",
                       description="How much volume is there in each well?",
                       default=50,
                       minimum=0,
                       maximum=200,
                       unit="µL")
    parameters.add_int(variable_name="replicates",
                       display_name="replicates",
                       description="How many replicates do you have?",
                       default=3,
                       minimum=2,
                       maximum=3,
                       unit="replicates")
    
    #### Starting tips
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
                       default="A")
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
                       default=1)
    
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

def run(protocol: protocol_api.ProtocolContext):
    plankton = protocol.params
# =============================================================================

## CONVERTING VARIABLES========================================================
## ============================================================================
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
    if plankton.sample_tube_type == 'PCR_strips':
        possible_strip_locations = {
            1:['6'],
            2:['3','9'],
            3:['2','7','11'],
            4:['2','5','8','11'],
            }
        strip_loc = possible_strip_locations[math.ceil(plankton.number_of_samples/8/2)]
        samples_per_rack = 8 * len(strip_loc)
        number_of_racks = math.ceil(plankton.number_of_samples / samples_per_rack)
        
        protocol.comment("Put your sample strips in the following columns"
                         f"{strip_loc}")
    else:
        number_of_racks = 1
        strip_loc = False
    
    # What volume needs to be aspirated (all replicates combined + airgaps of 5µL)
    transfer_volume = (plankton.PCR_volume * (plankton.replicates -1)) + ((plankton.replicates -1) * 5)
        
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### PIPETTE TIPS
    # Calculates how many tip racks per size are needed and set pipettes to true or false    
    tip_racks_p20, tip_racks_p300, P20, P300 = LW.number_of_tip_racks_2_0(volumes_aliquoting = False,
                                                                          number_of_aliquotes = False,
                                                                          volumes_transfering = transfer_volume,
                                                                          number_of_transfers = plankton.number_of_samples,
                                                                          starting_tip_p20 = starting_tip_p20,
                                                                          starting_tip_p300 = starting_tip_p300)
    # Loading tip racks
    tips_20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'tipone_20uL',
                              amount = tip_racks_p20,
                              deck_positions = [11,10],
                              protocol = protocol)
    tips_300 = LW.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               amount = tip_racks_p300,
                               deck_positions = [11,10],
                               protocol = protocol)
    
    #### PIPETTES       
    p20, p300 = LW.loading_pipettes(P20,
                                    tips_20,
                                    starting_tip_p20,
                                    P300, 
                                    tips_300,
                                    starting_tip_p300,
                                    protocol)
    
    #### LABWARE
    
    pool_rack = LW.loading_tube_racks(simulate = simulate, 
                                      tube_type = plankton.sample_tube_type,  
                                      reagent_type = 'pool', 
                                      amount = number_of_racks, 
                                      deck_positions = [6,3], 
                                      protocol = protocol)
    pool_wells = LW.tube_locations(source_racks = pool_rack,
                                   specific_columns = strip_loc,
                                   skip_wells = False,
                                   number_of_tubes = plankton.number_of_samples,
                                   reagent_type = 'destination',
                                   volume = plankton.PCR_volume / plankton.number_of_samples * plankton.replicates,
                                   protocol = protocol)
    
    source_rack_1 = LW.loading_tube_racks(simulate = simulate, 
                                      tube_type = plankton.sample_tube_type,  
                                      reagent_type = 'replicate_2', 
                                      amount = number_of_racks, 
                                      deck_positions = [5,2], 
                                      protocol = protocol)
    rep2_wells = LW.tube_locations(source_racks = source_rack_1,
                                   specific_columns = strip_loc,
                                   skip_wells = False,
                                   number_of_tubes = plankton.number_of_samples,
                                   reagent_type = 'samples',
                                   volume = plankton.PCR_volume / plankton.number_of_samples,
                                   protocol = protocol)
    
    if plankton.replicates > 2:
        source_rack_2 = LW.loading_tube_racks(simulate = simulate, 
                                          tube_type = plankton.sample_tube_type,  
                                          reagent_type = 'replicate_3', 
                                          amount = number_of_racks, 
                                          deck_positions = [4,1], 
                                          protocol = protocol)
        rep3_wells = LW.tube_locations(source_racks = source_rack_2,
                                       specific_columns = strip_loc,
                                       skip_wells = False,
                                       number_of_tubes = plankton.number_of_samples,
                                       reagent_type = 'samples',
                                       volume = plankton.PCR_volume / plankton.number_of_samples,
                                       protocol = protocol)
# =============================================================================

# LIGHTS ON====================================================================
# =============================================================================
    protocol.set_rail_lights(True)
# =============================================================================

# PIPETTING====================================================================
# =============================================================================
    if p20:
        pipette = p20
        push_out_volume = 2
    else:
        pipette = p300
        push_out_volume = 5
    
    #### Pooling duplos
    if plankton.replicates == 2:
        for rep2_well, pool_well in zip(rep2_wells, pool_wells):
            pipette.pick_up_tip()
            
            pipette.aspirate(plankton.PCR_volume, rep2_well)
            # To get everything out of the well
            protocol.delay(seconds=2)
            pipette.aspirate(5, rep2_well)
            
            pipette.dispense(transfer_volume, pool_well, push_out=push_out_volume)
            
            pipette.drop_tip()

    #### Pooling triplos
    if plankton.replicates == 3:
        for rep3_well, rep2_well, pool_well in zip(rep3_wells, rep2_wells, pool_wells):
            pipette.pick_up_tip()
            
            ## Rep3
            pipette.aspirate(plankton.PCR_volume, rep3_well)
            # To get everything out of the well
            protocol.delay(seconds=1)
            pipette.aspirate(5, rep3_well)
            
            ## Rep2
            pipette.aspirate(plankton.PCR_volume, rep2_well)
            # To get everything out of the well
            protocol.delay(seconds=1)
            pipette.aspirate(5, rep2_well)
            
            ## Pool
            pipette.dispense(transfer_volume, pool_well, push_out=push_out_volume)
            
            pipette.drop_tip()
# =============================================================================

# TURN RAIL LIGHT OFF==========================================================
# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================