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
sys.path.append("C:/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'multichanneltest',
            'description': 'multichannel test'}
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}
# =============================================================================
def run(protocol: protocol_api.ProtocolContext):
# =============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(True)
## ============================================================================    

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_p20 = LW.loading_tips(simulate,
                               'tipone_20uL',
                               96,
                               [1],
                               protocol)
    ## ========================================================================
    #### Sample racks
    # Loading sample plates
    sample_racks = LW.loading_tube_racks(simulate, 
                                         'PCR-strips', 
                                         'Sample_rack', 
                                         1,
                                         [2], 
                                         protocol)
    
    # Specifying the tube wells locations within the sample racks
    sample_tubes =  LW.multiple_reagent_tube_locations(source_racks = sample_racks,
                                                       specific_columns = [6],
                                                       skip_wells = False,
                                                       reagent_and_numbers_dict = {'samples': 8},
                                                       volume = 50,
                                                       protocol = protocol) 
    ## ========================================================================
    #### PCR-plate
    # Loading PCR-plate
    PCR_plate = LW.loading_tube_racks(simulate, 
                                      'plate_96_NIOZholder', 
                                      'PCR_plate', 
                                      1, 
                                      [3], 
                                      protocol)
    
    sample_destinations = LW.multiple_reagent_tube_locations(source_racks = PCR_plate,
                                                                                                 specific_columns = False,
                                                                                                 skip_wells = False,
                                                                                                 reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'Mock': plankton.number_of_Mocks, 'NTC': plankton.number_of_NTCs},
                                                                                                 volume = 0,
                                                                                                 protocol = protocol)   
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
    # transfering samples
    PM.transferring_reagents(sample_tubes + Mock_tubes,
                              sample_destinations + Mock_destination,
                              plankton.sample_volume,
                              True,
                              True,
                              p20,
                              p300,
                              protocol)

## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================   