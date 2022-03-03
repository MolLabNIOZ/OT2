"""
VERSION: V_March22
This is a protocol designed for Annalisa Delre, who is doing a PCR protocol
for Illumina sequencing that was developed by Douwe Maat in 2019(?). 
A PCR was already done, and now the samples need to be barcoded. The samples
cannot be added to the mix by a robot because we don't have a robot in the 
post-PCR lab. Therefor, we wrote a protocol specific for adding mix and
barcoded primers to PCR strips. Special about this protocol is that we
add 2 different reverse primers, causing the R primer to have a different 
volume than the F primer.

You need to provide:
    starting tips P20/p200
    number of samples (maximum = 23 excl 1 negative control)
    number of NTCs
    start volume of your mastermix
    mastermix tube type (1.5mL or 5mL)
    volume of mastermix to be dispensed
    location of the mastermix tube in the rack
    primer volume F 
    primer volume R

Deck locations:
    200 tips (if dispension volume = >20µL)     2 
    20 tips                                     7, 10
    mastermix tube rack (1.5mL or 5mL)          3
    tube strips - strips in rows 2, 7, 11       6
    F primers                                   11
    Ra primers                                  8
    Rb primers                                  5
    
What the protocol does: 
    Aspirating dispension volume from the mastermix tube 
    Dispensing dispension volume in the PCR strip
    Aspirating F primer volume from F primer rack
    Dispensing F primer volume in PCR strip
    Aspirating R primer volume from Ra primer rack
    Dispensing R primer volume in PCR strip
    Aspirating R primer volume from Rb primer rack
    Dispensing R primer volume in PCR strip
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# If mastermix dispense > 19: What is the starting position of the 200µL tips?
starting_tip_p200 = 'A1'
  ## If not applicable, you do not have to change anything
  
# How many samples do you want to include?
number_of_samples = 2   
  ## Max = 24 INCLUDING NTC            

# How many NTCs to include 
number_of_NTCs = 1 
  ## NOTE: The NTC should ALWAYS be at the end                                         

# What is the total volume (µL) of your mix?
start_vol = 1116
  ## The start_vol is the volume (µL) of mix that is in the source        
  ## labware at the start of the protocol.     

# What is the volume (µL) of mastermix that needs to be dispensed?
dispension_vol = 43   
                                         
# What is the volume (µL) of primer that needs to be added to the mix?
F_primer_vol = 3
R_primer_vol = 1.5                                

# Which tube are you using for your mastermix? (options 1.5mL or 5mL)
mastermix_tube_type = 'tube_1.5mL'
  ## For volume < 1300: 'tube_1.5mL'                                        
  ## For volume > 1300: 'tube_5mL'                                          

# Where is the mastermix tube located in the rack? 
mastermix_source = 'D1'
  ## convenient places:
  ## if mastermix_tube_type ==   'tube_1.5mL'  -->  D1 
  ## if mastermix_tube_type ==   'tube_5mL'    -->  C1 
  
# Do you want to simulate the protocol?
simulate = False
  ## True for simulating protocol, False for robot protocol                 
# =============================================================================

## IMPORT STATEMENTS===========================================================
## ============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      
  
if simulate: #Simulator
    from mollab_modules import volume_tracking_v1 as vt
    import json 
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.     
else: #Robot
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
## ============================================================================

## CALCULATED VARIABLES========================================================
## ============================================================================
number_of_primers = number_of_samples + number_of_NTCs
## ============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'mix_barcoded_primers_2Rprimers',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Illumina PCR - aliquoting mix from 1.5mL or 5mL tube - '
                    'add primers from 1.5mL tube, 2 different R primers'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix from a 1.5mL or 5mL tube.
    Adding barcoded primers - from 1.5mL tubes, 2 different R primers.
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    # Pipette tips
    if dispension_vol >= 19:
      ## When the mm volume to be dispensed >= 19, 200µL tips are          
      ## needed in addition to the 20µL tips.                              
        tips_200 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', 
            2,                                  
            '200tips')                          
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            7,                                  
            '20tips_1')                                
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            10,                                 
            '20tips_2')                         
        tips_20 = [tips_20_1, tips_20_2]
    else:
      ## When the mm volume to be dispensed <=19, only 20µL are needed      
        tips_20_1 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            2,                                  
            '20tips_1')                           
        tips_20_2 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            7,                                  
            '20tips_2')                           
        tips_20_3 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            10,                                 
            '20tips_3')                             
        tips_20 = [tips_20_1, tips_20_2, tips_20_3]
   
    # Tube_racks & plates                                          
    F_primer_source = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',    
        11,                                  
        'F_primer_source')  
    Ra_primer_source = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        8,
        'Ra_primer_source')
    Rb_primer_source = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        5,
        'Rb_primer_source')                         
    
    if mastermix_tube_type == 'tube_1.5mL':
        mastermix_tube = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            3,
            'mastermix_tube')   
               
    if simulate: #Simulator
        with open("labware/pcrstrips_96_wellplate_200ul/"
                  "pcrstrips_96_wellplate_200ul.json") as labware_file:
                labware_def_pcrstrips = json.load(labware_file)
        PCR_strips = protocol.load_labware_from_definition( 
            labware_def_pcrstrips,     
            6,                         
            'PCR_strips')         
        if mastermix_tube_type == 'tube_5mL': 
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                      labware_def_5mL = json.load(labware_file)
            mastermix_tube = protocol.load_labware_from_definition( 
                labware_def_5mL,           
                3,                         
                'mastermix_tube')           
    else: #Robot
        PCR_strips = protocol.load_labware( 
            'pcrstrips_96_wellplate_200ul',        
            6,                                     
            'PCR_strips')            
        if mastermix_tube_type == 'tube_5mL': 
            mastermix_tube = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                3,                                     
                'mastermix_tube')                               
           
    # Pipettes
    if dispension_vol >= 19:
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
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
      ## The aspiration_vol is the volume (µL) that is aspirated from the   
      ## container.                                                         
    ##### Variables for volume tracking
    start_height = vt.cal_start_height(mastermix_tube_type, start_vol)
      ## Call start height calculation function from volume tracking module.
    current_height = start_height
      ## Set the current height to start height at the beginning of the     
      ## protocol.                                                       
    F_primer_mix_vol = F_primer_vol + 3
    R_primer_mix_vol = R_primer_vol + 3 
      ## primer_mix_vol = volume for pipetting up and down                  
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    # Setting starting tip                                           
    if dispension_vol >= 19:
        ## If the mm volume to be dispendsed >= 19, assign p300 starting tip
        p300.starting_tip = tips_200.well(starting_tip_p200)
    p20.starting_tip = tips_20_1.well(starting_tip_p20)
    
    # Mastermix tube location
    MasterMix = mastermix_tube[mastermix_source]                   

    # Create a list of wells where mix and primers should go
    destination_wells = []
    PCR_strips_columns = ([PCR_strips.columns_by_name()[column_name] 
                           for column_name in ['2', '7', '11']])
    for column in PCR_strips_columns:
        for destination_well in column:
            destination_wells.append(destination_well)
    MasterMixAliquots = destination_wells[:number_of_primers]
      ## cuts off the list after a the number_of_primers number of wells 
    F_primer_source_wells = F_primer_source.wells()[:number_of_primers]
    Ra_primer_source_wells = Ra_primer_source.wells()[:number_of_primers]
    Rb_primer_source_wells = Rb_primer_source.wells()[:number_of_primers]
# =============================================================================

## PIPETTING===================================================================
## ============================================================================
## LIGHTS----------------------------------------------------------------------
    protocol.set_rail_lights(True)
## ----------------------------------------------------------------------------
## ALIQUOTING MASTERMIX--------------------------------------------------------
    if dispension_vol >= 19:
        pipette = p300
    else:
        pipette = p20
    for i, well in enumerate(MasterMixAliquots):
      ## aliquot mix, for each well do the following:                       
        if i == 0: 
            pipette.pick_up_tip()
              ## If we are at the first well, start by picking up a tip.    
        elif i % 8 == 0:
            pipette.drop_tip()
            pipette.pick_up_tip()
              ## Then, after every 8th well, drop tip and pick up new       
    
        current_height, pip_height, bottom_reached = vt.volume_tracking(
                mastermix_tube_type, dispension_vol, current_height)
                  ## call volume_tracking function, obtain current_height,  
                  ## pip_height and whether bottom_reached.                 
        
        if bottom_reached:
            aspiration_location = MasterMix.bottom(z=1)
            protocol.comment("You've reached the bottom of the tube!")
              ## If bottom is reached keep pipetting from bottom + 1        
        else:
            aspiration_location = MasterMix.bottom(pip_height)
              ## Set the location of where to aspirate from.                

        #### The actual aliquoting of mastermix                             
        pipette.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the       
          ## location specified in aspiration_location.                     
        pipette.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the         
          ## location specified in well (so a new well every time the       
          ## loop restarts)                                                 
        pipette.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill      
          ## completely when using a disposal volume by dispensing some     
          ## of the volume after each pipetting step. (blow-out to many     
          ## bubbles)                                                       
    pipette.drop_tip()   
## ----------------------------------------------------------------------------
## ADDING F PRIMERS TO THE MIX-------------------------------------------------
    for F_primer_well, destination_well in zip(
            F_primer_source_wells, MasterMixAliquots):
      ## Loop trough primer_wells and sample_wells                          
        p20.pick_up_tip()
        p20.aspirate(F_primer_vol, F_primer_well)
        p20.dispense(F_primer_vol, destination_well)
        p20.mix(3, F_primer_mix_vol, destination_well)
        p20.dispense(10, destination_well)
        p20.drop_tip()       
# ## ----------------------------------------------------------------------------
# ## ADDING Ra PRIMERS TO THE MIX------------------------------------------------
    for Ra_primer_well, destination_well in zip(
            Ra_primer_source_wells, MasterMixAliquots):
      ## Loop trough primer_wells and sample_wells                          
        p20.pick_up_tip()
        p20.aspirate(R_primer_vol, Ra_primer_well)
        p20.dispense(R_primer_vol, destination_well)
        p20.mix(3, R_primer_mix_vol, destination_well)
        p20.dispense(10, destination_well)
        p20.drop_tip()       
# ## ----------------------------------------------------------------------------
# ## ADDING Rb PRIMERS TO THE MIX-------------------------------------------------
    for Rb_primer_well, destination_well in zip(
            Rb_primer_source_wells, MasterMixAliquots):
      ## Loop trough primer_wells and sample_wells                          
        p20.pick_up_tip()
        p20.aspirate(R_primer_vol, Rb_primer_well)
        p20.dispense(R_primer_vol, destination_well)
        p20.mix(3, R_primer_mix_vol, destination_well)
        p20.dispense(10, destination_well)
        p20.drop_tip()       
## ----------------------------------------------------------------------------
## LIGHTS----------------------------------------------------------------------
    protocol.set_rail_lights(False)
# ----------------------------------------------------------------------------
## ============================================================================