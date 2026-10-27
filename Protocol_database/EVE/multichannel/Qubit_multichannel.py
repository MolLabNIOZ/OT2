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
from data.user_storage.mollab_modules import Pipetting_Modules_v5 as PM
from data.user_storage.mollab_modules import LabWare_v3 as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Qubit multichannel V1',
            'description': 'aliquoting of Qubit mix to a plate, standards are '
            'added from 1.5mL tubes to the first row of the plate, then samples'
            ' are added from either strips, a plate or 1.5mL tubes.'}
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}
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
                       default=60,
                       minimum=0,
                       maximum=88,
                       unit="samples")
    parameters.add_int(variable_name="sample_volume",
                       display_name="Sample Volume",
                       description="How much of your sample do you want to use?",
                       default=2,
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
    
    parameters.add_int(variable_name="standard_volume",
                       display_name="Standard Volume",
                       description="How much of your sample do you want to use?",
                       default=2,
                       minimum=1,
                       maximum=10,
                       unit="samples")
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
    # Combining the row-variable with the column-variable to create starting tip
    starting_tip_p20 = "A1"
    starting_tip_p300 = plankton.starting_tip_p300_row + str(plankton.starting_tip_p300_column)
# =============================================================================

# CALCULATED AND SET VARIABLES=================================================
# This region contains settings and calculations that are later used
# =============================================================================
    #### Volumes to pipette
    # Volume of the standard to add
    std_vol = plankton.standard_volume
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
                               [4],
                               protocol)
    tips_p300 = LW.loading_tips(simulate,
                               'opentrons_200uL',
                               tip_racks_p300,
                               [10],
                               protocol)
    ## ========================================================================
    #### PIPETTES
    left_pipette, right_pipette = LW.loading_pipettes('P20multi',
                                                      'P300',
                                                      tips_p20,
                                                      starting_tip_p20, 
                                                      tips_p300,
                                                      starting_tip_p300,
                                                      protocol)
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
                                         deck_positions = [2,5,8], 
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
                                           deck_positions = [1], 
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
                                       deck_positions = [3], 
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
    protocol.pause(f'Provide {number_of_Qmix_tubes} {Qmix_tube_type} containing ' +
                     f'{Qmix_start_volume} µL of Qubit mix in A1 on slot 9')   
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    #### Aliquoting QubitMix standards
    if number_of_Qmix_tubes > 1:
        action_at_bottom = 'next_tube'
    else:
        action_at_bottom = 'continue_at_bottom'
    PM.aliquoting_reagent(reagent_source = Qmix_tube,
                          reagent_tube_type = Qmix_tube_type,
                          reagent_startvolume = Qmix_start_volume,
                          aliquot_volume = Qmix_vol_standards,
                          destination_wells = standard_wells,
                          p20 = left_pipette,
                          p300 = right_pipette,
                          action_at_bottom = action_at_bottom,
                          pause = False,
                          protocol = protocol)
    #### Aliquoting QubitMix samples
    PM.aliquoting_reagent(reagent_source = Qmix_tube,
                          reagent_tube_type = Qmix_tube_type,
                          reagent_startvolume = Qmix_start_volume - (Qmix_vol_standards * 8),
                          aliquot_volume = Qmix_vol_sample,
                          destination_wells = sample_wells,
                          p20 = left_pipette,
                          p300 = right_pipette,
                          action_at_bottom = action_at_bottom,
                          pause = False,
                          protocol = protocol)

    #### Adding standards
    standard_sources = []
    for standard_tube in standard_tubes:
        for i in range(int(replica_standards)):
            standard_sources.append(standard_tube)
    left_pipette.reset_tipracks()
    left_pipette.configure_nozzle_layout(style=protocol_api.SINGLE, start='H1', tip_racks=tips_p20)
    PM.transferring_reagents(source_wells = standard_sources,
                             destination_wells = standard_wells,
                             transfer_volume = std_vol,
                             airgap = True,
                             mix = True,
                             p20 = left_pipette,
                             p300 = right_pipette,
                             protocol = protocol)
    
    #### Transferring samples
    PM.transferring_reagents_multichannel(source_wells = sample_tubes,
                                          destination_wells = sample_wells,
                                          transfer_volume = sample_vol,
                                          airgap = True,
                                          mix = True,
                                          p20 = left_pipette,
                                          tips_20 = tips_p20,
                                          p300 = False,
                                          tips_300 = False,
                                          protocol = protocol)