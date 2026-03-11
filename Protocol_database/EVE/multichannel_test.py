# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
simulate = True
#### Import opentrons protocol API v2
from opentrons import protocol_api
#### For simulating in the app, set pathway to modules
import sys
sys.path.append("O:/")
sys.path.append("/mnt/c/Program files/Opentrons")
sys.path.append("C:/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules_v5 as PM
from data.user_storage.mollab_modules import LabWare_v3 as LW
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
                               1,
                               [1],
                               protocol)
    #### Pipettes
    left_pipette, right_pipette = LW.loading_pipettes('P20multi',
                                                      False,
                                                      tips_p20,
                                                      'A1',
                                                      False,
                                                      False,
                                                      protocol)
    ## ========================================================================
    #### Sample racks
    # Loading sample plates
    sample_racks = LW.loading_tube_racks(simulate, 
                                         'PCR_strips', 
                                         'Sample_rack', 
                                         1,
                                         [2], 
                                         protocol)
    
    # Specifying the tube wells locations within the sample racks
    sample_tubes =  LW.tube_locations(source_racks = sample_racks,
                                       specific_columns = ['6'],
                                       skip_wells = False,
                                       number_of_tubes = 8,
                                       reagent_type = 'samples',
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
    
    
    
    
    columns_volume = {'1': 5, '2': 2.5, '3': 1, '4': 5, '5': 2.5,'6': 1, '8':2.5, '9': 1, '10': 5, '11': 2.5, '12': 1}
    for column, volume in columns_volume.items():
        sample_destination = LW.tube_locations(source_racks = PCR_plate,
                                               specific_columns = [column],
                                               skip_wells = False,
                                               number_of_tubes = 8,
                                               reagent_type = 'samples',
                                               volume = 50,
                                               protocol = protocol)

## ============================================================================
## PIPETTING===================================================================
## ============================================================================
    # transfering samples
        PM.transferring_reagents_multichannel(source_wells = sample_tubes,
                                              destination_wells = sample_destination,
                                              transfer_volume = volume,
                                              airgap = True,
                                              mix = True,
                                              p20 = left_pipette,
                                              tips_20 = tips_p20,
                                              p300 = right_pipette,
                                              tips_300 = False,
                                              protocol = protocol)

## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================

