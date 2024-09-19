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
            'protocolName': 'Preparing Qubit plate V1.0',
            'description': 'Preparing a 96-wells qPCR-plate for performing the HS or BR Qubit on the CFX96 or OPUS96.'
            }
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Samples
    parameters.add_int(variable_name="number_of_samples",
                       display_name="How many samples do you have?",
                       description="Number of samples you want to run on the Qubit. Max is 88 samples.",
                       default=88,
                       minimum=0,
                       maximum=88,
                       unit="samples")
    parameters.add_int(variable_name="number_of_standards",    
                       display_name="number of standards",
                       choices=[
                           {"display_name": "2", "value": 2},
                           {"display_name": "4", "value": 4},
                           {"display_name": "8", "value": 8},
                           ],
                       default = 4)    
    parameters.add_str(variable_name="sample_tube_type",    
                       display_name="sample tube type",
                       choices=[
                           {"display_name": "PCR-strips", "value": "PCR_strips"},
                           {"display_name": "PCR-plate", "value": "PCR_plate"},
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
                           {"display_name": "F", "value": "F"},
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
                           {"display_name": "F", "value": "F"},
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
    starting_tip_p20 = plankton.starting_tip_p20_row + str(plankton.starting_tip_p20_column)
    starting_tip_p300 = plankton.starting_tip_p300_row + str(plankton.starting_tip_p300_column)
# =============================================================================

# CALCULATED AND SET VARIABLES=================================================
# This region contains settings and calculations that are later used
# =============================================================================
    #### Qubit mix and added volume
    # Volume of the standard to add
    std_vol = 2
    # Volume of the sample to add
    sample_vol = 1
    
    # How much mix to dispense for standards
    Qmix_vol_standards = 50 - std_vol
    # How much mix to dispense for samples
    Qmix_vol_sample = 50 - sample_vol
    
    # How much Qmix do you need and what tube should be used?
    Qmix_start_volume = (((plankton.number_of_samples * 1.1)*Qmix_vol_sample) + 
                             (9 * Qmix_vol_standards))
    Qmix_tube_type, number_of_tubes, max_volume = LW.which_tube_type(
        total_volume = Qmix_start_volume,
        tube_type = False)
    
    #### Tip racks
    # Pipette tips needed
    tips_mix_standard = LW.amount_of_tips(volumes = Qmix_vol_sample,
                                          number_of_transfers = 8,
                                          tip_change = 16,
                                          max_p20_volume = 19)
    tips_mix_samples = LW.amount_of_tips(volumes = Qmix_vol_sample,
                                          number_of_transfers = plankton.number_of_samples,
                                          tip_change = 16,
                                          max_p20_volume = 19)
    tips_standards = LW.amount_of_tips(volumes = std_vol,
                                          number_of_transfers = 8,
                                          tip_change = 1,
                                          max_p20_volume = 15)
    tips_sample =  LW.amount_of_tips(volumes = sample_vol,
                                          number_of_transfers = plankton.number_of_samples,
                                          tip_change = 1,
                                          max_p20_volume = 15)
    
    # Adds the total amount of tips together
    p20_tips_needed = tips_mix_standard[0] + tips_mix_samples[0] + tips_standards[0] + tips_sample[0]
    p300_tips_needed = tips_mix_standard[1] + tips_mix_samples[1] + tips_standards[1] + tips_sample[1]
    
    # Defines how much P20 and P300 tip racks you need and if the pipette is True/False
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               p20_tips_needed)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip_p300,
                                               p300_tips_needed)
    
    #### Sample racks needed
    if plankton.sample_tube_type == 'PCR_strips':
        sample_loc = [2,7,11]
        samples_per_rack = len(sample_loc)*8
    if plankton.sample_tube_type == '1.5mL_tubes':
        sample_loc = False
        samples_per_rack = 24
    if plankton.sample_tube_type == 'PCR_plate':
        sample_loc = False
        samples_per_rack = 96
    number_of_sample_racks = plankton.number_of_samples/samples_per_rack
    
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    number_of_reactions = plankton.number_of_samples + 8
    
    if number_of_reactions > 96:
        raise Exception(f'You have {number_of_reactions} reactions. ' +
                        'This is more than 96 reactions if you add the NTCs and is not possible.')
    else: 
        protocol.comment(f"You have {plankton.number_of_samples} samples and 8 standards in {plankton.number_of_standards} different concentrations. "
                         "Add {Qmix_start_volume} μL to a {Qmix_tube_type}.")
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================    

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_p20 = LW.loading_tips(simulate = simulate,
                               tip_type = 'tipone_20uL',
                               tip_racks_p20 = tip_racks_p20,
                               deck_positions = [1,4],
                               protocol = protocol)
    tips_p300 = LW.loading_tips(simulate = simulate,
                               tip_type = 'opentrons_200uL',
                               tip_racks_p300 = tip_racks_p300,
                               deck_positions = [7],
                               protocol = protocol)
    ### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20 = P20, 
                                    tips_p20 = tips_p20,
                                    starting_tip_p20 = starting_tip_p20,
                                    P300 = P300, 
                                    tips_p300 = tips_p300,
                                    starting_tip_p300 = starting_tip_p300,
                                    protocol = protocol)
    ## ========================================================================
    #### loading mix rack
    # Mix rack
    mix_rack = LW.loading_tube_racks(simulate = simulate, 
                                     tube_type = Qmix_tube_type, 
                                     reagent_type = 'Qmix', 
                                     amount = 1, 
                                     deck_positions = [9], 
                                     protocol = protocol)
    
    # Defining mix tube
    mix_tube = LW.tube_locations(source_racks = mix_rack,
                                 specific_columns = False,
                                 skip_wells = False,
                                 number_of_tubes = number_of_tubes,
                                 reagent_type = 'Qmix',
                                 volume = Qmix_start_volume,
                                 protocol = protocol)
    ## ========================================================================
    #### loading samples
    # Sample racks
    sample_racks = LW.loading_tube_racks(simulate = simulate, 
                                     tube_type = plankton.sample_tube_type, 
                                     reagent_type = 'Qmix', 
                                     amount = number_of_sample_racks, 
                                     deck_positions = [2,5,8,11], 
                                     protocol = protocol)
    # Defining sample tubes
    sample_tubes = LW.tube_locations(source_racks = sample_racks,
                                     specific_columns = sample_loc,
                                     skip_wells = False,
                                     number_of_tubes = plankton.number_of_samples,
                                     reagent_type = 'samples',
                                     volume = sample_vol/plankton.number_of_samples,
                                     protocol = protocol)
    ## ========================================================================
    #### loading Qubit standards
    # Standard racks
    standard_rack = LW.loading_tube_racks(simulate = simulate, 
                                     tube_type = '1.5mL_tubes', 
                                     reagent_type = 'Standard', 
                                     amount = 1, 
                                     deck_positions = [3], 
                                     protocol = protocol)
    # Defining standard tubes
    standard_tubes = LW.tube_locations(source_racks = standard_rack,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = plankton.number_of_standards,
                                       reagent_type = 'standard_samples',
                                       volume = std_vol/plankton.number_of_standards,
                                       protocol = protocol)
    
    if len(standard_tubes) != 8:
        final_list_standard_tubes = int(8/len(standard_tubes))*standard_tubes
        final_list_standard_tubes.sort()
    else:
        final_list_standard_tubes = standard_tubes
    ## ========================================================================
    #### loading Qubit plate
    # Qubit plate
    qubit_plate = LW.loading_tube_racks(simulate = simulate, 
                                     tube_type = 'plate_96_NIOZholder', 
                                     reagent_type = 'Qubi_plate', 
                                     amount = 1, 
                                     deck_positions = [6], 
                                     protocol = protocol)
    # Defining destination wells
    standard_wells, sample_wells = LW.multiple_reagent_tube_locations(source_racks = qubit_plate,
                                                                      specific_columns = False,
                                                                      skip_wells = False,
                                                                      reagent_and_numbers_dict = {'standard_samples': 8, 'samples': plankton.number_of_samples},
                                                                      volume = 50/(plankton.number_of_samples+8),
                                                                      protocol = protocol)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    #### Aliquoting the Qubit mix
    # Aliquoting of the mix for the standard samples    
    PM.aliquoting_reagent(reagent_source = mix_tube, 
                          reagent_tube_type = Qmix_tube_type, 
                          reagent_startvolume = Qmix_start_volume,
                          aliquot_volume = Qmix_vol_standards,
                          destination_wells = standard_wells,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'continue_at_bottom',
                          pause = False,
                          protocol = protocol)
    # Aliquoting of the mix for the samples    
    PM.aliquoting_reagent(reagent_source = mix_tube, 
                          reagent_tube_type = Qmix_tube_type, 
                          reagent_startvolume = Qmix_start_volume - (8*Qmix_vol_standards),
                          aliquot_volume = Qmix_vol_sample,
                          destination_wells = sample_wells,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'continue_at_bottom',
                          pause = False,
                          protocol = protocol)
    ## ========================================================================
    #### Transfering the samples
    # Transfering standard samples
    PM.transferring_reagents(source_wells = final_list_standard_tubes,
                              destination_wells = standard_wells,
                              transfer_volume = std_vol,
                              airgap = True,
                              mix = True,
                              p20 = p20,
                              p300 = p300,
                              protocol = protocol)
    # Transfering samples
    PM.transferring_reagents(source_wells = sample_tubes,
                              destination_wells = sample_wells,
                              transfer_volume = sample_vol,
                              airgap = True,
                              mix = True,
                              p20 = p20,
                              p300 = p300,
                              protocol = protocol)