# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 09:53:34 2024
@author: rdebeer
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'

# What is the starting position of the 200µL tips?
starting_tip_p300 = 'A1'

# After how many times you want to change the tip of the mastermix pipette? 
tip_change = 16 #after times
    # After this amount of pipetting the mastermix, it will get a new tip

# How many samples do you want to include?
number_of_samples = 95
    ## NOTE: include in this number the mock too!!!                

# How many NTCs to include 
number_of_NTCs = 1
 ## NOTE: The NTC should ALWAYS be at the end of your plate!!

# What is the total volume (µL) of your mix?
total_mastermix_volume = 2100        
  ## The total_mastermix_volume is the volume (µL) of mix that is in the source        
  ## labware at the start of the protocol.

# What is the volume (µL) of mastermix that needs to be dispensed?
mastermix_volume = 10

# Where is the mastermix tube located in the rack? 
mastermix_source = 'A1'
  ## convenient places:
  ## if mastermix_tube_type ==   'tube_1.5mL'  -->  D1 
  ## if mastermix_tube_type ==   'tube_5mL'    -->  C1 

# What labware are your primers in?
primer_tube_type = 'PCR_strips'
  ## Primers in strips = 'PCR_strips'                                       
  ## Primers in plate = 'plate_96'
if primer_tube_type == 'PCR_strips':
  # In which columns are the strips in the plate (ignore if not using strips)?
    primer_loc = ['1', '3', '5', '7', '9', '11']
      ## max 2 racks with strips!
       
# What is the volume (µL) of primer that needs to be added to the mix?
primer_vol = 1.5           
   
# How many primers should WALL-E skip?
first_F_primer = 0
first_R_primer = 0         
# record this in the name of the protocol so that user knows which reverse 
# primer is added to his PCR

# Do you want the robot to pause after aliquoting mastermix?
pause = True
  ## Pauses the robot, so you can put in your samples

# Which specific wells (index) do you want to skip? Leave empty if you do not want to skip
skipped_samples = []

# Do you want the light on or off
lights_on = True
  ## If lights_on = True --> lights will be on.                                                        
  ## If lights_on = False --> lights will be off.
# =============================================================================
# IMPORTANT: this is only to be changed by the lab team

# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol  
# =============================================================================

# IMPORT STATEMENTS============================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
#### Import math 
import math
  ## To do some calculations  
                                      
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
# Calculates the total number of reactions
total_number_of_samples = number_of_samples + number_of_NTCs
    # Adds up the number of samples + the number of NTCs

total_number_of_reactions = total_number_of_samples

# Calculates total number of primer racks
# This is for forward and reverse
if primer_tube_type == '1.5mL_tubes':
    primer_per_rack = 24
if primer_tube_type == 'skirted_plate_96':
    primer_per_rack = 96
if primer_tube_type == 'PCR_strips':
    primer_per_rack = 8 * len(primer_loc)
