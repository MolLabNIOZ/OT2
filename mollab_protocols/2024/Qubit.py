# -*- coding: utf-8 -*-
"""
a protocol written for the aliquoting of Qubit mix from a 1.5mL or 5mL tube to 
a PCR plate, standards are added from 1.5mL tubes to the first row of the plate, 
then samples are added from either strips, a plate or 1.5mL tubes.
"""
# VARIABLES TO SET#!!!=========================================================
# This is the only region where you are allowed to change variables
# =============================================================================
#### Starting_tips
starting_tip_p20 = 'D11'
starting_tip_p300 = 'A1'

# How many samples do you want to include?
number_of_samples = 88 ## Max. = 88 samples

# How many standards do you want to include?
number_of_standards = 4 ## Optional: 2, 4 or 8
## If you choose 2 (standard Qubit standards St #1 and St #2) the robot will
## include 4 replicates of each of the standards
## If you choose 4 (Qubit St #1, 2 dilutions of St #2 and St #2) the robot will
## include 2 replicates of each of the standards
## If you choose 8 the robot will include every standard once.

# What labware are your samples in?
sample_tube_type = 'PCR_strips'  
  ## Options: 'PCR_strip', 'skirted_plate_96', non_skirted_plate_96', '1.5mL_tubes'

# In which columns are the strips in the plate (ignore if not using strips)?
if sample_tube_type == 'PCR_strips':
    sample_columns = ['2', '7', '11'] ## Max 4 racks with strips! 
      ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     

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

# CALCULATED AND SET VARIABLES=================================================
# This region contains settings and calculations that are later used
# =============================================================================
# Volume of the standard to add
std_vol = 2
# Volume of the sample to add
sample_vol = 1

# How much mix to dispense for standards
Qmix_vol_standards = 50 - std_vol
# How much mix to dispense for samples
Qmix_vol_sample = 50 - sample_vol

# How much Qmix do you need and what tube should be used?
Qmix_start_volume = (((number_of_samples * 1.1)*Qmix_vol_sample) + 
                         (9 * Qmix_vol_standards))
Qmix_tube_type, number_of_tubes, max_volume = LW.which_tube_type(
    total_volume = Qmix_start_volume,
    tube_type = False)
# =============================================================================

# METADATA=====================================================================
# This region contains some API opentrons stuff
# =============================================================================
metadata = {
    'protocolName': 'Qubit - mix and samples',
    'author': 'MB <maartje.brouwer@nioz.nl>',
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


