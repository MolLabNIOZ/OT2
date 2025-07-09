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
            'protocolName': 'Qubit V1.0',
            'description': 'aliquoting of Qubit mix to a plate, standards are '
            'added from 1.5mL tubes to the first row of the plate, then samples'
            ' are added from either strips, a plate or 1.5mL tubes.'
            }
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Standards
    parameters.add_int(variable_name="number_of_standard_dilutions",
                       display_name="number of standard dilutions?",
                       description="How many standards do you have?",
                       default=4,
                       minimum=2,
                       maximum=8,
                       unit="standards")
    
    #### Samples
    parameters.add_int(variable_name="number_of_samples",
                       display_name="number of saqmples",
                       description="How many samples do you have?",
                       default=88,
                       minimum=0,
                       maximum=88,
                       unit="samples")
    parameters.add_int(variable_name="sample_volume",
                       display_name="Sample Volume",
                       description="How much of your sample do you want to use?",
                       default=1,
                       minimum=1,
                       maximum=10,
                       unit="samples")

    parameters.add_str(variable_name="sample_tube_type",    
                       display_name="Sample tube type",
                       choices=[
                           {"display_name": "PCR-strips", "value": "PCR_strips"},
                           {"display_name": "PCR-plate", "value": "skirted_plate_96"},
                           {"display_name": "1.5mL tubes", "value": "1.5mL_tubes"},
                           ],
                       default="PCR_strips")
    
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

# CALCULATED AND SET VARIABLES=================================================
# This region contains settings and calculations that are later used
# =============================================================================
    #### Volumes to pipette
    # Volume of the standard to add
    std_vol = 2
    # Volume of the sample to add
    sample_vol = plankton.sample_volume    
    # How much mix to dispense for standards
    Qmix_vol_standards = 50 - std_vol
    # How much mix to dispense for samples
    Qmix_vol_sample = 50 - sample_vol
    
    #### Qmix 
    # How much Qmix do you need and what tube should be used?
    Qmix_start_volume = 5000
    Qmix_tube_type, number_of_Qmix_tubes, max_volume = LW.which_tube_type(
        total_volume = Qmix_start_volume,
        tube_type = False)
    
    #### Sample racks
    # Possible locations of strips in racks
    possible_strip_locations = {
        1:['6'],
        2:['3','9'],
        3:['2','7','11'],
        4:['2','5','8','11'],
        }     
    # Possible combinations for the different tube types
    tube_type_dict = {
        "PCR_strips" : (possible_strip_locations[math.ceil(plankton.number_of_samples/8/3)], len(possible_strip_locations[math.ceil(plankton.number_of_samples/8/3)])*8),
        "skirted_plate_96" : (False, 96),
        "1.5mL_tubes" : (False, 24),
        }
    # Number of sample racks
    stock_strip_columns = tube_type_dict[plankton.sample_tube_type][0]
    samples_per_rack = tube_type_dict[plankton.sample_tube_type][1]
    number_of_sample_racks = int(math.ceil((plankton.number_of_samples / samples_per_rack)))
    
    #### Calculates the amount of tip racks needed and set pipette True or False
    tip_racks_p20, tip_racks_p300, P20, P300 = LW.number_of_tip_racks_2_0(volumes_aliquoting = Qmix_vol_sample,
                                                                          number_of_aliquotes = plankton.number_of_samples + 8,
                                                                          volumes_transfering = sample_vol,
                                                                          number_of_transfers = plankton.number_of_samples + 8,
                                                                          starting_tip_p20 = starting_tip_p20,
                                                                          starting_tip_p300 = starting_tip_p300)
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_p20 = LW.loading_tips(simulate,
                               'tipone_20uL',
                               tip_racks_p20,
                               [7,10,11,8],
                               protocol)
    tips_p300 = LW.loading_tips(simulate,
                               'opentrons_200uL',
                               tip_racks_p300,
                               [8,11,10,7],
                               protocol)
    ## ========================================================================
    #### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20 = P20, 
                                    tips_20 = tips_p20,
                                    starting_tip_p20 = starting_tip_p20,
                                    P300 = P300, 
                                    tips_300 = tips_p300,
                                    starting_tip_p300 = starting_tip_p300,
                                    protocol = protocol)
    ## ========================================================================
    #### Water rack
    # Loading Qmix rack
    Qmix_rack = LW.loading_tube_racks(simulate = simulate, 
                                      tube_type = Qmix_tube_type,  
                                      reagent_type = 'Qmix', 
                                      amount = 1, 
                                      deck_positions = [9], 
                                      protocol = protocol)
    # Loading Qmix tube
    Qmix_tube = LW.tube_locations(source_racks = Qmix_rack,
                                  specific_columns = False,
                                  skip_wells = False,
                                  number_of_tubes = number_of_Qmix_tubes,
                                  reagent_type = 'Qmix',
                                  volume = Qmix_start_volume,
                                  protocol = protocol)
    ## ========================================================================
    #### Sample racks
    sample_racks = LW.loading_tube_racks(simulate = simulate, 
                                         tube_type = plankton.sample_tube_type,  
                                         reagent_type = 'samples', 
                                         amount = number_of_sample_racks,
                                         deck_positions = [1,3,4,6], 
                                         protocol = protocol)
    sample_tubes = LW.tube_locations(source_racks = sample_racks,
                                     specific_columns = stock_strip_columns,
                                     skip_wells = False,
                                     number_of_tubes = plankton.number_of_samples,
                                     reagent_type = 'samples',
                                     volume = 50,
                                     protocol = protocol)   
    ## ========================================================================
    #### Standard racks
    standard_racks = LW.loading_tube_racks(simulate = simulate, 
                                           tube_type = "1.5mL_tubes",  
                                           reagent_type = 'standards', 
                                           amount = 1,
                                           deck_positions = [2], 
                                           protocol = protocol)
    #### Standard tubes
    standard_tubes  = []
    for i in range(plankton.number_of_standard_dilutions):
        skip = list(range(len(standard_tubes)))
        standard_tube = LW.tube_locations(source_racks = standard_racks,
                                          specific_columns = False,
                                          skip_wells = skip,
                                          number_of_tubes = 1,
                                          reagent_type = f'Qbitstd{i+1}',
                                          volume = 50,
                                          protocol = protocol)
        standard_tubes += standard_tube
    ## ========================================================================
    #### Qubit plate
    Qbit_plate = LW.loading_tube_racks(simulate = simulate, 
                                       tube_type = "skirted_plate_96",  
                                       reagent_type = 'Qbit', 
                                       amount = 1,
                                       deck_positions = [5], 
                                       protocol = protocol)
    # Standard destinations    
    standard_wells = []
    replica_standards = int(8 / plankton.number_of_standard_dilutions)
    for i in range(plankton.number_of_standard_dilutions):
        skip = list(range(len(standard_wells)))
        destination = LW.tube_locations(source_racks = Qbit_plate,
                                        specific_columns = False,
                                        skip_wells = skip,
                                        number_of_tubes = replica_standards,
                                        reagent_type = f'Qbitstd{i+1}',
                                        volume = 50,
                                        protocol = protocol)
        standard_wells += destination
    # Sample destinations    
    sample_wells = LW.tube_locations(source_racks = Qbit_plate,
                                     specific_columns = False,
                                     skip_wells = list(range(len(standard_wells))),
                                     number_of_tubes = plankton.number_of_samples,
                                     reagent_type = "samples",                                     
                                     volume = 50,
                                     protocol = protocol)

