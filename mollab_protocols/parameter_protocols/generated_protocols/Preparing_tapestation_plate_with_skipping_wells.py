skipped_wells = [0,1,2,3,4,5,44]

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
            'protocolName': 'Preparing a Tapestation-plate with skipping wells {DELETE AFTER USE}V1.0',
            'description': 'Preparing the Tapestation-plate for all the different protocols.'
            }
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
                       default=96,
                       minimum=0,
                       maximum=96,
                       unit="samples")
    
    #### Tapestation kit
    parameters.add_str(variable_name="tapestation_kit",    
                       display_name="Tapestation kit",
                       choices=[
                           {"display_name": "D1000", "value": "D1000"},
                           {"display_name": "D5000", "value": "D5000"},
                           {"display_name": "gDNA kit", "value": "gDNA_kit"},
                           {"display_name": "RNA kit", "value": "RNA_kit"},
                           ],
                       default="D1000")
    
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

def run(protocol: protocol_api.ProtocolContext):
    # Sets p as variable for protocol.params, this will make it all shorter
    plankton = protocol.params
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    #### Total reactions
    total_samples = plankton.number_of_samples - len(skipped_wells)

    #### Definingen the kit type and volumes
    # Setting dictonary with the possible kits
    # Order is sample_volume, buffer_volume, mixing_volume
    tapestation_kits_dict = {
        'D1000': [1, 3, 2],
        'D5000': [ 1,  10,  5],
        'gDNA_kit': [ 1,  10,  5],
        'RNA_kit': [ 1,  5,  2.5]
        }
    
    # Setting the sample, buffer and mixing volumes depending on the dict
    sample_volume = tapestation_kits_dict[plankton.tapestation_kit][0]
    buffer_volume = tapestation_kits_dict[plankton.tapestation_kit][1]
    mixing_volume = tapestation_kits_dict[plankton.tapestation_kit][2]
    
    #### Calculating pipette tips and tip racks
    # Sets variables for the starting tips
    starting_tip_p20 = plankton.starting_tip_p20_row + plankton.starting_tip_p20_column.strip("this_is_not_an_int")
    starting_tip_p300 = 'A1'

    ## Calculates the amount of tips needed
    # Calculates the tips needed for pipetting the sample
    p20_tips_needed_sample, p300_tips_needed_sample = LW.amount_of_tips(sample_volume,
                                                                        total_samples,
                                                                        1,
                                                                        15)

    # Calculates the tips needed for pipetting the buffer
    p20_tips_needed_buffer, p300_tips_needed_buffer = LW.amount_of_tips(buffer_volume,
                                                                        total_samples,
                                                                        16,
                                                                        19)
    # Calculates the total amount of pipette tips needed
    p20_tips_needed = p20_tips_needed_sample + p20_tips_needed_buffer
    p300_tips_needed = p300_tips_needed_sample + p300_tips_needed_buffer
    
    # Defines how much P20 and P300 tip racks you need and if the pipette is True/False
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               p20_tips_needed)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip_p300,
                                               p300_tips_needed)
    
    #### Buffer calculations
    # Calculates how many buffer you need
    buffer_volume_needed = buffer_volume * (total_samples + 10)
## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    protocol.comment(f"You will need {buffer_volume_needed} uL buffer from de {plankton.tapestation_kit} kit in an amber 1.5mL tube. Place the tube in A1 of the rack named '1.5mL ts reagent tube'") 
## ============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_p20 = LW.loading_tips(simulate,
                               'tipone_20uL',
                               tip_racks_p20,
                               [7,10],
                               protocol)
    tips_p300 = LW.loading_tips(simulate,
                               'opentrons_200uL',
                               tip_racks_p300,
                               [8,11],
                               protocol)

    #### Sample racks
    # Loading source plate
    source_plate = LW.loading_tube_racks(simulate, 
                                         'plate_96_NIOZholder', 
                                         'Source_plate', 
                                         1, 
                                         [4], 
                                         protocol)  
    # Specifying the tube wells locations within the source plate
    source_wells = LW.tube_locations(source_plate,
                                     False,
                                     skipped_wells,
                                     total_samples,
                                     'samples',
                                     10,
                                     protocol)
    
    #### Tapestation racks
    # Loading destination plate
    destination_plate = LW.loading_tube_racks(simulate, 
                                              'plate_96_NIOZholder', 
                                              'Destination_plate', 
                                              1, 
                                              [5], 
                                              protocol)
    # Specifying the tube wells locations within the destination plate
    destination_wells = LW.tube_locations(destination_plate,
                                     False,
                                     False,
                                     total_samples,
                                     'tapestation_sample',
                                     0,
                                     protocol)
    
    #### Tapestation buffer
    # Loading the Tapestation buffer rack
    ts_buffer_rack = LW.loading_tube_racks(simulate, 
                                           '1.5mL_tubes', 
                                           'Reagent_rack', 
                                           1, 
                                           [6], 
                                           protocol)
    # Specifying the tube locations within the ts buffer rack
    ts_tube_location = LW.tube_locations(ts_buffer_rack,
                                         False,
                                         False,
                                         1,
                                         'tapestation_buffer',
                                         buffer_volume_needed,
                                         protocol)
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
    # Aliquoting Tapestation buffer
    PM.aliquoting_reagent(ts_tube_location, 
                          '1.5mL_tubes', 
                          buffer_volume_needed,
                          buffer_volume,
                          destination_wells,
                          p20,
                          p300,
                          16,
                          'continue_at_bottom',
                          False,
                          protocol)
    # Transfering samples to Tapestation plate
    PM.transferring_reagents_no_bubbles(source_wells,
                                        destination_wells,
                                        sample_volume,
                                        mixing_volume,
                                        p20,
                                        p300,
                                        protocol)