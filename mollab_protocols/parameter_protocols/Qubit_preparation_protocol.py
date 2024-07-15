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
                           {"display_name": "A", "PCR strips": "PCR_strips"},
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