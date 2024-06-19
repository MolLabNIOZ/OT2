# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
simulate = True
#### Import opentrons protocol API v2
from opentrons import protocol_api
#### For simulating in the app, set pathway to modules
import sys
sys.path.append("C:/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW                       
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'mastermix_and_barcoded_primers',
            'description': 'aliquoting mix and distributing barcoded primers'}
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Mastermix
    parameters.add_int(variable_name="total_mastermix_volume",
                       display_name="total mastermix volume",
                       description="How much volume is in your mastermix tube?",
                       default=0,
                       minimum=0,
                       maximum=50000,
                       unit="µL MM")
    parameters.add_int(variable_name="mastermix_volume",
                       display_name="mastermix volume per reaction",
                       description="How much mastermix should each reaction get?",
                       default=0,
                       minimum=0,
                       maximum=50,
                       unit="µL MM")
    #### Samples/Barcodes
    parameters.add_int(variable_name="number_of_barcodes",
                       display_name="number of unique barcodes",
                       description="Number of unique barcode combinations. Include samples, mock, NTC, etc.",
                       default=96,
                       minimum=0,
                       maximum=96,
                       unit="barcodes")
    parameters.add_int(variable_name="primer_vol",
                       display_name="primer volume",
                       description="How much (µL) should be added of each primer?",
                       default=3,
                       minimum=0,
                       maximum=5,
                       unit="µL primer")    
    parameters.add_int(variable_name="skipped_forward_barcodes",
                       display_name="forwards to skip",
                       description="How many forward barcodes should WALL-E skip?",
                       default=0,
                       minimum=0,
                       maximum=95,
                       unit="barcodes")
    parameters.add_int(variable_name="skipped_reverse_barcodes",
                       display_name="reverses to skip",
                       description="How many reverse barcodes should WALL-E skip?",
                       default=0,
                       minimum=0,
                       maximum=95,
                       unit="barcodes")
    parameters.add_int(variable_name="strips_per_rack",
                       display_name="strips per rack",
                       description="How many strips do you want in each strip_rack?",
                       default=6,
                       minimum=1,
                       maximum=6,
                       unit="strips")
    
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
                       description="What column number is the starting tip in?",
                       default=1,
                       minimum=1,
                       maximum=12,
                       unit="")
    
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
                       description="What column number is the starting tip in?",
                       default=1,
                       minimum=1,
                       maximum=12,
                       unit="")

def run(protocol: protocol_api.ProtocolContext):    
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
    strips_per_rack = protocol.params.strips_per_rack
    print(strips_per_rack)

## ============================================================================



## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(True)
## ============================================================================    






    