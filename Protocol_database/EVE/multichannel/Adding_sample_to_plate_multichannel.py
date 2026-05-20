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
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules_v5 as PM
from data.user_storage.mollab_modules import LabWare_v3 as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Adding sample to barcoded PCR-plate multichannel V1',
            'description': 'Adding your samples to the PCR plate with (barcoded) primers.'}
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    #### Samples
    parameters.add_int(variable_name="number_of_samples",
                       display_name="number of unique samples",
                       description="Number of unique samples. Include samples but EXCLUDE the Mock & NTC.",
                       default=80,
                       minimum=0,
                       maximum=94,
                       unit="samples")
    parameters.add_int(variable_name="number_of_Mocks",
                       display_name="number of unique Mocks",
                       description="Number of unique Mocks. Could be 0 or 1",
                       default=1,
                       minimum=0,
                       maximum=1,
                       unit="Mocks")
    parameters.add_int(variable_name="number_of_NTCs",
                       display_name="number of NTCs",
                       description="Number of NTCs. A NTC is a reaction without any template volume added.",
                       default=1,
                       minimum=1,
                       maximum=5,
                       unit="reactions")
    
    parameters.add_str(variable_name="sample_tube_type",    
                       display_name="sample tube type",
                       choices=[
                               {"display_name": "PCR-strips", "value": "PCR_strips"},
                               {"display_name": "1.5mL_tubes", "value": "1.5mL_tubes"},
                               ],
                       default="PCR_strips")
    parameters.add_float(variable_name="sample_volume",
                       display_name="sample volume per reaction",
                       description="How much sample should each reaction get?",
                       default=1.0,
                       minimum=0.5,
                       maximum=15.0,
                       unit="µL")
    
    #### Lights/Pause  
    parameters.add_bool(variable_name="lights_on",
                        display_name="lights on",
                        description="Do you want the lights turned ON?",
                        default=True)    

def run(protocol: protocol_api.ProtocolContext):
    # Sets p as variable for protocol.params, this will make it all shorter
    plankton = protocol.params
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    number_of_tubes = plankton.number_of_samples + plankton.number_of_Mocks
    if plankton.sample_tube_type == 'PCR_strips':       
        # Calculates how many sample racks were needed
        
        possible_strip_locations = {
            1:['6'],
            2:['3','9'],
            3:['2','7','11'],
            4:['2','5','8','11'],
            } 
        sample_loc = possible_strip_locations[math.ceil(number_of_tubes/8/3)]
        samples_per_rack = 8 * len(sample_loc)
        number_of_sample_racks = math.ceil(number_of_tubes/samples_per_rack)
    else:
        sample_loc = False
        number_of_sample_racks = math.ceil(number_of_tubes/24)
# =============================================================================
        
## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(plankton.lights_on)
## ============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ## ========================================================================
    #### Pipette tips
    tips_20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'tipone_20uL',
                              amount = 1,
                              deck_positions = [4],
                              protocol = protocol)
    ### Loading pipettes
    left_pipette, right_pipette = LW.loading_pipettes('P20multi',
                                                      False,
                                                      tips_20,
                                                      'A1',
                                                      False, 
                                                      False,
                                                      protocol)
    ## ========================================================================
    #### Sample racks
    # Loading sample plates
    sample_racks = LW.loading_tube_racks(simulate, 
                                         plankton.sample_tube_type, 
                                         'Sample_rack', 
                                         number_of_sample_racks, 
                                         [2,5,8], 
                                         protocol)
    # Specifying the tube wells locations within the sample racks
    sample_tubes, Mock_tubes =  LW.multiple_reagent_tube_locations(source_racks = sample_racks,
                                                                   specific_columns = sample_loc,
                                                                   skip_wells = False,
                                                                   reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'Mock': plankton.number_of_Mocks},
                                                                   volume = 10,
                                                                   protocol = protocol)
    ## ========================================================================
    #### PCR-plate
    # Loading PCR-plate
    PCR_plate = LW.loading_tube_racks(simulate, 
                                       'plate_96_NIOZholder', 
                                       'PCR_plate', 
                                       1,
                                       [6], 
                                       protocol)
    sample_destinations, Mock_destination, NTC_destinations = LW.multiple_reagent_tube_locations(source_racks = PCR_plate,
                                                                                                 specific_columns = False,
                                                                                                 skip_wells = False,
                                                                                                 reagent_and_numbers_dict = {'samples': plankton.number_of_samples, 'Mock': plankton.number_of_Mocks, 'NTC': plankton.number_of_NTCs},
                                                                                                 volume = 0,
                                                                                                 protocol = protocol)
## ============================================================================

## COMMENTS====================================================================
## ============================================================================
    protocol.comment("Put your sample strips in the following columns"
                     f"{sample_loc}")
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
    left_pipette.reset_tipracks()
    PM.transferring_reagents_multichannel(source_wells = sample_tubes + Mock_tubes,
                                          destination_wells = sample_destinations + Mock_destination,
                                          transfer_volume = plankton.sample_volume,
                                          airgap = True,
                                          mix = True,
                                          p20 = left_pipette,
                                          tips_20 = tips_20,
                                          p300 = False,
                                          tips_300 = False,
                                          protocol = protocol)
## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================