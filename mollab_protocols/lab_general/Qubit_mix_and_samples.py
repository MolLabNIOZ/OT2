"""
VERSION: V_May22
Qubit_mix_and_samples.py is a protocol written for adding the Qubit mix

Het Idee:
Aliquot mix vanuit 5 ml buis naar plaat
altijd een standaard links van de plaat, 8 welletjes, 48 uL + 2 uL
optie voor 2 assays, 1 standaard links, 1 standaard rechts, max helft samples
2 rekjes als er 2 assays zijn

Start volume laten uitrekenen en dan een comment in het protocol zetten dat ze 
een buis met zoveel startvolume moeten neerzetten (+ 10% extra)

licht moet UIT voor het protocol begint

1.5 mL tubes met standaard (50uL aliquots maken, dan kan het zonder vol track)
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# What is the starting position of the 200µL tips?
starting_tip_p200 = 'A1'
    ## If not applicable, you do not have to change anything
    
# Are you running 1 or 2 assays at the same time?
    ## 1 = HS or BR ---- 2 = HS and BR
    ## The first assay always starts from the left of the plate, the second 
    ## assay always starts from the right of the plate!
number_of_assays = 1

# How many samples do you want to include?
number_of_samples = 10
# What is the starting volume 

# Which tube are you using for your Qubit mix? (options 1.5mL or 5mL)
  ## For volume < 1300: 'tube_1.5mL'                                        
  ## For volume > 1300: 'tube_5mL'  
  ## If you are doing 2 assays in one plate, it might be that they are not
  ## in the same type of tube
if number_of_assays == 1:
    Qmix_tube_type_left = 'tube_5mL'
if number_of_assays == 2: 
    Qmix_tube_type_1_left = 'tube_5mL'
    Qmix_tube_tupe_2_right = 'tube_1.5mL'

mastermix_source = 'C1'
  ## convenient places:
  ## if mastermix_tube_type ==   'tube_1.5mL'  -->  D1 
  ## if mastermix_tube_type ==   'tube_5mL'    -->  C1

# What labware are your samples in?
sample_tube_type = 'PCR_strip'  
  ## Samples in strips = 'PCR_strip'                                       
  ## Samples in plate = 'plate_96'  
  ## Samples in 1.5mL tubes = 'tube_1.5mL'  
  
# In which columns are the strips in the plate (ignore if not using strips)?
sample_columns = ['2', '7','11']
  ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
  ## max 4 racks with strips!  

# What is the location of your first sample (fill in if you have a plate)?                                    
first_sample = 'A2'
  ## 'A1' is standard for tubes and plates. 
  ## 'A2' is standard for tube_strips
  ## But if you have more samples in the plate than
  ## fit in a plate, change the first well position.

# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.

import pandas as pd
  ## Import pandas to open the dataframe with the labware offsets.

import math
  ## Import math for some calculations.

if simulate: #Simulator
    from mollab_modules import volume_tracking_v1 as vt
    import json
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware. 
else: #Robot
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
  
# CALCULATED AND SET VARIABLES=================================================
# =============================================================================
# Setting callibration data per labware for both robot and simulator
if simulate: #Simulator
    offsets = pd.read_csv("mollab_protocols/labware_offsets_for_simulate.csv",
                          sep=';')
    offsets = offsets.set_index('labware')
else: #Robot
    offsets = pd.read_csv(
        "data/user_storage/mollab_modules/labware_offset.csv", sep=';')
    offsets = offsets.set_index('labware')
    
# Dispension volume of the mix for the standards
dispension_vol_std = 48

# Dispension volume of the mix for the samples
dispension_vol_sample = 49

# Volume of the standard to add
std_vol = 2

# Volume of the sample to add
sample_vol = 1

if sample_tube_type == 'tube_1.5mL':
    samples_per_rack = 24
if sample_tube_type == 'plate_96':
    samples_per_rack = 96
if sample_tube_type == 'PCR_strip':
    samples_per_rack = 8 * len(sample_columns)
sample_racks = math.ceil(number_of_samples / samples_per_rack)
  ## How many tube_strip_racks are needed (1,2 or 3)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'Qubit - mix and samples',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>, MB <maartje.brouwer@nioz.nl>',
    'description': ('Aliquoting Qubit mix and adding samples/standards'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting Qubit mix (48µL for standards, 49µL for samples);
    Adding standards from 1.5mL tubes (2µL)
    Adding samples from different labware (1µL)
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES ================================================
# =============================================================================

    # Pipette tips
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',
        1,
        '200tips')
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',
        4,
        '20tips_1')
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',
        7,
        '20tips_2')
    
    # Tube racks & plates
    destination_plate = protocol.load_labware(
        'biorad_qpcr_plate_nioz_plateholder',
        3,
        '96well_plate')
    
    if mastermix_tube_type == 'tube_1.5mL':
        mastermix_tube = 


