# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 09:46:56 2024
@author: rdebeer
"""
# VARIABLES TO SET#!!!=========================================================
# This is the only region where you are allowed to change variables
# =============================================================================
#### Starting_tips
starting_tip_p20 = 'F4'
 # If applicable: What is the starting position of the first 20µL tip?

#### information about the standard dilution serie (std)  
number_of_std_series = 2
# Determines how often the std is used on the plate
length_std_series = 8
# The ammount of dilution within the std


# How much sample do you want to add?
sample_volume = 2
    #NOTE: this has to be the same as the sample volume from the qPCR protocol

# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
#### Simulation or robot run
simulate = False

#### Import opentrons protocol API v2
from opentrons import protocol_api
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
                        
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {
    'protocolName': 'Adding_dilution_serie.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('A protocol for the dilution of many primers.')}
requirements = {
    'apiLevel': '2.18',
    'robotType': 'OT-2'}

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
    tips_20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'tipone_20uL',
                              amount = 2,
                              deck_positions = [11,10],
                              protocol = protocol)
    
    p20, p300 = LW.loading_pipettes(P20 = True, 
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
                                      number_of_tubes = length_std_series)
    
    # Loading PCR-plate
    qPCR_plate = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = 'plate_96_NIOZholder',
                                           reagent_type = 'qPCR-plate',
                                           amount = 1,
                                           deck_positions = [7],
                                           protocol = protocol)
    
    ## Defines the columns you need
    specific_qPCR_columns = ['12','11','10','9','8','7','6','5','4','3','2','1']
    for i in range(number_of_std_series):
        column = []
        column.append(specific_qPCR_columns[i])
        qPCR_wells = LW.tube_locations(source_racks = qPCR_plate,
                                 specific_columns = column,
                                 skip_wells = False,
                                 number_of_tubes = length_std_series)
        PM.transferring_reagents(source_wells = dilution_tubes,
                                 destination_wells = qPCR_wells,
                                 transfer_volume = sample_volume,
                                 airgap = True,
                                 mix = True,
                                 p20 = p20,
                                 p300 = p300,
                                 protocol = protocol)          