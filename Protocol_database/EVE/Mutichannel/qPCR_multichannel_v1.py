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
sys.path.append("/home/maartje/GitHub/OT2/")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules_v6 as PM
from data.user_storage.mollab_modules import LabWare_v3 as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'qPCR with a multichannel v1',
            'description': 'Aliquoting mastermix, samples, standard, room for dilution series'
            }
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    #### Mastermix
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
                       description="Number of unique samples. Include samples but EXCLUDE the Mock & NTC.",
                       default=32,
                       minimum=0,
                       maximum=94,
                       unit="samples")
    parameters.add_float(variable_name="sample_volume",
                         display_name="sample vol per reaction",
                         description="How much sample should each reaction get?",
                         default=3.0,
                         minimum=1.0,
                         maximum=15.0,
                         unit="µL sample")
    parameters.add_int(variable_name="number_of_NTCs",
                       display_name="number of NTCs",
                       description="Number of NTCs.",
                       default=2,
                       minimum=1,
                       maximum=5,
                       unit="NTCs")
    parameters.add_int(variable_name="number_of_replicates",
                       display_name="number of replicates",
                       description="1 means every sample once, 2 means duplicates, 3 means triplicates etc",
                       default=1,
                       minimum=1,
                       maximum=3,
                       unit="replicates")

    #### Standard sample and dilution serie
    parameters.add_int(variable_name="number_of_std_series",
                       display_name="number of dilution series",
                       description="Number of replicates of the dilution serie used for quantification.",
                       default= 3,
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

    #### PCR
    parameters.add_str(variable_name="PCR_tube_type",
                        display_name="PCR tube type",
                        choices=[
                            {"display_name": "PCR-strips", "value": "PCR_strips"},
                            {"display_name": "PCR-plate", "value": "skirted_plate_96"}
                            ],
                        default="skirted_plate_96")

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
    if plankton.starting_tip_p300_row == 'this_is_not_false':
        starting_tip_p300_row = 'F'
    else:
        starting_tip_p300_row = plankton.starting_tip_p300_row
    # Combining the row-variable with the column-variable to create starting tip
    starting_tip_p300 = starting_tip_p300_row + str(plankton.starting_tip_p300_column)
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    #### Pipetting variables
    # Defines MM tube
    if plankton.total_mastermix_volume > 1500 and plankton.mastermix_volume <= 19:
        tube_type = '1.5mL_tubes'
    else:
        tube_type = False
    MM_tube_type, number_of_MM_tubes, max_volume_MM = LW.which_tube_type(plankton.total_mastermix_volume,tube_type)
    
    #### Calculating total amount of reactions
    number_of_standard_dilution_samples = plankton.number_of_std_series * plankton.lenght_of_std_serie
    total_reactions = (plankton.number_of_samples * plankton.number_of_replicates)  + plankton.number_of_NTCs + number_of_standard_dilution_samples + plankton.number_of_std_samples
    
    if plankton.number_of_std_samples == 0:
        standard_sample_tubes = 0
    else:
        standard_sample_tubes = 1

    #### Final and stock racks
    # Possible locations of strips in racks
    possible_strip_locations = {
        1:['6'],
        2:['3','9'],
        3:['2','7','11'],
        4:['2','5','8','11'],
        }     
    # Calculates number of stock racks
    sample_strip_columns = possible_strip_locations[math.ceil((plankton.number_of_samples + standard_sample_tubes)/8/3)]
    samples_per_rack = len(possible_strip_locations[math.ceil((plankton.number_of_samples + standard_sample_tubes)/8/3)])*8
    number_of_sample_racks = int(math.ceil(((plankton.number_of_samples + standard_sample_tubes) / samples_per_rack)))

    #### Calculates the amount of tip racks needed and set pipette True or False
    tip_racks_p20, tip_racks_p300, P20, P300 = LW.number_of_tip_racks_2_0(volumes_aliquoting = plankton.total_mastermix_volume,
                                                                          number_of_aliquotes = total_reactions,
                                                                          volumes_transfering = plankton.mastermix_volume,
                                                                          number_of_transfers = plankton.number_of_samples + standard_sample_tubes,
                                                                          starting_tip_p20 = starting_tip_p20,
                                                                          starting_tip_p300 = starting_tip_p300)
## COMMENTS====================================================================
## ============================================================================
    if total_reactions > 96:
        raise Exception("The amount of samples, including standard series etc. does not fit a 96wells plate")
    else: 
        protocol.comment(f"You have {plankton.number_of_samples} samples and {plankton.number_of_NTCs} NTCs. You also will add {plankton.number_of_std_samples} of standard samples and {plankton.number_of_std_series} standard dilution series with a lenght of {plankton.lenght_of_std_serie} reactions.")
    if plankton.number_of_replicates > 1:
        protocol.comment(f"Your samples will be replicated {plankton.number_of_replicates} times.")
## ============================================================================

# =============================================================================
# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_p20 = LW.loading_tips(simulate,
                               'tipone_20uL',
                               1,
                               [1],
                               protocol)
    tips_p300 = LW.loading_tips(simulate,
                               'opentrons_200uL',
                               tip_racks_p300,
                               [10,11],
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
    #### MASTERMIX
    # Load mastermix rack
    # Loading MM rack
    MM_rack = LW.loading_tube_racks(simulate = simulate,
                                    tube_type = MM_tube_type,
                                    reagent_type = 'mastermix',
                                    amount = 1,
                                    deck_positions = [7],
                                    protocol = protocol)
    # Loading MM tubes
    MM_volume = max_volume_MM/number_of_MM_tubes
    MM_tubes = LW.tube_locations(source_racks = MM_rack,
                                 specific_columns = False,
                                 skip_wells = False,
                                 number_of_tubes = number_of_MM_tubes,
                                 reagent_type = 'mastermix',
                                 volume = MM_volume,
                                 protocol = protocol)
    ## ========================================================================
    #### Samples
    # Loading sample racks
    protocol.pause('WHATCH OUT!!! For partial tip usage, the order of the sample and dilution racks is the opposite of the usual order!!!')
    sample_racks = LW.loading_tube_racks(simulate = simulate, 
                                         tube_type = 'PCR_strips',  
                                         reagent_type = 'samples', 
                                         amount = number_of_sample_racks,
                                         deck_positions = [8,5,2], 
                                         protocol = protocol)
    # Loading stock tubes
    sample_tube_locations, standard_sample_tube_location = LW.multiple_reagent_tube_locations (source_racks = sample_racks,
                                                                                               specific_columns = sample_strip_columns,
                                                                                               skip_wells = False,
                                                                                               reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'standard_samples': standard_sample_tubes},
                                                                                               volume = plankton.sample_volume,
                                                                                               protocol = protocol)
    # For replicates, replicate the sample source tubes
    sample_tube_locations *= plankton.number_of_replicates
    ## ========================================================================
    #### qPCR-PLATE
    # qPCR-PLATE 
    qPCR_plate = LW.loading_tube_racks(simulate = simulate, 
                                       tube_type = "skirted_plate_96",  
                                       reagent_type = 'qPCR-plate', 
                                       amount = 1,
                                       deck_positions = [6], 
                                       protocol = protocol)
    # qPCR-wells
    replicates = {1: [],
                  2: ['sample_duplicates'],
                  3: ['sample_duplicates', 'sample_triplicates']}
    reagent_and_numbers_dict = {'samples': plankton.number_of_samples,
                                **{replicate: plankton.number_of_samples for replicate in replicates[plankton.number_of_replicates]},
                                'NTC': plankton.number_of_NTCs,
                                'standard_samples': plankton.number_of_std_samples}
    qPCR_destinations = LW.multiple_reagent_tube_locations(source_racks = qPCR_plate,
                                                        specific_columns = False,
                                                        skip_wells = False,
                                                        reagent_and_numbers_dict = reagent_and_numbers_dict,
                                                        volume = plankton.sample_volume,
                                                        protocol = protocol)

    sample_destinations, *replicate_destinations, NTC_destinations, STD_destinations = qPCR_destinations
    all_sample_destinations = sample_destinations.copy()
    for replicate in replicate_destinations:
        all_sample_destinations.extend(replicate)

    # standard dilution series wells                                        
    specific_dilser_columns = ['12','11','10','9']
    qPCR_dilution_wells = []
    for i in range(plankton.number_of_std_series):
        columns = []
        columns.append(specific_dilser_columns[i])
        dilutions = LW.tube_locations(source_racks = qPCR_plate,
                                      specific_columns = columns,
                                      skip_wells = False,
                                      number_of_tubes = plankton.lenght_of_std_serie,
                                      reagent_type = 'dilution_series',
                                      volume = plankton.sample_volume,
                                      protocol = protocol)
        qPCR_dilution_wells += dilutions
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Aliquoting mastermix
    left_pipette.reset_tipracks()
    if number_of_MM_tubes == 1:
        action_at_bottom = 'continue_at_bottom'
    else:
        action_at_bottom = 'next_tube'
    flat_qPCR_destinations = [item for sublist in qPCR_destinations for item in sublist]
    PM.aliquoting_reagent(reagent_source = MM_tubes,
                          reagent_tube_type = MM_tube_type,
                          reagent_startvolume = plankton.total_mastermix_volume,
                          aliquot_volume = plankton.mastermix_volume,
                          destination_wells = flat_qPCR_destinations + qPCR_dilution_wells,
                          p20 = left_pipette,
                          tips_20 = tips_p20,
                          p300 = right_pipette,
                          tips_300 = tips_p300,
                          action_at_bottom = action_at_bottom,
                          pause = False,
                          protocol = protocol)

    ## ========================================================================
    # Transfering samples
    PM.transferring_reagents_multichannel(source_wells = sample_tube_locations,
                                          destination_wells = all_sample_destinations,
                                          transfer_volume = plankton.sample_volume,
                                          airgap = True,
                                          mix = True,
                                          p20 = left_pipette,
                                          tips_20 = tips_p20,
                                          p300 = False,
                                          tips_300 = False,
                                          protocol = protocol)
    # Transfering standard sample
    for i in range(plankton.number_of_std_samples):
        STD_destination = STD_destinations[i]
        PM.transferring_reagents_multichannel(source_wells = standard_sample_tube_location,
                                              destination_wells = [STD_destination],
                                              transfer_volume = plankton.sample_volume,
                                              airgap = True,
                                              mix = True,
                                              p20 = left_pipette,
                                              tips_20 = tips_p20,
                                              p300 = False,
                                              tips_300 = False,
                                              protocol = protocol)
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================