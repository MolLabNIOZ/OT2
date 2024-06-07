# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 09:46:56 2024
@author: rdebeer
"""
# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
import sys
sys.path.append("C:/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW                       
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology'}
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}

def add_parameters(parameters: protocol_api.Parameters):
    parameters.add_bool(variable_name="simulate",
                        display_name="simulate",
                        description="switch off when running on the robot",
                        default=True)
    parameters.add_int(variable_name="number_of_std_series",
                       display_name="number of standard series",
                       description="How many standard dilution series do you want?",
                       default=3,
                       minimum=0,
                       maximum=12,
                       unit="standard series")
    parameters.add_int(variable_name="length_std_series",
                       display_name="length of the standard series",
                       description="How many dilutions are in your series?",
                       default=8,
                       minimum=1,
                       maximum=8,
                       unit="dilutions")
    parameters.add_int(variable_name="sample_volume",
                       display_name="sample volume",
                       description="How much do you want to add per sample?",
                       unit="µL")
    parameters.add_str(variable_name="starting_tip_p20",    
                       display_name="starting tip p20",
                       default="A1")
    
def run(protocol: protocol_api.ProtocolContext):
# =============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    # If water_volume >= 19µL use pp20 and p300, otherwise use p20 only
    tips_20 = LW.loading_tips(simulate = protocol.params.simulate,
                              tip_type = 'tipone_20uL',
                              amount = 2,
                              deck_positions = [11,10],
                              protocol = protocol)
    
    p20, p300 = LW.loading_pipettes(P20 = True, 
                                    tips_20 = tips_20,
                                    starting_tip_p20 = "protocol.params.starting_tip_p20",
                                    P300 = False, 
                                    tips_300 = False,
                                    starting_tip_p300 = False,
                                    protocol = protocol)
    #### Loading labware
    # Loading dilution serie
    dilution_racks = LW.loading_tube_racks(simulate = protocol.params.simulate,
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
                                       number_of_tubes = protocol.params.length_std_series)
    
    # Loading PCR-plate
    qPCR_plate = LW.loading_tube_racks(simulate = protocol.params.simulate,
                                       tube_type = 'plate_96_NIOZholder',
                                       reagent_type = 'qPCR-plate',
                                       amount = 1,
                                       deck_positions = [7],
                                       protocol = protocol)
    
    ## Defines the columns you need
    specific_qPCR_columns = ['12','11','10','9','8','7','6','5','4','3','2','1']
    for i in range(protocol.params.number_of_std_series):
        column = []
        column.append(specific_qPCR_columns[i])
        qPCR_wells = LW.tube_locations(source_racks = qPCR_plate,
                                 specific_columns = column,
                                 skip_wells = False,
                                 number_of_tubes = protocol.params.length_std_series)
        PM.transferring_reagents(source_wells = dilution_tubes,
                                 destination_wells = qPCR_wells,
                                 transfer_volume = protocol.params.sample_volume,
                                 airgap = True,
                                 mix = True,
                                 p20 = p20,
                                 p300 = p300,
                                 protocol = protocol)          