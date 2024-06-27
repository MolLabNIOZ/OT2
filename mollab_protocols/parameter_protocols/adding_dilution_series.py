# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
simulate = True
#### Import opentrons protocol API v2
from opentrons import protocol_api
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
            'description': 'adding dilution series to your qPCR plate'}
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
def add_parameters(parameters: protocol_api.Parameters):
    parameters.add_int(variable_name="number_of_std_series",
                       display_name="number of standard series",
                       description="How many standard dilution series do you want?",
                       default=3,
                       minimum=0,
                       maximum=12,
                       unit="series")
    parameters.add_int(variable_name="length_std_series",
                       display_name="length of the standard series",
                       description="How many dilutions are in your series?",
                       default=8,
                       minimum=1,
                       maximum=8,
                       unit="dilutions")
    parameters.add_float(variable_name="sample_volume",
                         display_name="sample volume",
                         description="How much do you want to add per sample?",
                         default=3,
                         minimum=1,
                         maximum=19,
                         unit="µL")
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
    plankton = protocol.params
# =============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Starting tips
    starting_tip_p20_row = plankton.starting_tip_p20_row
    starting_tip_p20_column = plankton.starting_tip_p20_column.strip('this_is_not_an_int')
    starting_tip_p20 = starting_tip_p20_row + starting_tip_p20_column     
    
    #### Pipette tips
    amount_tips_20, amount_tips_300 = LW.amount_of_tips(plankton.sample_volume,
                                                        plankton.number_of_std_series * plankton.length_std_series,
                                                        1,
                                                        15)
    racks_tips_20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                          amount_tips_20)
    tips_20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'tipone_20uL',
                              amount = racks_tips_20,
                              deck_positions = [11,10],
                              protocol = protocol)
 
    
    #### Pipettes
    p20, p300 = LW.loading_pipettes(P20 = P20, 
                                    tips_20 = tips_20,
                                    starting_tip_p20 = starting_tip_p20,
                                    P300 = False, 
                                    tips_300 = False,
                                    starting_tip_p300 = False,
                                    protocol = protocol)
    
    #### Loading labware
    # Loading dilution serie
    dilution_racks = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = 'PCR_strips',
                                           reagent_type = 'dilution_serie',
                                           amount = 1,
                                           deck_positions = [8],
                                           protocol = protocol)
    ## Specific location of tubes
    specific_dilution_columns = ['6']
    protocol.comment(f"Place your dilution strip in column "
                     f"{specific_dilution_columns} please")
    dilution_tubes = LW.tube_locations(source_racks = dilution_racks,
                                       specific_columns = specific_dilution_columns,
                                       skip_wells = False,
                                       number_of_tubes = plankton.length_std_series)
    
    # Loading PCR-plate
    qPCR_plate = LW.loading_tube_racks(simulate = simulate,
                                       tube_type = 'plate_96_NIOZholder',
                                       reagent_type = 'qPCR-plate',
                                       amount = 1,
                                       deck_positions = [7],
                                       protocol = protocol)
    
    #### Define destination wells
    specific_qPCR_columns = ['12','11','10','9','8','7','6','5','4','3','2','1']
    for i in range(plankton.number_of_std_series):
        column = []
        column.append(specific_qPCR_columns[i])
        qPCR_wells = LW.tube_locations(source_racks = qPCR_plate,
                                       specific_columns = column,
                                       skip_wells = False,
                                       number_of_tubes = plankton.length_std_series)
# =============================================================================

# THE ACTUAL PIPETTING=========================================================
# =============================================================================       
        PM.transferring_reagents(source_wells = dilution_tubes,
                                 destination_wells = qPCR_wells,
                                 transfer_volume = plankton.sample_volume,
                                 airgap = True,
                                 mix = True,
                                 p20 = p20,
                                 p300 = p300,
                                 protocol = protocol)
# =============================================================================