number_of_primer_racks = math.ceil(total_number_of_samples / primer_per_rack)
  ## How many tube_strip_racks are needed (1 or 2)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'general_PCR_protocol_for_WALL-E',
    'author': 'MB <maartje.brouwer@nioz.nl>, RDB <rob.de.beer@nioz.nl>',
    'description': ('qPCR - aliquoting mix and samples'),
    'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix;
    Adding primers from different labware.
    """
# =============================================================================

# CHECKING SAMPLES AMOUNT======================================================
# =============================================================================    
    total_reactions = number_of_samples + number_of_NTCs
    if total_reactions > 96:
        raise Exception(f'You have {total_reactions} reactions. ' +
                        'This is more than 96 reactions and not possible.')
# =============================================================================
    ## LIGHTS----------------------------------------------------------------------
    if not lights_on:
        protocol.set_rail_lights(False)
    if lights_on:
        protocol.set_rail_lights(True)
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### Pipette tips
    # If water_volume >= 19µL use pp20 and p300, otherwise use p20 only
    if mastermix_volume>= 19: # p300 only needed when water_volume => 19
        amount_tips_20 = 3
        tips_20 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'tipone_20uL',
                                  amount = amount_tips_20,
                                  deck_positions = [7,11,10],
                                  protocol = protocol)
        
        amount_tips_300 = 1
        tips_300 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'opentrons_200uL',
                                  amount = amount_tips_300,
                                  deck_positions = [8],
                                  protocol = protocol)
        
    else:
        amount_tips_20 = 4
        tips_20 = LW.loading_tips(simulate = simulate,
                                  tip_type = 'tipone_20uL',
                                  amount = amount_tips_20,
                                  deck_positions = [8,7,11,10],
                                  protocol = protocol)
        tips_300 = False
        
      ### Loading pipettes
    P20 = True
    if mastermix_volume >= 19:
        P300 = True
    else:
        P300 = False
    p20, p300 = LW.loading_pipettes(P20,
                                    tips_20,
                                    starting_tip_p20,
                                    P300, 
                                    tips_300,
                                    starting_tip_p300,
                                    protocol)
        
    ## ========================================================================
    
    ### Loading labware -------------------------------------------------------
    ### MASTERMIX
    # Deciding what tube type you need for the mastermix
    reagent_tube_type, number_of_tubes, max_volume = LW.which_tube_type(
                                        total_volume = total_mastermix_volume,
                                        tube_type = False)
    
    # Loading mastermix tube
    mastermix_racks = LW.loading_tube_racks(simulate = simulate,
                                          tube_type = reagent_tube_type,
                                          reagent_type = 'Mastermix',
                                          amount = 1,
                                          deck_positions = [9],
                                          protocol = protocol)
    
    ## Specific location of mastermix
    mastermix_tube = LW.tube_locations(source_racks = mastermix_racks,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = 1)
    
    ### PRIMERS
    # Loading forward primers
    forward_racks = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = primer_tube_type,
                                         reagent_type = 'forward_primers',
                                         amount = number_of_primer_racks,
                                         deck_positions = [1,4],
                                         protocol = protocol)
    
    # Specific location of the forward primers
    forward_tubes = LW.tube_locations(source_racks = forward_racks,
                                     specific_columns = primer_loc,
                                     skip_wells = skipped_samples,
                                     number_of_tubes = total_number_of_samples)
    
    # Loading reverse primers
    reverse_racks = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = primer_tube_type,
                                         reagent_type = 'reverse_primers',
                                         amount = number_of_primer_racks,
                                         deck_positions = [3,6],
                                         protocol = protocol)
    
    # Specific location of the forward primers
    reverse_tubes = LW.tube_locations(source_racks = reverse_racks,
                                     specific_columns = primer_loc,
                                     skip_wells = skipped_samples,
                                     number_of_tubes = total_number_of_samples)
    
    # Loading PCR-plate
    PCR_plate = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = 'plate_96_NIOZholder',
                                           reagent_type = 'PCR-plate',
                                           amount = 1,
                                           deck_positions = [5],
                                           protocol = protocol)
    
    #### Where to pipette what?
    # Mastermix destinations
    mastermix_destinations = LW.tube_locations(source_racks = PCR_plate,
                                               specific_columns = False,
                                               skip_wells = False,
                                               number_of_tubes = total_number_of_samples)
    # Primer destinations
    primer_destinations = LW.tube_locations(source_racks = PCR_plate,
                                               specific_columns = False,
                                               skip_wells = False,
                                               number_of_tubes = total_number_of_samples)
    
    # Indicate the index of the first and last well in the plate
    first_primer_on_plate = 0
    last_primer_on_plate = 96
    
    #### Forward primer
    # Creating a list from the first reverse primer to the end of the plate
    slice_from_starting_F_to_end_plate = slice(first_F_primer, 
                                               last_primer_on_plate)
    from_starting_F_primer_to_end = forward_tubes[slice_from_starting_F_to_end_plate]
    
    # Creating a list from the last reverse primer on the plate till the last
    # primer
    slice_from_end_to_starting_F_primer = slice(first_primer_on_plate,
                                                first_F_primer)
    from_start_to_starting_F_primer = forward_tubes[slice_from_end_to_starting_F_primer]
    
    # Adding both reverse lists to each other to one list
    F_primers = from_starting_F_primer_to_end + from_start_to_starting_F_primer
    
    # creating the list with the amount of primers
    F_primer_wells = F_primers[:total_number_of_reactions]
    
    #### Reverse primer    
    # Creating a list from the first reverse primer to the end of the plate
    slice_from_starting_R_to_end_plate = slice(first_R_primer, 
                                               last_primer_on_plate)
    from_starting_R_primer_to_end = reverse_tubes[slice_from_starting_R_to_end_plate]
    
    # Creating a list from the last reverse primer on the plate till the last
    # primer
    slice_from_end_to_starting_R_primer = slice(first_primer_on_plate,
                                                first_R_primer)
    from_start_to_starting_R_primer = reverse_tubes[slice_from_end_to_starting_R_primer]
    
    # Adding both reverse lists to each other to one list
    R_primers = from_starting_R_primer_to_end + from_start_to_starting_R_primer
    
    # creating the list with the amount of primers
    R_primer_wells = R_primers[:total_number_of_reactions]
    
    ## ========================================================================

    ## PIPETTING===============================================================
    ## ========================================================================
    # Pipetting mastermix -----------------------------------------------------
    PM.aliquoting_reagent(reagent_source = mastermix_tube,
                          reagent_tube_type = reagent_tube_type,
                          reagent_startvolume = total_mastermix_volume,
                          aliquot_volume = mastermix_volume,
                          destination_wells = mastermix_destinations,
                          p20 = p20,
                          p300 = p300,
                          tip_change = tip_change,
                          action_at_bottom = 'raise_error',
                          pause = pause,
                          protocol = protocol)  
    
    # # Transfering forward primer
    PM.transferring_reagents(source_wells = F_primer_wells,
                              destination_wells = primer_destinations,
                              transfer_volume = primer_vol ,
                              airgap = True,
                              mix = True,
                              p20 = p20,
                              p300 = p300,
                              protocol = protocol)

    # # Transfering reverse primer
    PM.transferring_reagents(source_wells = R_primer_wells,
                              destination_wells = primer_destinations,
                              transfer_volume = primer_vol ,
                              airgap = True,
                              mix = True,
                              p20 = p20,
                              p300 = p300,
                              protocol = protocol)

    ## ========================================================================
# LIGHTS-----------------------------------------------------------------------
    if lights_on:
        protocol.set_rail_lights(False)
# -----------------------------------------------------------------------------