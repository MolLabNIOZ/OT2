# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
simulate = False
#### Import opentrons protocol API v2
from opentrons import protocol_api
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
            'protocolName': 'Preparing a Tapestation-plate V2.1',
            'description': 'Preparing the Tapestation-plate for any tapestation kit'
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

def run(protocol: protocol_api.ProtocolContext):
    plankton = protocol.params
# =============================================================================
    
## CONVERTING  VARIABLES=======================================================
## ============================================================================
    #### Starting tips
    starting_tip_p20 = plankton.starting_tip_p20_row + str(plankton.starting_tip_p20_column)  

    #### Definingen volumes based on tapestation kit
    # Setting dictonary with the possible kits and their respective volumes
    tapestation_kits_dict = {
        'D1000': {'sample_volume': 1, 'buffer_volume': 3, 'mixing_volume': 2},
        'D5000': {'sample_volume': 1, 'buffer_volume': 10, 'mixing_volume': 5},
        'gDNA_kit': {'sample_volume': 1, 'buffer_volume': 10, 'mixing_volume': 5},
        'RNA_kit': {'sample_volume': 1, 'buffer_volume': 5, 'mixing_volume': 2.5}
        }    
    # Setting the sample, buffer and mixing volumes depending on the dict
    sample_volume = tapestation_kits_dict[plankton.tapestation_kit]['sample_volume']
    buffer_volume = tapestation_kits_dict[plankton.tapestation_kit]['buffer_volume']
    mixing_volume = tapestation_kits_dict[plankton.tapestation_kit]['mixing_volume']
## ============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================    
    #### Tapestation buffer
    ### Calculate how much buffer is needed for the amount of samples (+10%)
    total_buffer_volume = buffer_volume * (plankton.number_of_samples + 10)
## ============================================================================
## COMMENTS====================================================================
## ============================================================================
    protocol.comment(f"Put {total_buffer_volume} µL of sample buffer from de "
                     f"{plankton.tapestation_kit} kit in an amber 1.5mL tube. "
                     f"Place the tube in A1 of the rack named '1.5mL ts buffer tube'") 
## ============================================================================
# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### PIPETTE TIPS    
    ### Calculate how many p20 tips are needed
    ## Tips needed for buffer transfer
    tips_buffer = LW.amount_of_tips(buffer_volume,
                                    plankton.number_of_samples,
                                    16,
                                    19)
    ## Tips needed for sample transfer
    tips_sample = LW.amount_of_tips(sample_volume,
                                    plankton.number_of_samples,
                                    1,
                                    15)
    ## Add them up
    amount_tips_20 = tips_buffer[0] + tips_sample[0]
    
    ### Defines how much P20 tip racks are needed
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                               amount_tips_20)
    
    ### Loading tip racks
    tips_p20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'tipone_20uL',
                              amount = tip_racks_p20,
                              deck_positions = [7,10],
                              protocol = protocol)
    
    ### Pipettes
    p20, p300 = LW.loading_pipettes(P20, 
                                    tips_p20,
                                    starting_tip_p20,
                                    False, 
                                    [],
                                    "",
                                    protocol) 
    #### LABWARE
    ### Tapestation sample buffer
    ## Rack
    ts_buffer_rack = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = '1.5mL_tubes',
                                           reagent_type = 'tapestation sample buffer',
                                           amount = 1,
                                           deck_positions = [6],
                                           protocol = protocol)
    ## Tube
    ts_buffer_tube = LW.tube_locations(source_racks = ts_buffer_rack,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = 1,
                                       reagent_type = 'tapestation_buffer',
                                       volume = total_buffer_volume,
                                       protocol = protocol)
    
    ### Samples
    ## Racks
    sample_plate = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = 'plate_96_NIOZholder',
                                         reagent_type = 'sample_plate',
                                         amount = 1,
                                         deck_positions = [4],
                                         protocol = protocol)   
    
    ## Tube location
    source_wells = LW.tube_locations(source_racks = sample_plate,
                                     specific_columns = False,
                                     skip_wells = False,
                                     number_of_tubes = plankton.number_of_samples,
                                     reagent_type = 'samples',
                                     volume = 25,
                                     protocol = protocol)
    
    ### Destination plate
    ## Racks
    destination_plate = LW.loading_tube_racks(simulate = simulate,
                                              tube_type = 'plate_96_NIOZholder',
                                              reagent_type = 'destination_plate',
                                              amount = 1,
                                              deck_positions = [5],
                                              protocol = protocol)    
    ## Tubes
    destination_wells = LW.tube_locations(source_racks = destination_plate,
                                          specific_columns = False,
                                          skip_wells = False,
                                          number_of_tubes = plankton.number_of_samples,
                                          reagent_type = 'tapestation_sample',
                                          volume = 0,
                                          protocol = protocol)
## ============================================================================
    
# THE ACTUAL PIPETTING=========================================================
# =============================================================================    
    #### Tapestation buffer
    PM.aliquoting_reagent(reagent_source = ts_buffer_tube,
                          reagent_tube_type = '1.5mL_tubes',
                          reagent_startvolume = total_buffer_volume,
                          aliquot_volume = buffer_volume,
                          destination_wells = destination_wells,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'continue_at_bottom',
                          pause = False,
                          protocol = protocol)
    
    #### Sample
    PM.transferring_reagents_no_bubbles(source_wells = source_wells,
                             destination_wells = destination_wells,
                             transfer_volume = sample_volume,
                             mix = mixing_volume,
                             p20 = p20,
                             p300 = p300,
                             protocol = protocol)
## ============================================================================