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
sys.path.append("C:/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'adding_sample_to_PCR_plate',
            'description': 'adding sample to the PCR plate with barcoded primers'}
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    
    #### Samples
    parameters.add_int(variable_name="number_of_reactions",
                       display_name="number of unique reactions",
                       description="Number of unique reactions. Include samples, mock, NTC, etc.",
                       default=96,
                       minimum=0,
                       maximum=96,
                       unit="reactions")
    parameters.add_int(variable_name="number_of_NTCs",
                       display_name="number of NTCs",
                       description="Number of NTCs. A NTC is a reaction without any template volume added.",
                       default=1,
                       minimum=0,
                       maximum=5,
                       unit="reactions")
    parameters.add_str(variable_name="sample_tube_type",    
                       display_name="sample tube type",
                       choices=[
                               {"display_name": "PCR-strips", "value": "PCR_strips"},
                               {"display_name": "1.5mL_tubes", "value": "1.5mL_tubes"},
                               ],
                       default="PCR_strips")
    parameters.add_int(variable_name="sample_strips_per_rack",
                       display_name="sample strips per rack",
                       description="How many strips with samples do you want in each strip_rack?",
                       default=3,
                       minimum=1,
                       maximum=3,
                       unit="strips")
    parameters.add_float(variable_name="sample_volume",
                       display_name="sample volume per reaction",
                       description="How much sample should each reaction get?",
                       default=0.0,
                       minimum=0.0,
                       maximum=50.0,
                       unit="µL sample")
    
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
    parameters.add_str(variable_name="starting_tip_p20_column",    
                       display_name="starting tip p20 column",
                       choices=[
                           {"display_name": " 1", "value": " 1"},
                           {"display_name": " 2", "value": " 2"},
                           {"display_name": " 3", "value": " 3"},
                           {"display_name": " 4", "value": " 4"},
                           {"display_name": " 5", "value": " 5"},
                           {"display_name": " 6", "value": " 6"},
                           {"display_name": " 7", "value": " 7"},
                           {"display_name": " 8", "value": " 8"},
                           {"display_name": " 9", "value": " 9"},
                           {"display_name": " 10", "value": " 10"},
                           {"display_name": " 11", "value": " 11"},
                           {"display_name": " 12", "value": " 12"}
                           ],
                       default=" 1")
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
    parameters.add_str(variable_name="starting_tip_p300_column",    
                       display_name="starting tip p300 column",
                       choices=[
                           {"display_name": " 1", "value": " 1"},
                           {"display_name": " 2", "value": " 2"},
                           {"display_name": " 3", "value": " 3"},
                           {"display_name": " 4", "value": " 4"},
                           {"display_name": " 5", "value": " 5"},
                           {"display_name": " 6", "value": " 6"},
                           {"display_name": " 7", "value": " 7"},
                           {"display_name": " 8", "value": " 8"},
                           {"display_name": " 9", "value": " 9"},
                           {"display_name": " 10", "value": " 10"},
                           {"display_name": " 11", "value": " 11"},
                           {"display_name": " 12", "value": " 12"}
                           ],
                       default=" 1")
    
    #### Lights/Pause
    parameters.add_bool(variable_name="lights_on",
                        display_name="lights on",
                        description="Do you want the lights turned ON?",
                        default=True)
    parameters.add_bool(variable_name="pause",
                        display_name="pause after mix",
                        description="Do you want to pause after adding mix, before adding primers?",
                        default=False)
    
def run(protocol: protocol_api.ProtocolContext):
    # Sets p as variable for protocol.params, this will make it all shorter
    p = protocol.params
# =============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
    number_of_reactions = p.number_of_reactions - p.number_of_NTCs

    if p.sample_tube_type == 'PCR_strips':
        #### Location of primer strips in racks
        possible_sample_locations = {
        1:['6'],
        2:['3','9'],
        3:['2','7','11']}
        
        # Calculates how many sample racks were needed
        sample_loc = possible_sample_locations[p.sample_strips_per_rack]
        sample_per_rack = 8 * len(sample_loc)
        number_of_sample_racks = math.ceil(number_of_reactions/sample_per_rack)
    else:
        sample_loc = False
        number_of_sample_racks = math.ceil(number_of_reactions/24)
    
    # Sets variables for the starting tips
    starting_tip_p20 = p.starting_tip_p20_row +  p.starting_tip_p20_column.strip()
    starting_tip_p300 = p.starting_tip_p300_row +  p.starting_tip_p300_column.strip()
    
    # Calculates the amount of tips needed
    p20_tips_needed, p300_tips_needed = LW.amount_of_tips(p.sample_volume,
                                                          p.number_of_reactions,
                                                          1,
                                                          15)
    
    # Defines how much P20 and P300 tip racks you need and if the pipette is True/False
    tip_racks_p20, P20 = LW.number_of_tipracks(starting_tip_p20,
                                          p20_tips_needed)
    tip_racks_p300, P300 = LW.number_of_tipracks(starting_tip_p300,
                                           p300_tips_needed) 
## ============================================================================

## COMMENTS====================================================================
## ============================================================================

## ============================================================================

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(p.lights_on)
## ============================================================================    

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    tips_p20 = LW.loading_tips(simulate,
                               'tipone_20uL',
                               tip_racks_p20,
                               [1,4,7,10],
                               protocol)
    tips_p300 = LW.loading_tips(simulate,
                               'opentrons_200uL',
                               tip_racks_p300,
                               [10,7,4,1],
                               protocol)
    
    #### Sample racks
    # Loading sample plates
    sample_racks = LW.loading_tube_racks(simulate, 
                                         p.sample_tube_type, 
                                         'Sample_rack', 
                                         number_of_sample_racks, 
                                         [2,5,8,11], 
                                         protocol)
    
    # Specifying the tube wells locations within the sample racks
    sample_tubes = LW.tube_locations(sample_racks,
                                     sample_loc,
                                     False,
                                     number_of_reactions)
   
    #### PCR-plate
    # Loading PCR-plate
    PCR_plate = LW.loading_tube_racks(simulate, 
                                       'plate_96_NIOZholder', 
                                       'PCR_plate', 
                                       1, 
                                       [6], 
                                       protocol)
    # Sample destinations
    sample_destions = LW.tube_locations(PCR_plate,
                                        False,
                                        False,
                                        number_of_reactions)
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
    PM.transferring_reagents(sample_tubes,
                            sample_destions,
                            p.sample_volume,
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