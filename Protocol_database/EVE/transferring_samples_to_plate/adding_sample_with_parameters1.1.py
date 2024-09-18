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
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Adding sample to PCR-plate V1.1',
            'description': 'Adding your samples to the PCR plate with (barcoded) primers.'
            ' The parameters you are able to change are: number of samples and NTCs, the labware your sample is in, what volume of template you want to add, the starting tip and whether the lights are on or off.'}
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Samples
    parameters.add_int(variable_name="number_of_samples",
                       display_name="number of unique samples",
                       description="Number of unique samples. Include samples but EXCLUDE the Mock & NTC.",
                       default=94,
                       minimum=0,
                       maximum=94,
                       unit="samples")
    parameters.add_int(variable_name="number_of_Mocks",
                       display_name="number of unique Mocks",
                       description="Number of unique Mocks. Could be 0 or 1",
                       default=1,
                       minimum=0,
                       maximum=1,
                       unit="Mocks")
    parameters.add_int(variable_name="number_of_NTCs",
                       display_name="number of NTCs",
                       description="Number of NTCs. A NTC is a reaction without any template volume added.",
                       default=1,
                       minimum=1,
                       maximum=5,
                       unit="reactions")
    parameters.add_str(variable_name="sample_tube_type",    
                       display_name="sample tube type",
                       choices=[
                               {"display_name": "PCR-strips", "value": "PCR_strips"},
                               {"display_name": "1.5mL_tubes", "value": "1.5mL_tubes"},
                               ],
                       default="PCR_strips")
    parameters.add_float(variable_name="sample_volume",
                       display_name="sample volume per reaction",
                       description="How much sample should each reaction get?",
                       default=1.0,
                       minimum=1.0,
                       maximum=15.0,
                       unit="µL sample")
    
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
    
    #### Lights/Pause  
    parameters.add_bool(variable_name="lights_on",
                        display_name="lights on",
                        description="Do you want the lights turned ON?",
                        default=True)
  
def run(protocol: protocol_api.ProtocolContext):
    # Sets p as variable for protocol.params, this will make it all shorter
    plankton = protocol.params
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    if plankton.sample_tube_type == 'PCR_strips':       
        # Calculates how many sample racks were needed
        sample_loc = ['2','7','11']
        sample_per_rack = 8 * len(sample_loc)
        number_of_sample_racks = math.ceil(plankton.number_of_samples/sample_per_rack)
    else:
        sample_loc = False
        number_of_sample_racks = math.ceil(plankton.number_of_samples/24)
    
    #### Starting tips
    if plankton.starting_tip_p20_row == 'this_is_not_false':
        starting_tip_p20_row = 'F'
    else:
        starting_tip_p20_row = plankton.starting_tip_p20_row   
    # Combining the row-variable with the column-variable to create starting tip
    starting_tip_p20 = starting_tip_p20_row + str(plankton.starting_tip_p20_column)
    starting_tip_p300 = 'A1'
    
    # Calculates the amount of tips needed
    p20_tips_needed, p300_tips_needed = LW.amount_of_tips(plankton.sample_volume,
                                                          plankton.number_of_samples,
                                                          1,
                                                          15)
    
    # Defines how much P20 and P300 tip racks you need and if the pipette is True/False
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               p20_tips_needed)
    P300 = False
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    number_of_reactions = plankton.number_of_samples + plankton.number_of_NTCs + plankton.number_of_Mocks
    
    if number_of_reactions > 96:
        raise Exception(f'You have {number_of_reactions} reactions. ' +
                        'This is more than 96 reactions if you add the NTCs and is not possible.')
    else: 
        protocol.comment(f"You have {plankton.number_of_samples} samples, {plankton.number_of_Mocks} Mocks and {plankton.number_of_NTCs} NTCs.")
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(plankton.lights_on)
## ============================================================================    

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_p20 = LW.loading_tips(simulate,
                               'tipone_20uL',
                               tip_racks_p20,
                               [1,4],
                               protocol)
    tips_p300 = []
    ## ========================================================================
    #### Sample racks
    # Loading sample plates
    sample_racks = LW.loading_tube_racks(simulate, 
                                         plankton.sample_tube_type, 
                                         'Sample_rack', 
                                         number_of_sample_racks, 
                                         [2,5,8,11], 
                                         protocol)
    
    # Specifying the tube wells locations within the sample racks
    sample_tubes, Mock_tubes =  LW.multiple_reagent_tube_locations(source_racks = sample_racks,
                                     specific_columns = sample_loc,
                                     skip_wells = False,
                                     reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'Mock': plankton.number_of_Mocks},
                                     volume = 10,
                                     protocol = protocol) 
    ## ========================================================================
    #### PCR-plate
    # Loading PCR-plate
    PCR_plate = LW.loading_tube_racks(simulate, 
                                       'plate_96_NIOZholder', 
                                       'PCR_plate', 
                                       1, 
                                       [6], 
                                       protocol)

    
    sample_destinations, Mock_destination, NTC_destinations = LW.multiple_reagent_tube_locations(source_racks = PCR_plate,
                                                                                                 specific_columns = False,
                                                                                                 skip_wells = False,
                                                                                                 reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'Mock': plankton.number_of_Mocks, 'NTC': plankton.number_of_NTCs},
                                                                                                 volume = 0,
                                                                                                 protocol = protocol)   
    ## ========================================================================
    ### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20, 
                                    tips_p20,
                                    starting_tip_p20,
                                    P300, 
                                    tips_p300,
                                    starting_tip_p300,
                                    protocol)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # transfering samples
    PM.transferring_reagents(sample_tubes + Mock_tubes,
                              sample_destinations + Mock_destination,
                              plankton.sample_volume,
                              True,
                              True,
                              p20,
                              p300,
                              protocol)

## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================   