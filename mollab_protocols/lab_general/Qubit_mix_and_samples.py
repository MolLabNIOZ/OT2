"""
VERSION: V_May22
Qubit_mix_and_samples.py is a protocol written for adding the Qubit mix

Het idee is veranderd
Nu: willen we gewoon 1 plaat vol pipetteren  en eventueel dan nog 1 plaat + nog 
een paar samples --> in eerste in stantie gewoon max 88 samples
"""

#%% VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# What is the starting position of the 200µL tips?
starting_tip_p300 = 'A1'
    ## If not applicable, you do not have to change anything
    
# Are you running 1 or 2 assays at the same time?
    ## 1 = HS or BR ---- 2 = HS and BR
    ## The first assay always starts from the left of the plate, the second 
    ## assay always starts from the right of the plate!
number_of_assays = 1

# How many samples do you want to include?
## For now: max. = 88 samples
number_of_samples = 10

# Which tube are you using for your Qubit mix? (options 1.5mL or 5mL)
  ## For volume < 1300: 'tube_1.5mL'                                        
  ## For volume > 1300: 'tube_5mL'  
Qmix_tube_type = 'tube_5mL'


# What labware are your samples in?
sample_tube_type = 'PCR_strip'  
  ## If your samples are in strips copy/paste 'PCR_strip'                                       
  ## If your samples are in a plate copy/paste 'plate_96'  
  ## If your samples are in 1.5 ml eppendorfs copy/paste 'tube_1.5mL'  
  
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

#%% IMPORT STATEMENTS============================================================
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
  
#%% CALCULATED AND SET VARIABLES=================================================
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

# In which well is your mix tube? 
Qmix_source = 'A1'

# Dispension volume of the mix for the standards
dispension_vol_std = 48

# Dispension volume of the mix for the samples
dispension_vol_sample = 49

# Volume of the standard to add
std_vol = 2

# Volume of the sample to add
sample_vol = 1

start_vol = (number_of_samples*dispension_vol_sample) + (8*dispension_vol_std)

if sample_tube_type == 'tube_1.5mL':
    samples_per_rack = 24
if sample_tube_type == 'plate_96':
    samples_per_rack = 96
if sample_tube_type == 'PCR_strip':
    samples_per_rack = 8 * len(sample_columns)
sample_racks = math.ceil(number_of_samples / samples_per_rack)
  ## How many tube_strip_racks are needed (1,2 or 3)
# =============================================================================


#%% METADATA=====================================================================
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
        10,
        '200tips')
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',
        8,
        '20tips_1')
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',
        11,
        '20tips_2')
    tips_20 = [tips_20_1, tips_20_2]
    
    # Tube racks & plates
    if Qmix_tube_type == 'tube_1.5mL':
        Qmix_tube = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        1,
        'Qubit_mix_tube')

    if sample_tube_type == 'tube_1.5mL':
        sample_source_1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            2,
            'sample_source_1')
        sample_source_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            3,
            'sample_source_2')
        sample_source_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            5,
            'sample_source_3')
        sample_source_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            6,
            'sample_source_4')
    
    if sample_tube_type == 'plate_96':
        sample_source_1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            2,                                  
            'sample_source_1')

    if simulate: #Simulator
        with open("labware/biorad_qpcr_plate_nioz_plateholder/"
                  "biorad_qpcr_plate_nioz_plateholder.json") as labware_file:
            labware_def_niozplate = json.load(labware_file)
        destination_plate = protocol.load_labware_from_definition(
            labware_def_niozplate,
            7,
            '96well_plate')
        if Qmix_tube_type == 'tube_5mL':
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                 "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                      labware_def_5mL = json.load(labware_file)
            Qmix_tube = protocol.load_labware_from_definition( 
                labware_def_5mL,           
                1,                         
                'Qubit_mix_tube')
        if sample_tube_type == 'PCR_strip':
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            sample_source_1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                2,                         
                'sample_source_1')         
            sample_source_2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips, 
                3,                     
                'sample_source_2')    
            sample_source_3 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,
                5,                   
                'sample_source_3')    
            sample_source_4 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,
                6,                   
                'sample_source_4')     
    else: 
        destination_plate = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',
            7,
            '96well_plate')
        if Qmix_tube_type == 'tube_5mL':
            Qmix_tube = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                1,                                     
                'Qubit_mix_tube') 
        if sample_tube_type == 'PCR_strips':
            sample_source_1 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                2,                                     
                'sample_source_1')                      
            sample_source_2 = protocol.load_labware_( 
                'pcrstrips_96_wellplate_200ul',    
                3,                                 
                'sample_source_2')                 
            sample_source_3 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',    
                5,                                
                'sample_source_3') 
            sample_source_4 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',    
                6,                                
                'sample_source_4') 
   
    # Pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',             
        'right',                        
        tip_racks=[tips_200])           
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  
        'left',                             
        tip_racks=tips_20)
# =============================================================================

# PREDIFINED VARIABLES=========================================================
# =============================================================================
    aspiration_vol_std = (dispension_vol_std + (dispension_vol_std/100*2))
    aspiraton_vol_sample = (
        dispension_vol_sample + (dispension_vol_sample/100*2))
      ## The aspiration_vol is the volume (µL) that is aspirated from the   
      ## container.                                                         
    
    ##### Variables for volume tracking
    start_height = vt.cal_start_height(Qmix_tube, start_vol)
      ## Call start height calculation function from volume tracking module.
    current_height = start_height
      ## Set the current height to start height at the beginning of the     
      ## protocol.      

    std_mix_vol = std_vol + 3
    sample_mix_vol = sample_vol + 3
      ## mix_vol = volume for pipetting up and down                  
# =============================================================================                   

# SETTING LOCATIONS============================================================
# =============================================================================
    # Setting starting tip
    p300.starting_tip = tips_200.well(starting_tip_p300)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
    
    # Qubit mix location
    QubitMix = Qmix_tube[Qmix_source]
    
    # Make a list of all possible wells in the destination plate
    destination_wells = []
    for well in destination_plate.wells():
        destination_wells.append(well)
    # Create a list of wells where the standards should go.
    
    