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

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Adding sample & mix to PCR-plate without barcodes V1.0',
            'description': 'Adding your samples and mix to the PCR plate with unlabeled primers.'
            }
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Mastermix
    parameters.add_int(variable_name="total_mastermix_volume",
                       display_name="total mastermix volume",
                       description="How much volume is in your mastermix tube?",
                       default=3000,
                       minimum=0,
                       maximum=50000,
                       unit="µL MM")
    parameters.add_int(variable_name="mastermix_volume",
                       display_name="mastermix volume per reaction",
                       description="How much mastermix should each reaction get?",
                       default=20,
                       minimum=0,
                       maximum=50,
                       unit="µL MM")
    
    #### Samples
    parameters.add_int(variable_name="number_of_samples",
                       display_name="number of unique samples",
                       description="Number of unique samples. Include samples but EXCLUDE the Mock & NTC.",
                       default=64,
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

## CONVERTING VARIABLES========================================================
## ============================================================================
    # Sets variables for the starting tips
    starting_tip_p20 = plankton.starting_tip_p20_row + plankton.starting_tip_p20_column.strip("this_is_not_an_int")
    starting_tip_p300 = plankton.starting_tip_p300_row + plankton.starting_tip_p300_column.strip("this_is_not_an_int")
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    #### Calculating samples per rack
    if plankton.sample_tube_type == "PCR_strips":
        sample_loc = ['2','7','11']
        samples_per_rack = (len(sample_loc)*8)
    
    if plankton.sample_tube_type == "1.5mL_tubes":
        sample_loc = False
        samples_per_rack = 24
    
    # Total amount of tubes and racks
    total_number_of_tubes = plankton.number_of_samples + plankton.number_of_Mocks
    total_reactions = plankton.number_of_samples + plankton.number_of_Mocks + plankton.number_of_NTCs
    number_of_sample_racks = math.ceil(total_number_of_tubes/samples_per_rack)
    
    #### Calculating tips and tip racks
    # Calculates amount of tips needed for the mastermix and sample
    tips_mastermix = LW.amount_of_tips(plankton.mastermix_volume,
                                        total_number_of_tubes,
                                        16,
                                        19)
    tips_sample = LW.amount_of_tips(plankton.sample_volume,
                                    total_number_of_tubes,
                                    1,
                                    15)
    
    # Calculates total amount of tips needed
    p20_tips_needed = tips_mastermix[0] + tips_sample[0]
    p300_tips_needed = tips_mastermix[1] + tips_sample[1]
    
    # Calculates how many tip racks you need and defines the pipette
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               p20_tips_needed)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip_p300,
                                                 p300_tips_needed)
    
    #### Mastermix tube type
    reagent_tube_type_mastermix, number_of_tubes_mastermix, max_volume_mastermix = LW.which_tube_type(total_volume = plankton.total_mastermix_volume,
                                                                                                      tube_type = False)
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    if total_reactions > 96:
        raise Exception(f'You have {total_reactions} reactions. ' +
                        'This is more than 96 reactions and is not possible, please check again or ask a technician for help!')
    else: 
        protocol.comment(f"You have {plankton.number_of_samples} samples, {plankton.number_of_Mocks} Mocks and {plankton.number_of_NTCs} NTCs.")
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(plankton.lights_on)
## ============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### PIPETTE TIPS
    tips_20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'opentrons_20uL',
                              amount = tip_racks_p20,
                              deck_positions = [1,4,7,10],
                              protocol = protocol)
    tips_300 = LW.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               amount = tip_racks_p300,
                               deck_positions = [10,7,4,1],
                               protocol = protocol)     
    
    #### PIPETTES       
    p20, p300 = LW.loading_pipettes(P20,
                                    tips_20,
                                    starting_tip_p20,
                                    P300, 
                                    tips_300,
                                    starting_tip_p300,
                                    protocol)
    
    #### MASTERMIX
    # Load mastermix rack
    mastermix_racks = LW.loading_tube_racks(simulate = simulate,
                                            tube_type = reagent_tube_type_mastermix,
                                            reagent_type = 'Mastermix',
                                            amount = number_of_tubes_mastermix,
                                            deck_positions = [9],
                                            protocol = protocol)
    # Specific location of mastermix
    mastermix_tube = LW.tube_locations(source_racks = mastermix_racks,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = number_of_tubes_mastermix,
                                       reagent_type = 'mastermix',
                                       volume = plankton.total_mastermix_volume,
                                       protocol = protocol)
    
    #### SAMPLES   
    # Loading sample plates
    sample_racks = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = plankton.sample_tube_type,
                                         reagent_type = 'sample_rack',
                                         amount = number_of_sample_racks,
                                         deck_positions = [2,5,8,11],
                                         protocol = protocol)
    
    # Specific location of samples
    sample_tubes_location, mock_tubes_location = LW.multiple_reagent_tube_locations (source_racks = sample_racks,
                                                                                    specific_columns = sample_loc,
                                                                                    skip_wells = False,
                                                                                    reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'Mock': plankton.number_of_Mocks},
                                                                                    volume = plankton.sample_volume,
                                                                                    protocol = protocol)
    
    #### QPCR-PLATE
    # Loading qPCR-plate
    qPCR_plate = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = 'plate_96_NIOZholder',
                                           reagent_type = 'qPCR-plate',
                                           amount = 1,
                                           deck_positions = [6],
                                           protocol = protocol)
    
    # Loading destination wells
    sample_destination, mock_destination, NTC_destination = LW.multiple_reagent_tube_locations (source_racks = qPCR_plate,
                                                                                                specific_columns = False,
                                                                                                skip_wells = False,
                                                                                                reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'Mock': plankton.number_of_Mocks, 'NTC': plankton.number_of_NTCs},
                                                                                                volume = plankton.sample_volume,
                                                                                                protocol = protocol)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Aliquoting mastermix
    PM.aliquoting_reagent(reagent_source = mastermix_tube,
                          reagent_tube_type = reagent_tube_type_mastermix,
                          reagent_startvolume = plankton.total_mastermix_volume,
                          aliquot_volume = plankton.mastermix_volume,
                          destination_wells = sample_destination + mock_destination + NTC_destination,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'next_tube',
                          pause = False,
                          protocol = protocol)
    
    # Transfering samples to plate
    PM.transferring_reagents(source_wells = sample_tubes_location + mock_tubes_location,
                              destination_wells = sample_destination + mock_destination,
                              transfer_volume = plankton.sample_volume,
                              airgap = True,
                              mix = True,
                              p20 = p20,
                              p300 = p300,
                              protocol = protocol)


## ============================================================================
 
## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================