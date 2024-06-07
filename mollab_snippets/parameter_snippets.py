# -*- coding: utf-8 -*-
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
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    parameters.add_int(variable_name="",
                       display_name="",
                       description="",
                       default=,
                       minimum=,
                       maximum=,
                       unit="")
    parameters.add_str(variable_name="",    
                       display_name="",
                       choices=[
                           {"display_name": "A", "value": "A"},
                           ],
                       default="A")
    
    
    
    #### TIPS
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
    
    
protocol.params.variable_name

