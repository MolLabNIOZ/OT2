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
sys.path.append("/mnt/c/Program files/Opentrons")
 #### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'CheckIt pipette check',
            'description': 'checking volume accuracy of the OT-2 pipettes'}
requirements = {'apiLevel': '2.18', 'robotType': 'OT-2'}
# =============================================================================

# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    #### which pipettes do you want to test, with what volumes?
    ## P20?
    parameters.add_bool(variable_name="check_p20",
                        display_name="Do you want to check the P20?",
                        description="",
                        default=True)
    # Which tips?
    parameters.add_bool(variable_name="opentrons_tip20",
                        display_name="Check P20 with Opentrons?",
                        description="Do you want to check with the original Opentrons tips?",
                        default=True)
    parameters.add_bool(variable_name="tipone_tip20",
                        display_name="Check P20 with TipOne?",
                        description="Do you want to check with TipOne tips?",
                        default=True)
    # Which volumes?
    parameters.add_int(variable_name="p20_vol_1",
                       display_name="P20 first volume to check",
                       description="If you don't want to check P20, set it to 0",
                       default=1,
                       minimum=0,
                       maximum=20,
                       unit="µL")
    parameters.add_int(variable_name="p20_vol_2",
                       display_name="P20 second volume to check",
                       description="If you don't want another volume, set it to 0",
                       default=5,
                       minimum=0,
                       maximum=20,
                       unit="µL")
    parameters.add_int(variable_name="p20_vol_3",
                       display_name="P20 third volume to check",
                       description="If you don't want another volume, set it to 0",
                       default=20,
                       minimum=0,
                       maximum=20,
                       unit="µL")
    
    
    ## P300
    parameters.add_bool(variable_name="check_p300",
                        display_name="Do you want to check the P300?",
                        description="",
                        default=True)
    # Which tips?
    parameters.add_bool(variable_name="opentrons_tip300",
                        display_name="Check P300 with Opentrons?",
                        description="Do you want to check with the original Opentrons tips?",
                        default=True)
    parameters.add_bool(variable_name="tipone_tip300",
                        display_name="Check P300 with TipOne?",
                        description="Do you want to check with TipOne tips?",
                        default=True)
    
    # Which volumes?
    parameters.add_int(variable_name="p300_vol_1",
                       display_name="P300 first volume to check",
                       description="If you don't want to check P300, set it to 0",
                       default=20,
                       minimum=0,
                       maximum=50,
                       unit="µL")
    parameters.add_int(variable_name="p300_vol_2",
                       display_name="P300 second volume to check",
                       description="If you don't want another volume, set it to 0",
                       default=50,
                       minimum=0,
                       maximum=50,
                       unit="µL")  
    
    
    
def run(protocol: protocol_api.ProtocolContext):
    plankton = protocol.params    
# =============================================================================    

## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(True)
## ============================================================================    

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### CheckIt
    # CheckIt_5 = CheckIt_50 = False
    
    #if 5 >= any([plankton.p20_vol_1,plankton.p20_vol_2,plankton.p20_vol_3,plankton.p300_vol_1,plankton.p300_vol_2]) > 0:
    if simulate:
        import json
        with open("labware/Checkit_5/Checkit_5.json") as labware_file:
            labware = json.load(labware_file)
        CheckIt_5 = protocol.load_labware_from_definition(labware,
                                                          4,
                                                          "CheckIt_5")      
    else:
        CheckIt_5 = protocol.load_labware("checkit_5",
                                          4,
                                          "CheckIt_5")
    
    #if 50 >= any([plankton.p20_vol_1,plankton.p20_vol_2,plankton.p20_vol_3,plankton.p300_vol_1,plankton.p300_vol_2]) > 5:
    if simulate:
        import json
        with open("labware/Checkit_50/Checkit_50.json") as labware_file:
            labware = json.load(labware_file)
        CheckIt_50 = protocol.load_labware_from_definition(labware,
                                                          5,
                                                          "CheckIt_50")      
    else:
        CheckIt_50 = protocol.load_labware("checkit_50",
                                           5,
                                           "CheckIt_50")   
    #### TIPS
    tips_20 = []
    tips_300 = []
    if plankton.check_p20:
        if plankton.opentrons_tip20:
            opentrons_20 = LW.loading_tips(simulate = simulate,
                                           tip_type = 'opentrons_20uL',
                                           amount = 1,
                                           deck_positions = [10],
                                           protocol = protocol)
            tips_20 += opentrons_20
            
        if plankton.tipone_tip20:
            tipone_20 = LW.loading_tips(simulate = simulate,
                                           tip_type = 'tipone_20uL',
                                           amount = 1,
                                           deck_positions = [7],
                                           protocol = protocol)
            tips_20 += tipone_20
            
    if plankton.check_p300:
        if plankton.opentrons_tip300:
            opentrons_200 = LW.loading_tips(simulate = simulate,
                                           tip_type = 'opentrons_200uL',
                                           amount = 1,
                                           deck_positions = [11],
                                           protocol = protocol)
            tips_300 += opentrons_200
            
        if plankton.tipone_tip300:
            tipone_300 = LW.loading_tips(simulate = simulate,
                                          tip_type = 'tipone_300uL',
                                          amount = 1,
                                          deck_positions = [8],
                                          protocol = protocol)
            tips_300 += tipone_300
    
    #### PIPETTES
    p20, p300 = LW.loading_pipettes(plankton.check_p20,
                                    tips_20,
                                    "A1",
                                    plankton.check_p300, 
                                    tips_300,
                                    "A1",
                                    protocol)

## ============================================================================

## CHECKING====================================================================
## ============================================================================
    #### Set destination wells
    remaining_CheckIt_5_wells = []
    remaining_CheckIt_50_wells = []
    for well in CheckIt_5.columns_by_name()["1"]:
        remaining_CheckIt_5_wells.append(well)
    for well in CheckIt_50.columns_by_name()["1"]:
        remaining_CheckIt_50_wells.append(well)
    
    # Check p20
    if plankton.check_p20:
        pipette = p20        
        volumes = [plankton.p20_vol_1,plankton.p20_vol_2,plankton.p20_vol_3]
        for tip_rack in tips_20:
            tips = ['A1','B1','C1']
            for volume, tip in zip(volumes, tips):
                if 0 < volume <= 5:
                    CheckIt = CheckIt_5
                    wells = remaining_CheckIt_5_wells
                else:
                    CheckIt = CheckIt_50
                    wells = remaining_CheckIt_50_wells          
            
                pipette.pick_up_tip(tip_rack[tip])
                pipette.aspirate(volume, CheckIt.wells_by_name()['A2'].bottom(2))
                pipette.dispense(volume, wells[0].bottom(1))
                pipette.drop_tip()
                wells.pop(0)
    
            if CheckIt == CheckIt_5:
                remaining_CheckIt_5_wells = wells
            if CheckIt == CheckIt_50:
                remaining_CheckIt_50_wells = wells
    # Check p300
    if plankton.check_p300:
        pipette = p300        
        volumes = [plankton.p300_vol_1,plankton.p300_vol_2]
        for tip_rack in tips_300:
            tips = ['A1','B1','C1']
            for volume, tip in zip(volumes, tips):
                if 0 < volume <= 5:
                    CheckIt = CheckIt_5
                    wells = remaining_CheckIt_5_wells
                else:
                    CheckIt = CheckIt_50
                    wells = remaining_CheckIt_50_wells          
            
                pipette.pick_up_tip(tip_rack[tip])
                pipette.aspirate(volume, CheckIt.wells_by_name()['A2'].bottom(2))
                pipette.dispense(volume, wells[0].bottom(1))
                pipette.drop_tip()
                wells.pop(0)
    
            if CheckIt == CheckIt_5:
                remaining_CheckIt_5_wells = wells
            if CheckIt == CheckIt_50:
                remaining_CheckIt_50_wells = wells
    

## ============================================================================
    
## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================        
        