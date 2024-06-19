"""
Version: Jan_2024
A protocol written to dilute stocks.
"""

# VARIABLES TO SET#!!!=========================================================
# This is the only region where you are allowed to change variables
# =============================================================================
#### Starting_tips
starting_tip_p20 = 'A5'
 # If applicable: What is the starting position of the first 20µL tip?
starting_tip_p300 = 'H8'
 # If applicable: What is the starting position of the first 200µL tip?
  ## If volume-wise p20 or p300 is not used, this variable won't be used.

#### Number of stocks to dilute 
number_to_dilute = 1 # MAX = 144, but preferably max 96
    #!!! excluding tubes/wells to skip!!!
#### Are there stocks you want to skip?
stock_skip_wells = False # False or list of indexes. First sample = index 0
#### If 
dilution_skip_wells = False # False or list of indexes. First sample = index 0

#### In what kind of tube(s) is the stock
stock_tube_type = 'PCR_strips'
    # optional: skirted_plate_96 / plate_96_NIOZholder / non_skirted_plate_96 / 
    #           PCR_strips / 1.5mL_tubes
if stock_tube_type == 'PCR_strips':
    #### Columns of the strips in the strip_rack
    stock_strip_columns = ['2', '5', '8', '11']
    # This determines how many primers you can do at once. 
    # Preferably max 4 strips per rack, but max 6 is possible.

#### In what kind of tube(s) do you want the dilutions
dilution_tube_type = 'PCR_strips'
    # optional: skirted_plate_96 / plate_96_NIOZholder / non_skirted_plate_96 / 
    #           PCR_strips / 1.5mL_tubes  
if dilution_tube_type == 'PCR_strips':
    #### Columns of the strips in the strip_rack
    dilution_strip_columns = ['2', '5', '8', '11']
    # This determines how many primers you can do at once. 
    # Preferably max 4 strips per rack, but max 6 is possible.

#### Dilution ratio
dilution_ratio = 10
  ## For almost all primers dilution_ratio = 10, but for R22mod it is 5

#### Dilution volume  
final_volume = 20
  ## Advised: a minimum of 20µL and a maximum of 60µL
# =============================================================================
 
# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
#### Simulation or robot run
simulate = True

#### Import opentrons protocol API v2
from opentrons import protocol_api
                                      
#### Import protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
                        
#### Import other modules
import math # to do some calculations (rounding up)
# =============================================================================

# CALCULATED VARIABLES=========================================================
# In this region, calculations are made for later use in the protocol.
# =============================================================================
stock_volume = final_volume / dilution_ratio
reagent_volume = final_volume - stock_volume
total_reagent_volume = reagent_volume * number_to_dilute
reagent_tube_type, number_of_reagent_tubes, max_volume = LW.which_tube_type(
    total_reagent_volume, False)

number_stock_racks = math.ceil(number_to_dilute / (len(stock_strip_columns)*8))
number_dilution_racks = math.ceil(number_to_dilute / (len(dilution_strip_columns)*8))
  ## How many strip_racks are needed (1,2,3 or 4) for primer stocks. The same
  ## amount is needed for primer dilutions
# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {
    'protocolName': 'diluting_barcoded_primer_sets.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('A protocol for the dilution of many primers.'),
    'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    # If water_volume >= 19µL use pp20 and p300, otherwise use p20 only
    if reagent_volume >= 19: # p300 only needed when water_volume => 19
        amount_tips_20 = 2
        tips_20 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'tipone_20uL',
                                  amount = amount_tips_20,
                                  deck_positions = [7,4],
                                  protocol = protocol)
        
        amount_tips_300 = 1
        tips_300 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'opentrons_200uL',
                                  amount = amount_tips_300,
                                  deck_positions = [10],
                                  protocol = protocol)
        
    else:
        amount_tips_20 = 3
        tips_20 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'tipone_20uL',
                                  amount = amount_tips_20,
                                  deck_positions = [10,7,4],
                                  protocol = protocol)  

    #### Pipettes
    P20 = True
    if reagent_volume >= 19:
        P300 = True
    else:
        P300 = False
        tips_300 = False
    p20, p300 = LW.loading_pipettes(P20, 
                                    tips_20,
                                    starting_tip_p20,
                                    P300, 
                                    tips_300,
                                    starting_tip_p300,
                                    protocol)
    
    
    #### Labware
    ### Reagent tubes
    ## Loading labware
    reagent_racks = LW.loading_tube_racks(simulate = simulate,
                                          tube_type = reagent_tube_type,
                                          reagent_type = 'dilution_reagent',
                                          amount = 1,
                                          deck_positions = [11],
                                          protocol = protocol)
    ## Specific location of tubes
    reagent = LW.tube_locations(source_racks = reagent_racks,
                                specific_columns = False,
                                skip_wells = False,
                                number_of_tubes = number_of_reagent_tubes)
    
    ### Stocks
    ## Loading labware
    stock_racks = LW.loading_tube_racks(simulate = simulate,
                                        tube_type = 'PCR_strips',
                                        reagent_type = 'stocks',
                                        amount = number_stock_racks,
                                        deck_positions = [2,5,8],
                                        protocol = protocol)
    ## Specific location of tubes
    stocks = LW.tube_locations(source_racks = stock_racks,
                               specific_columns = stock_strip_columns,
                               skip_wells = False,
                               number_of_tubes = number_to_dilute)
    
    ### Dilutions
    ## Loading labware
    dilution_racks = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = 'PCR_strips',
                                           reagent_type = 'dilutions',
                                           amount = number_dilution_racks,
                                           deck_positions = [3,6,9],
                                           protocol = protocol)
    dilutions = LW.tube_locations(source_racks = dilution_racks,
                                  specific_columns = dilution_strip_columns,
                                  skip_wells = False,
                                  number_of_tubes = number_to_dilute)    

# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.comment(f"I need {number_of_reagent_tubes} of {reagent_tube_type}"
                     f"s completely filled with reagent.") 
# ============================================================================= 
 
## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(True)
## ============================================================================

## PIPETTING===================================================================
## ============================================================================
## Aliquoting water------------------------------------------------------------     
    PM.aliquoting_reagent(reagent_source = reagent,
                          reagent_tube_type = reagent_tube_type,
                          reagent_startvolume = max_volume,
                          aliquot_volume = reagent_volume,
                          destination_wells = dilutions,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'next_tube',
                          pause = False,
                          protocol = protocol)                  
## ----------------------------------------------------------------------------        
## Adding primer stocks--------------------------------------------------------         
    PM.transferring_reagents(source_wells = stocks,
                             destination_wells = dilutions,
                             transfer_volume = stock_volume,
                             airgap = True,
                             mix = True,
                             p20 = p20,
                             p300 = p300,
                             protocol = protocol)
    
## ----------------------------------------------------------------------------    
## ============================================================================
 
## LIGHTS======================================================================
## ============================================================================
    protocol.set_rail_lights(False)
## ============================================================================