## ============================================================================        

## LIGHTS======================================================================
## ============================================================================
    # Always put the light off when starting the protocol.    
    protocol.set_rail_lights(False)
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    protocol.comment(f'Provide {number_of_Qmix_tubes} {Qmix_tube_type} containing ' +
                     f'{Qmix_start_volume} µL of Qubit mix in A1 on slot 9')
    
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    #### Aliquoting QubitMix standards
    PM.aliquoting_reagent(reagent_source = Qmix_tube,
                          reagent_tube_type = Qmix_tube_type,
                          reagent_startvolume = Qmix_start_volume,
                          aliquot_volume = Qmix_vol_standards,
                          destination_wells = standard_wells,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'raise_error',
                          pause = False,
                          protocol = protocol)
    #### Aliquoting QubitMix samples
    PM.aliquoting_reagent(reagent_source = Qmix_tube,
                          reagent_tube_type = Qmix_tube_type,
                          reagent_startvolume = Qmix_start_volume - (Qmix_vol_standards * 8),
                          aliquot_volume = Qmix_vol_sample,
                          destination_wells = sample_wells,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'raise_error',
                          pause = False,
                          protocol = protocol)
    
    #### Adding standards
    standard_sources = []
    for standard_tube in standard_tubes:
        for i in range(int(replica_standards)):
            standard_sources.append(standard_tube)
                    
    PM.transferring_reagents(source_wells = standard_sources,
                             destination_wells = standard_wells,
                             transfer_volume = std_vol,
                             airgap = True,
                             mix = True,
                             p20 = p20,
                             p300 = p300,
                             protocol = protocol)
    
    #### Adding samples
    PM.transferring_reagents(source_wells = sample_tubes,
                             destination_wells = sample_wells,
                             transfer_volume = sample_vol,
                             airgap = True,
                             mix = True,
                             p20 = p20,
                             p300 = p300,
                             protocol = protocol)
## ============================================================================
