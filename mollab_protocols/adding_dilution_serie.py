"""
A protocol designed to transfer a standard dilution series from a strip into a
96 wells plate. The dilution series come at the end of a plate. MasterMix
should already have been added to these wells by EVE.

Edited:
240320 (MB): fixed some details and shortened some parts
             
"""
# VARIABLES TO SET#!!!=========================================================
# This is the only region where you are allowed to change variables
# =============================================================================
#### Starting_tips
starting_tip_p20 = 'A1'
 # If applicable: What is the starting position of the first 20µL tip?

#### information about the standard dilution serie (std)  
number_of_std_series = 3
# How many replicates of the standard dilution series should be added

# How much sample do you want to add?
sample_volume = 2.5
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
    'author': 'NIOZ_MolLab_team',
    'description': ('A protocol for MO, for adding dilution series to a qPCR. '
                    'Adds a specified number of dilution series to the end of '
                    'a qPCR plate.'),
    'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):
# =============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
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
    # Loading PCR_strip rack for the dilution serie
    dilution_racks = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = 'PCR_strips',
                                           reagent_type = 'dilution_series',
                                           amount = 1,
                                           deck_positions = [8],
                                           protocol = protocol)
    ## Specific location of tubes
    column = '6'
    protocol.comment(f"Place your dilution strip in column "
                     f"{column} of a 96_wells plate on deck "
                     f"slot 8 please.")
    dilution_tubes = LW.tube_locations(source_racks = dilution_racks,
                                       specific_columns = [column],
                                       skip_wells = False,
                                       number_of_tubes = 8)
    
    # Loading PCR-plate
    qPCR_plate = LW.loading_tube_racks(simulate = simulate,
                                       tube_type = 'skirted_plate_96',
                                       reagent_type = 'qPCR_plate',
                                       amount = 1,
                                       deck_positions = [9],
                                       protocol = protocol)
    
    ## Specific locations of where the dilutions series should go
    possible_columns = ['12','11','10','9','8','7','6','5','4','3','2','1']
    for i in range(number_of_std_series):
        qPCR_wells = LW.tube_locations(source_racks = qPCR_plate,
                                       specific_columns = [possible_columns[i]],
                                       skip_wells = False,
                                       number_of_tubes = 8)
# =============================================================================

# THE ACTUAL PIPETTING=========================================================
# =============================================================================
        PM.transferring_reagents(source_wells = dilution_tubes,
                                 destination_wells = qPCR_wells,
                                 transfer_volume = sample_volume,
                                 airgap = True,
                                 mix = True,
                                 p20 = p20,
                                 p300 = p300,
                                 protocol = protocol)
# =============================================================================