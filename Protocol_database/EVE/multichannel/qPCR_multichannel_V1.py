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
            'protocolName': 'qPCR multichannel V1',
            'description': 'Adding MasterMix (optional), samples, standards to a qPCR plate.'
            }
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Mastermix
    parameters.add_bool(variable_name="mastermix_included",
                        display_name="Mastermix?",
                        description="Do you want to include mastermix?",
                        default=True)
    
    parameters.add_int(variable_name="total_mastermix_volume",
                       display_name="total mastermix volume",
                       description="How much volume is in your mastermix tube?",
                       default=2000,
                       minimum=0,
                       maximum=50000,
                       unit="µL MM")
    parameters.add_int(variable_name="mastermix_volume",
                       display_name="mastermix vol per reaction",
                       description="How much mastermix should each reaction get?",
                       default=22,
                       minimum=19,
                       maximum=50,
                       unit="µL MM")
    
    #### Samples
    parameters.add_int(variable_name="number_of_samples",
                       display_name="number of unique samples",
                       description="Number of unique samples",
                       default=10,
                       minimum=0,
                       maximum=94,
                       unit="samples")
    parameters.add_int(variable_name="number_of_replicates",
                       display_name="number of replicates",
                       description="1 means every sample once, 2 means duplicates, 3 means triplicates etc",
                       default=3,
                       minimum=1,
                       maximum=3,
                       unit="replicates")
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
                       display_name="sample vol per reaction",
                       description="How much sample should each reaction get?",
                       default=3.0,
                       minimum=1.0,
                       maximum=15.0,
                       unit="µL sample")
    
    #### Standard sample and dilution serie
    parameters.add_int(variable_name="number_of_std_series",
                       display_name="number of dilution series",
                       description="Number of replicates of the dilution serie used for quantification.",
                       default= 1,
                       minimum= 0,
                       maximum= 4,
                       unit="dil series")
    parameters.add_int(variable_name="lenght_of_std_serie",
                       display_name="length dilution series",
                       description="The length of a single standard dilution serie.",
                       default= 8,
                       minimum= 0,
                       maximum= 8,
                       unit="dilutions")
    parameters.add_int(variable_name="number_of_std_samples",
                       display_name="number of standard samples",
                       description="Number of replicates of the standard sample.",
                       default= 6,
                       minimum= 0,
                       maximum= 8,
                       unit="STD sample")
    parameters.add_str(variable_name="STD_tube_type",    
                       display_name="STD sample tube type",
                       choices=[
                               {"display_name": "PCR-strips", "value": "PCR_strips"},
                               {"display_name": "1.5mL_tubes", "value": "1.5mL_tubes"},
                               ],
                       default="1.5mL_tubes")
    
    #### Starting tips
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
    # Sets p as variable for protocol.params, this will make it all shorter
    plankton = protocol.params
# =============================================================================

