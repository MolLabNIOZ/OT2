"""
Version: V_Aug22

tapestation_reagents.py is a protocol written to add the reagents of any
TapeStation assay from a 1.5mL tube to a 96-wells plate and add the samples
from 1.5mL tubes, PCR strips or a 96-wells plate to the reagents. It is also
possible to do one of the 2.
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# If applicable: What is the starting position of the first 20µL tip?
starting_tip_p20 = 'A1'
# If applicable: What is the starting position of the first 200µL tip?
starting_tip_p200 = 'A1'
  ## If volume-wise p20 or p200 is not applicable, this variable won't be used

# How many primers do you want to dilute? 
number_of_samples = 30
  ## The maximum number of samples is 96, as the TapeStation can only measure
  ## one plate at the time anyway.

# Which Tapestation kit are you using?
tapestation_kit = 'D1000'  
  ## Options are:
  ##    'D1000'
  ##    'D5000'  
  ##    'HS-D1000'
  ##    'HS-D5000'
  ##    'gDNA'
  ##    'RNA'
  ##    'HS-RNA'

# What labware are your samples in?
sample_tube_type = 'PCR_strip'
  ## Samples in strips = 'PCR_strip'                                       
  ## Samples in plate = 'plate_96'  
  ## Samples in 1.5mL tubes = 'tube_1.5mL'             
sample_columns = ['2', '7','11']
  ## optional:
  ##    3 strips per rack: ['2', '7', '11'] 
  ##    4 strips per rack: ['2', '5', '8','11']
  ##    6 strips per rack: ['1', '3', '5', '7', '9', '11']
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
                                      
##### Import volume_tracking module 
# volume tracking module is imported inside the def
                                          
# Import other modules
import math
  ## math to do some calculations (rounding up)  
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
# Setting buffer and sample volume - dependent on the chosen tapestation kit
if tapestation_kit == 'D1000':
    buffer_vol = 3
    sample_vol = 1  
if tapestation_kit == 'D5000' or 'gDNA':
    buffer_vol = 10
    sample_vol = 1  
if tapestation_kit == 'HS-D1000' or 'HS-D5000':
    buffer_vol = 2
    sample_vol = 2
if tapestation_kit == 'RNA':
    buffer_vol = 5
    sample_vol = 1  
if tapestation_kit == 'HS-RNA':
    buffer_vol = 1
    sample_vol = 2  
 
# How many sample racks are needed?   
if sample_tube_type == 'PCR_strips':
    sample_racks = math.ceil(number_of_samples / 48)
elif sample_tube_type == 'tube_1.5mL':
    sample_racks = math.ceil(number_of_primers / 24)
elif sample_tube_type == 'plate_96':
    sample_racks = math.ceil(number_of_primers / 96)
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'tapestation_reagents.py',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('A protocol for the 10x dilution of many primers.'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Dilute primers 10x - a protocol for the dilution of many primers
    """
    # IMPORT for simulator
    if not protocol.is_simulating(): 
        from data.user_storage.mollab_modules import volume_tracking_v1 as vt
    else:
        import json
        from mollab_modules import volume_tracking_v1 as vt
# =============================================================================