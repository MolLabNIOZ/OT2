"""
VERSION: V_June22
equimolar_pooling.py is a protocol for pooling samples in equimolar amounts.
First use get_uL_info to get a list of volumes per sample to add to the pool.
Copy that list into this protocol and run this protocol on the OT2

Samples can be provided in a PCR plate, PCR strips or 1.5mL tubes.

You have to provide:
    List with sample volumes 
        make sure the order is similar to the sample orientation
    Location of the starting tip in P20 or P200
    Type of tubes the samples are in
    
    The protocol will tell you what tube the pool will be made in.
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the tips?
starting_tip_p20 = 'A1'
starting_tip_p200 = 'A1'

DNA_µL_list = ([4.0, 0.26666666666666666, 1.1111111111111112, 
                0.42105263157894735, 8.0, 
                30.769230769230766, 0.4444444444444444, 
                1.0, 4.444444444444445, 13.333333333333334])

# What labware are your samples in?
sample_tube_type = 'plate_96' 
  ##Other options:
# sample_tube_type = 'PCR_strip'                                        
# sample_tube_type = 'tube_1.5mL'  

if sample_tube_type == 'PCR_strips':
    # In which columns are the strips in the plate (ignore if not using strips)?
    sample_columns = ['2', '7','11']
      ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
      ## max 4 racks with strips!  

# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol
# =============================================================================

# IMPORT STATEMENTS AND FILES==================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.
import pandas as pd
  ## For accessing offset .csv file
# =============================================================================

# CALCULATED VARIABLES=========================================================
# ============================================================================= 
total_pool_volume = sum(DNA_µL_list)

if above(total_pool_volume, 19):
    p200 = True
    

# If not simulated, import the .csv from the robot with robot_specific 
# labware off_set values
if not simulate:
    offsets = pd.read_csv(
        "data/user_storage/mollab_modules/labware_offset.csv", sep=';'
        )
      ## import .csv
    offsets = offsets.set_index('labware')
      ## remove index column
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'equimolar_pooling.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('pooling samples in equimolar amounts'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    pool samples together in different volumes
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    labwares = {}
      ## empty dict to add labware and labware_names to, to loop through


    
    
    