## CONVERTING VARIABLES========================================================
## ============================================================================
    if plankton.starting_tip_p300_row == 'this_is_not_false':
        starting_tip_p300_row = 'F'
    else:
        starting_tip_p300_row = plankton.starting_tip_p300_row
    
    # Combining the row-variable with the column-variable to create starting tip
    starting_tip_p300 = starting_tip_p300_row + str(plankton.starting_tip_p300_column)
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    #### Calculating total amount of reactions
    
    number_of_standard_dilution_samples = plankton.number_of_std_series * plankton.lenght_of_std_serie
    total_reactions = (plankton.number_of_samples * plankton.number_of_replicates) + plankton.number_of_NTCs + number_of_standard_dilution_samples + plankton.number_of_std_samples
        
    if plankton.number_of_std_samples == 0:
        standard_sample_tubes = 0
    else:
        standard_sample_tubes = 1  

    #### Calculating samples per rack
    if plankton.sample_tube_type == "PCR_strips":
        possible_strip_locations = {
            1:['6'],
            2:['3','9'],
            3:['2','7','11'],
            4:['2','5','8','11'],
            } 
        sample_loc = possible_strip_locations[math.ceil(plankton.number_of_samples/8/3)]
        samples_per_rack = 8 * len(sample_loc)
    
    if plankton.sample_tube_type == "1.5mL_tubes":
        sample_loc = False
        samples_per_rack = 24
    
    number_of_sample_racks = math.ceil(plankton.number_of_samples/samples_per_rack)
    
    #### Pipette tips
    # Calculates amount of tips needed for the mastermix and sample
    tips_mastermix = LW.amount_of_tips(plankton.mastermix_volume,
                                        total_reactions,
                                        16,
                                        19)
    tips_sample = LW.amount_of_tips(plankton.sample_volume,
                                    total_reactions - number_of_standard_dilution_samples,
                                    1,
                                    15)
    
    # Calculates total amount of tips needed
    p20_tips_needed = tips_mastermix[0] + tips_sample[0]
    p300_tips_needed = tips_mastermix[1] + tips_sample[1]
    
    # Calculates how many tip racks you need and defines the pipette
    tip_racks_p20, P20 = LW.number_of_tipracks('A1',
                                               p20_tips_needed + 7)
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
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================    

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### PIPETTE TIPS
    tips_20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'tipone_20uL',
                              amount = tip_racks_p20,
                              deck_positions = [7],
                              protocol = protocol)
    tips_300 = LW.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               amount = tip_racks_p300,
                               deck_positions = [4],
                               protocol = protocol)     
    
    #### PIPETTES
    left = 'P20multi'
    if P300:
        right = 'P300'
    else:
        right = False       
    left_pipette, right_pipette = LW.loading_pipettes(left,
                                                      right,
                                                      tips_20,
                                                      'A1', 
                                                      tips_300,
                                                      starting_tip_p300,
                                                      protocol)
    #### MASTERMIX
    # Load mastermix rack
    mastermix_racks = LW.loading_tube_racks(simulate = simulate,
                                            tube_type = reagent_tube_type_mastermix,
                                            reagent_type = 'Mastermix',
                                            amount = number_of_tubes_mastermix,
                                            deck_positions = [3],
                                            protocol = protocol)
    # Specific location of mastermix
    mastermix_tube = LW.tube_locations(source_racks = mastermix_racks,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = number_of_tubes_mastermix,
                                       reagent_type = 'mastermix',
                                       volume = plankton.total_mastermix_volume/number_of_tubes_mastermix,
                                       protocol = protocol)
    
    #### SAMPLES   
    # Loading sample plates
    sample_racks = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = plankton.sample_tube_type,
                                         reagent_type = 'sample_rack',
                                         amount = number_of_sample_racks,
                                         deck_positions = [2,5,8],
                                         protocol = protocol)
    
    # Specific location of samples
    sample_tubes_location = LW.tube_locations(source_racks = sample_racks,
                                              specific_columns = sample_loc,
                                              skip_wells = False,
                                              number_of_tubes = plankton.number_of_samples,
                                              reagent_type = 'samples',
                                              volume = 30,
                                              protocol = protocol)

    # STD sample
    STD_rack = LW.loading_tube_racks(simulate = simulate,
                                     tube_type = plankton.STD_tube_type,
                                     reagent_type = 'standard_sample_rack',
                                     amount = 1,
                                     deck_positions = [1],
                                     protocol = protocol)
    STD_tube = LW.tube_locations(source_racks = STD_rack,
                                  specific_columns = False,
                                  skip_wells = False,
                                  number_of_tubes = standard_sample_tubes,
                                  reagent_type = 'standard_samples',
                                  volume = 30,
                                  protocol = protocol)
    STD_sources = STD_tube * plankton.number_of_std_samples
    
    #### QPCR-PLATE
    # Loading qPCR-plate
    qPCR_plate = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = 'plate_96_NIOZholder',
                                           reagent_type = 'qPCR-plate',
                                           amount = 1,
                                           deck_positions = [6],
                                           protocol = protocol)
    
    # Loading destination wells
    reagent_dict = {}
    # Add sample keys dynamically
    sample_keys = ['samples']
    if plankton.number_of_replicates >= 2:
        sample_keys.append('sample_duplicates')
    if plankton.number_of_replicates == 3:
        sample_keys.append('sample_triplicates')    
    for key in sample_keys:
        reagent_dict[key] = plankton.number_of_samples
    # Add control samples
    reagent_dict['NTC'] = plankton.number_of_NTCs
    reagent_dict['standard_samples'] = plankton.number_of_std_samples
    
    destinations = LW.multiple_reagent_tube_locations(source_racks = qPCR_plate,
                                                      specific_columns = False,
                                                      skip_wells = False,
                                                      reagent_and_numbers_dict = reagent_dict,
                                                      volume = plankton.sample_volume,
                                                      protocol = protocol)
    # Unpack and flatten lists
    sample_destination = [dest for dest in destinations[:plankton.number_of_replicates]]
    NTC_destination = destinations[plankton.number_of_replicates]
    STD_destination = destinations[plankton.number_of_replicates + 1]
    # Loading standard dilution series wells                                        
    specific_dilser_columns = ['12','11','10','9']
    dilution_destination = []
    for i in range(plankton.number_of_std_series):
        columns = []
        columns.append(specific_dilser_columns[i])
        destination = LW.tube_locations(source_racks = qPCR_plate,
                                                 specific_columns = columns,
                                                 skip_wells = False,
                                                 number_of_tubes = plankton.lenght_of_std_serie,
                                                 reagent_type = 'dilution_series',
                                                 volume = plankton.sample_volume,
                                                 protocol = protocol)
        dilution_destination += destination
        
    mastermix_destinations = [well for sublist in sample_destination for well in sublist] + NTC_destination + STD_destination + dilution_destination
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Aliquoting mastermix
    # PM.aliquoting_reagent(reagent_source = mastermix_tube,
    #                       reagent_tube_type = reagent_tube_type_mastermix,
    #                       reagent_startvolume = plankton.total_mastermix_volume,
    #                       aliquot_volume = plankton.mastermix_volume,
    #                       destination_wells = mastermix_destinations,
    #                       p20 = left_pipette,
    #                       p300 = right_pipette,
    #                       action_at_bottom = 'continue_at_bottom',
    #                       pause = False,
    #                       protocol = protocol)
    # Transfering samples to plate
    left_pipette.reset_tipracks()
    for i in range(plankton.number_of_replicates):
        sources = sample_tubes_location
        destinations = sample_destination[i]   
        PM.transferring_reagents_multichannel(source_wells = sources,
                                               destination_wells = destinations,
                                               transfer_volume = plankton.sample_volume,
                                               airgap = True,
                                               mix = True,
                                               p20 = left_pipette,
                                               tips_20 = tips_20,
                                               p300 = right_pipette,
                                               tips_300 = tips_300,
                                               protocol = protocol)

    # Transferring standard sample to plate
    left_pipette.configure_nozzle_layout(style=protocol_api.SINGLE, start='H1', tip_racks=tips_20)
    # transferring_reagents(source_wells = source_locations,
    #                               destination_wells = sample_locations,
    #                               transfer_volume = plankton.sample_volume,
    #                               airgap = True,
    #                               mix = True,
    #                               p20 = p20,
    #                               p300 = p300,
    #                               protocol = protocol)
    
    
# ## ============================================================================
 
# ## LIGHTS======================================================================
# ## ============================================================================
#     protocol.set_rail_lights(False)
# ## ============================================================================