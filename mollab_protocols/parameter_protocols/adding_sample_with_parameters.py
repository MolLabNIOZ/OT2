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
sys.path.append("C:/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'adding_sample_to_PCR_plate_V1.0',
            'description': 'adding sample to the PCR plate with barcoded primers'}
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Samples
    parameters.add_int(variable_name="number_of_samples",
                       display_name="number of unique samples",
                       description="Number of unique samples. Include samples & mock but EXCLUDE the NTC.",
                       default=95,
                       minimum=0,
                       maximum=95,
                       unit="samples")
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
    
    # Sets variables for the starting tips
    starting_tip_p20 = plankton.starting_tip_p20_row +  plankton.starting_tip_p20_column.strip("this_is_not_an_int")
    
    # Calculates the amount of tips needed
    p20_tips_needed, p300_tips_needed = LW.amount_of_tips(plankton.sample_volume,
                                                          plankton.number_of_samples,
                                                          1,
                                                          15)
    
    # Defines how much P20 and P300 tip racks you need and if the pipette is True/False
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               p20_tips_needed)
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    number_of_reactions = plankton.number_of_samples + plankton.number_of_NTCs
    
    if number_of_reactions > 96:
        raise Exception(f'You have {plankton.number_of_samples} reactions. ' +
                        'This is more than 96 reactions if you add the NTCs and is not possible.')
    else: 
        protocol.comment("You have {planktonnumber_of_reactions} samples and {plankton.number_of_NTCs}.")
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
    sample_tubes = LW.tube_locations(sample_racks,
                                     sample_loc,
                                     False,
                                     plankton.number_of_samples)
   
    ## ========================================================================
    #### PCR-plate
    # Loading PCR-plate
    PCR_plate = LW.loading_tube_racks(simulate, 
                                       'plate_96_NIOZholder', 
                                       'PCR_plate', 
                                       1, 
                                       [6], 
                                       protocol)
    # Sample destinations
    sample_destions = LW.tube_locations(PCR_plate,
                                        False,
                                        False,
                                        plankton.number_of_samples)
    ## ========================================================================
    ### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20, 
                                    tips_p20,
                                    starting_tip_p20,
                                    False, 
                                    [],
                                    'A1',
                                    protocol)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # transfering samples
    PM.transferring_reagents(sample_tubes,
                            sample_destions,
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