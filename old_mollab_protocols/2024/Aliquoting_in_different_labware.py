# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 12:49:49 2024

@author: rdebeer
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL or 300 µL tips?
starting_tip = 'A1'

# How many times you want to aliquote?
number_of_aliquotes = 163

# After how many times you want to change the tip? 
tip_change = 16 #after times
    # After this amount of pipetting the reagent, it will get a new tip

# Are you doing a qPCR or a regular PCR?
lights_on = True
  ## True or False                                                          
  ## Lights off if qPCR, standard sample and/or standard dilution series

stock_source = 'A1'
  ## if mastermix_tube_type ==   '1.5mL_tubes'  -->  D1 
  ## if mastermix_tube_type ==   '5mL_tubes'    -->  C1 

# What is the volume (µL) of reagent that needs to be dispensed?
reagent_volume = 8

# What labware are your samples in?
final_tube_type = 'PCR_strips'
  ## Samples in strips = 'PCR_strips'                                       
  ## Primers in plate = 'skirted_plate_96'  
  ## Samples in 1.5mL tubes = '1.5mL_tubes'                                         
if final_tube_type == 'PCR_strips':
# In which columns are the strips in the plate (ignore if not using strips)?
    sample_columns = ['1', '3', '5','7','9','11']

else:
    sample_columns = False
  ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
  ## max 4 racks with strips!  
# What is the volume (µL) of sample that needs to be added to the mix?

# =============================================================================  

# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
#### Simulation or robot run
simulate = True

#### Import opentrons protocol API v2
from opentrons import protocol_api
#### Import math 
import math
    ## To do some calculations  
                                      
# #### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW

# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================      
# Defines total number of samples.
total_number_of_samples = number_of_aliquotes
# Calculates how many µL of stock you need.
stock_volume = reagent_volume * (number_of_aliquotes*1.10)
# Calculates in which tube your stock needs to be.
stock_tube_type, number_of_tubes, max_volume = LW.which_tube_type(total_volume = stock_volume,
                                                                tube_type = False)

# Defines how many tubes there are in a specific rack and calculates how many
# total racks you need.
if final_tube_type == '1.5mL_tubes':
    samples_per_rack = 24
    max_reactions = samples_per_rack * 8
if final_tube_type == 'skirted_plate_96':
    samples_per_rack = 96
    max_reactions = samples_per_rack * 8
if final_tube_type == 'PCR_strips':
    samples_per_rack = 8 * len(sample_columns)
    max_reactions = samples_per_rack * 8
number_of_sample_racks = math.ceil(total_number_of_samples / samples_per_rack)

if number_of_aliquotes > max_reactions:
    raise Exception ('You have to many reactions!')
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'aliquoting in different labware', 'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix;
    Adding samples from different labware.
    """
# =============================================================================
## LIGHTS----------------------------------------------------------------------
    if not lights_on:
        protocol.set_rail_lights(False)
    if lights_on:
        protocol.set_rail_lights(True)    
    
    protocol.comment("You need {stock_volume} µL of your stock in a {stock_tube_type}.")
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    # If water_volume >= 19µL use pp20 and p300, otherwise use p20 only
    if reagent_volume >= 19:
        amount_tips_300 = 2
        tips_300 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'opentrons_200uL',
                                  amount = amount_tips_300,
                                  deck_positions = [10, 7],
                                  protocol = protocol)
        P300 = True
        P20 = False
        tips_20 = False
    else:
        amount_tips_20 = 2
        tips_20 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'tipone_20uL',
                                  amount = amount_tips_20,
                                  deck_positions = [10, 7],
                                  protocol = protocol)
        P300 = False
        P20 = True
        tips_300 = False
    # Loading stock tube
    stock_racks = LW.loading_tube_racks(simulate = simulate,
                                      tube_type = stock_tube_type,
                                      reagent_type = 'Stock',
                                      amount = 1,
                                      deck_positions = [9],
                                      protocol = protocol)

    ## Specific location of stock
    stock_tube = LW.tube_locations(source_racks = stock_racks,
                                   specific_columns = False,
                                   skip_wells = False,
                                   number_of_tubes = 1)
    
    ### Final tubes
    # Loading final tubes
    final_racks = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = final_tube_type,
                                         reagent_type = 'destination_racks',
                                         amount = number_of_sample_racks,
                                         deck_positions = [11,8,5,6,4,1,2,3],
                                         protocol = protocol)
    
    # Specific location of the final tubes
    final_tubes = LW.tube_locations(source_racks = final_racks,
                                     specific_columns = sample_columns,
                                     skip_wells = False,
                                     number_of_tubes = number_of_aliquotes)
    ### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20,
                                  tips_20,
                                  starting_tip,
                                  P300, 
                                  tips_300,
                                  starting_tip,
                                  protocol)
    
    ## ========================================================================

    ## PIPETTING===============================================================
    ## ========================================================================
    # Pipetting mastermix -----------------------------------------------------
    PM.aliquoting_reagent(reagent_source = stock_tube,
                          reagent_tube_type = stock_tube_type,
                          reagent_startvolume = stock_volume,
                          aliquot_volume = reagent_volume,
                          destination_wells = final_tubes,
                          p20 = p20,
                          p300 = p300,
                          tip_change = tip_change,
                          action_at_bottom = 'continue_at_bottom',
                          pause = False,
                          protocol = protocol) 
    ## ========================================================================
# LIGHTS-----------------------------------------------------------------------
    if lights_on:
        protocol.set_rail_lights(False)
# -----------------------------------------------------------------------------