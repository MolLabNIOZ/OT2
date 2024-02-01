# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:25:25 2024
@author: rdebeer
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'

# What is the starting position of the 200µL tips?
starting_tip_p300 = 'A1'

# How many samples do you want to include?
number_of_samples = 65
  ## MAX ==  number of samples -                                 
  ##         (number of std series * length of std series) -     
  ##         number of standard sample replicates

# How many NTCs to include 
number_of_NTCs = 1 
  ## NOTE: The NTC come after samples and std_samples                     

# What is the total volume (µL) of your mix?
mastermix_volume = 1800
  ## The start_vol_m is the volume (µL) of mix that is in the source        
  ## labware at the start of the protocol.

# After how many times you want to change the tip of the mastermix? 
tip_change = 16 #times
    # After this amount of pipetting the mastermix, it will get a new tip

# Do you want the robot to pause after aliquoting mastermix?
pause = True
  ## Pauses the robot, so you can put in your samples

# Which specific wells do you want to skip? Leave empty if you do not want to skip
skipped_samples = []
  
# Are you doing a qPCR or a regular PCR?
qPCR = True
  ## True or False                                                          
  ## Lights off if qPCR, standard sample and/or standard dilution series 
if qPCR:  
    # How many dilution serie replicates do you want to include?
    number_of_std_series = 3 
      ## If none -- fill in 0
    # How many dilutions are in the standard dilution series?
    length_std_series = 8
      ## length_of_std_series  MAX == 8                                     
    # How many replicates of the standard sample are you taking?
    number_of_std_samples = 6
else:
    ## If we are not doing a qPCR - protocol uses these values.             
    number_of_std_series = 0  
    length_std_series = 0
    number_of_std_samples = 0
 
mastermix_source = 'A1'
  ## convenient places:
  ## if mastermix_tube_type ==   '1.5mL_tubes'  -->  D1 
  ## if mastermix_tube_type ==   '5mL_tubes'    -->  C1 

# What is the volume (µL) of mastermix that needs to be dispensed?
reagent_volume = 22     

# What labware are your samples in?
sample_tube_type = '1.5mL_tubes'
  ## Samples in strips = 'PCR_strips'                                       
  ## Primers in plate = 'skirted_plate_96'  
  ## Samples in 1.5mL tubes = '1.5mL_tubes'                                         
if sample_tube_type == 'PCR_strips':
    
# In which columns are the strips in the plate (ignore if not using strips)?
    sample_columns = ['2', '7','11']

else:
    sample_columns = False
  ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
  ## max 4 racks with strips!  
# What is the volume (µL) of sample that needs to be added to the mix?
sample_volume = 2
  ## MAX = 17µL
# What is the location of your first sample (fill in if you have a plate)?                                    
first_sample = 'A1'
  ## 'A1' is standard for tubes and plates. 
  ## 'A2' is standard for tube_strips
  ## But if you have more samples in the plate than
  ## fit in the qPCR, change the first well position.
  
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
                                      
#### Import mollab protocol module
from data.user_storage.mollab_modules import Pipetting_Modules as PM
from data.user_storage.mollab_modules import LabWare as LW

# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================                   
if number_of_std_samples >= 1:
    total_number_of_samples = number_of_samples + 1
      ## If a standard sample is taken, add 1 to the total number of samples
else:
    total_number_of_samples = number_of_samples

if sample_tube_type == '1.5mL_tubes':
    samples_per_rack = 24
if sample_tube_type == 'skirted_plate_96':
    samples_per_rack = 96
if sample_tube_type == 'PCR_strips':
    samples_per_rack = 8 * len(sample_columns)
number_of_sample_racks = math.ceil(total_number_of_samples / samples_per_rack)
  ## How many tube_strip_racks are needed (1,2 or 3)

# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'general_qPCR_protocol',
    'author': 'MB <maartje.brouwer@nioz.nl>, RDB <rob.de.beer@nioz.nl>',
    'description': ('qPCR - aliquoting mix and samples'),
    'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix;
    Adding samples from different labware.
    """
# =============================================================================

# CHECKING SAMPLES AMOUNT======================================================
# =============================================================================    
    total_reactions = number_of_samples + number_of_std_samples + number_of_NTCs + (number_of_std_series*8)
    if total_reactions > 96:
        raise Exception(f'You have {total_reactions} reactions. ' +
                        'This is more than 96 reactions and not possible.')

# =============================================================================
## LIGHTS----------------------------------------------------------------------
    if qPCR:
        protocol.set_rail_lights(False)
    if not qPCR:
        protocol.set_rail_lights(True)
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
    
    #### Loading labware
    ### MASTERMIX
    # Deciding what tube type you need for the mastermix
    reagent_tube_type, number_of_tubes, max_volume = LW.which_tube_type(total_volume = mastermix_volume,
                                           tube_type = False)
    
    # Loading mastermix tube
    mastermix_racks = LW.loading_tube_racks(simulate = simulate,
                                          tube_type = reagent_tube_type,
                                          reagent_type = 'Mastermix',
                                          amount = 1,
                                          deck_positions = [1],
                                          protocol = protocol)
    
    ## Specific location of mastermix
    mastermix_tube = LW.tube_locations(source_racks = mastermix_racks,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = 1)
    
    ### SAMPLES   
    # Loading sample plates
    sample_racks = LW.loading_tube_racks(simulate = simulate,
                                         tube_type = sample_tube_type,
                                         reagent_type = 'sample_rack',
                                         amount = number_of_sample_racks,
                                         deck_positions = [2,5,8,11],
                                         protocol = protocol)
    
    # Specific location of samples
    sample_tubes = LW.tube_locations(source_racks = sample_racks,
                                     specific_columns = sample_columns,
                                     skip_wells = skipped_samples,
                                     number_of_tubes = number_of_samples +1)
    
    # Defining what the standard sample tube is
    standard_sample_tube = []
    for i in range(number_of_std_samples):
        standard_sample_tube.append(sample_tubes[-1])
    
    # Loading PCR-plate
    qPCR_plate = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = 'plate_96_NIOZholder',
                                           reagent_type = 'qPCR-plate',
                                           amount = 1,
                                           deck_positions = [3],
                                           protocol = protocol)
  
    #### Where to pipette what?
    # Sample destinations
    sample_destinations = LW.tube_locations(source_racks = qPCR_plate,
                                            specific_columns = False,
                                            skip_wells = False,
                                            number_of_tubes = number_of_samples + number_of_NTCs + number_of_std_samples)
   
    # Standard sample destinations
    standard_sample_destination = sample_destinations[number_of_samples + number_of_NTCs:]
    
    # standard dilution serie destination
    ## Defines the columns you need
    std_dilution_destinations = []
    specific_qPCR_columns = ['12','11','10','9','8','7','6','5','4','3','2','1']
    for i in range(number_of_std_series):
        column = []
        column.append(specific_qPCR_columns[i])
        destination = LW.tube_locations(source_racks = qPCR_plate,
                                 specific_columns = column,
                                 skip_wells = False,
                                 number_of_tubes = length_std_series)
        std_dilution_destinations = std_dilution_destinations + destination
    
    # Mastermix destinations
    mastermix_destinations = sample_destinations + std_dilution_destinations

   
    ## ========================================================================
    ### Loading pipettes
    p20, p300 = LW.loading_pipettes(P20 = True, 
                                    tips_20 = tips_20,
                                    starting_tip_p20 = starting_tip_p20,
                                    P300 = True, 
                                    tips_300 = tips_300,
                                    starting_tip_p300 = starting_tip_p300,
                                    protocol = protocol)
    
    ## ========================================================================

    ## PIPETTING===============================================================
    ## ========================================================================
    # Pipetting mastermix ----------------------------------------------------
    PM.aliquoting_reagent(reagent_source = mastermix_tube,
                          reagent_tube_type = reagent_tube_type,
                          reagent_startvolume = max_volume,
                          aliquot_volume = reagent_volume,
                          destination_wells = mastermix_destinations,
                          p20 = p20,
                          p300 = p300,
                          tip_change = tip_change,
                          action_at_bottom = 'continue_at_bottom',
                          pause = pause,
                          protocol = protocol)  
    
    # Defines the columns you need for samples
    
    # transfering samples
    PM.transferring_reagents(source_wells = sample_tubes[:-1],
                              destination_wells = sample_destinations,
                              transfer_volume = sample_volume,
                              airgap = True,
                              mix = True,
                              p20 = p20,
                              p300 = p300,
                              protocol = protocol)
    
    # Transfering standard samples
    PM.transferring_reagents(source_wells = standard_sample_tube,
                          destination_wells = standard_sample_destination,
                          transfer_volume = sample_volume,
                          airgap = True,
                          mix = True,
                          p20 = p20,
                          p300 = p300,
                          protocol = protocol)
    ## ========================================================================
# LIGHTS-----------------------------------------------------------------------
    if not qPCR:
        protocol.set_rail_lights(False)
# -----------------------------------------------------------------------------        