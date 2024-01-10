# =============================================================================
# Author(s): Sanne Vreugdenhil
# Creation date: 210527
# Description: protocol to aliquot PCR mix into PCR strips
#   and then add barcoded primers to them - specific for 12S PCR.
# =============================================================================

# ==========================IMPORT STATEMENTS==================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
  
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##

##### !!! OPTION 1: ROBOT
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
##### !!! OPTION 2: SIMULATOR
from mollab_modules import volume_tracking_v1 as vt
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': '12S_illuPCR_strips_WALL-E',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('Illumina PCR - aliquoting mix and primers - 12S'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix from a 5 mL tube to 5x + 2 wells PCR strips in 
    2x 96-wells plates; using volume tracking so that the pipette starts 
    aspirating at the starting height of the liquid and goes down as the 
    volume decreases.
    Adding primers from PCR strips (with 10 uM primer F&R primer mix)
    to PCR strips (with mastermix).
    """
# =============================================================================


# ======================LOADING LABWARE AND PIPETTES===========================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    # Pipette tips
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        3,                                  #deck position
        '200tips')                          #custom name
    tips_20 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        4,                                  #deck position
        '20tips')                           #custom name   

    # Tube racks & plates                 
    ##### !!! OPTION 1: ROBOT      
    # mastermix_tube = protocol.load_labware(
    #     'eppendorfscrewcap_15_tuberack_5000ul', #labware def
    #      5,                                     #deck position
    #      'mastermix_tube')                             #custom name          
    # primer_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     6,                                 #deck position
    #     'primer_strips_1')                 #custom name
    # primer_strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     7,                                 #deck position
    #     'primer_strips_2')                 #custom name                  
    # mastermix_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     8,                                 #deck position
    #     'mastermix_strips_1')                    #custom name    
    # mastermix_strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     9,                                 #deck position
    #     'mastermix_strips_2')                    #custom name                      
    ##### !!! OPTION 2: SIMULATOR      
    with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
               "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
             labware_def_5mL = json.load(labware_file)
    mastermix_tube = protocol.load_labware_from_definition( 
             labware_def_5mL,   #variable derived from opening json
             5,                 #deck position
             'mastermix_tube')       #custom name 
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
    primer_strips_1 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        6,                     #deck position
        'primer_strips_1')     #custom name  
    primer_strips_2 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        7,                     #deck position
        'primer_strips_2')     #custom name                            
    mastermix_strips_1 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        8,                     #deck position
        'mastermix_strips_1')        #custom name   
    mastermix_strips_2 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        9,                     #deck position
        'mastermix_strips_2')         #custom name                  
    
    # Pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20])                #assigned tiprack
# =============================================================================


# ==========================VARIABLES TO SET#!!!===============================
# =============================================================================
    start_vol = 1974 
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##
    dispension_vol = 42 
      ## The dispension_vol is the volume (ul) that needs to be aliquoted   ##
      ## into the destination wells/tubes.                                  ##
    primer_vol = 3 
      ## The sample_vol is the volume (ul) of sample added to the PCR       ##
      ## reaction.                                                          ##
    p300.starting_tip = tips_200.well('A1')
    p20.starting_tip = tips_20.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##
    container = 'tube_5mL'
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
      ## There are several options to choose from:                          ##
      ## 'tube_1.5ml', 'tube_2mL', 'tube_5mL', 'tube_15mL', 'tube_50mL'   	##
    mastermix_source = mastermix_tube['C1']
# Mastermix destination wells==================================================
    mastermix = []
      ## Create an empty list to append wells to                            ##
    mastermix_columns = (
        [mastermix_strips_1.columns_by_name()[column_name] for column_name in
         ['2', '7', '11']] + 
        [mastermix_strips_2.columns_by_name()[column_name] for column_name in
         ['2', '7']] 
        )
      ## Make a list of columns, this is a list of lists!                   ##
    for column in mastermix_columns:
        for well in column:
            mastermix.append(well)
      ## Separate the columns into wells and append them to list            ##
    mastermix_wells = (
        [mastermix_strips_2.wells_by_name()[well_name] for well_name in
         ['A11', 'B11']]
        )
      ## Make a list of separate wells                                      ## 
    for well in mastermix_wells:
        mastermix.append(well)
      ## Append the wells to the list                                       ##
# Primer source tubes==========================================================
    primers = []
      ## Create an empty list to append wells to                            ##
    primer_columns = (
        [primer_strips_1.columns_by_name()[column_name] for column_name in
         ['2', '7', '11']] + 
        [primer_strips_2.columns_by_name()[column_name] for column_name in
         ['2', '7']] 
        )
      ## Make a list of columns, this is a list of lists!                   ##
    for column in primer_columns:
        for well in column:
            primers.append(well)
      ## Separate the columns into wells and append them to list            ##
    primer_wells = (
        [primer_strips_2.wells_by_name()[well_name] for well_name in
         ['A11', 'B11']]
        ) 
      ## Make a list of separate wells                                      ## 
    for well in primer_wells:
        primers.append(well)
      ## Append the wells to the list                                       ##
# =============================================================================
# =============================================================================


# ==========================PREDIFINED VARIABLES===============================
# =============================================================================
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
      ## The aspiration_vol is the volume (ul) that is aspirated from the   ##
      ## container.                                                         ##
    ##### Variables for volume tracking
    start_height = vt.cal_start_height(container, start_vol)
      ## Call start height calculation function from volume tracking module.##
    current_height = start_height
      ## Set the current height to start height at the beginning of the     ##
      ## protocol.                                                          ##
# =============================================================================


# ===============================ALIQUOTING MIX================================
# =============================================================================
    ## For each column in destination_wells, pick up a tip, than for each   ##
    ## well in these columns pipette mix, and after the+ column drop the tip##
    ## Repeat untill all columns in the list are done.                      ##      
    for i, well in enumerate(mastermix):
    ## Name all the wells in the plate 'well', for all these do:            ## 
        if i == 0:
            p300.pick_up_tip()
          ## If we are at the first well, start by picking up a tip.        ##
        elif i % 8 == 0:
            p300.drop_tip()
            p300.pick_up_tip() 
          ## Then, after every 8th well, drop tip and pick up a new one.    ##
        current_height, pip_height, bottom_reached = vt.volume_tracking(
            container, dispension_vol, current_height)  
          ## The volume_tracking function needs the arguments container,    ##
          ## dispension_vol, and the current_height which we have set in    ##
          ## this protocol. With those variables, the function updates      ##
          ## the current_height, the pip_height and calculates the          ##
          ## delta_height of the liquid after the next aspiration step.     ##
        if bottom_reached: 
            aspiration_location = mastermix_source.bottom(z=1) #!!!
            protocol.comment("You've reached the bottom!")
        else:
            aspiration_location = mastermix_source.bottom(pip_height) #!!!
          ## If the level of the liquid in the next run of the loop will    ## 
          ## be smaller than 1 we have reached the bottom of the tube.      ##
          ## To prevent the pipette from crashing into the bottom, we       ##
          ## tell it to go home and pause the protocol so that this can     ##
          ## never happen. Set the location of where to aspirate from.      ##
          ## Because we put this in the loop, the location will change      ##
          ## to the newly calculated height after each pipetting step.      ##
        p300.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the       ##
          ## location specified in aspiration_location.                     ##
        p300.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the         ##
          ## location specified in well (so a new well every time the       ##
          ## loop restarts)                                                 ##
        p300.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill       ##
          ## completely when using a disposal volume by dispensing some     ##
          ## of the volume after each pipetting step. (blow-out to many     ##
          ## bubbles)                                                       ##
    p300.drop_tip()      
# =============================================================================


# ===============================ADDING PRIMERS================================
# =============================================================================
    ## For the columns in both the source (primers) and the destination     ##
    ## (mix): loop trough the wells in those columns.                       #
    for primer_tube, mix_tube in zip(primers, mastermix):
        p20.pick_up_tip()
        p20.aspirate(primer_vol, primer_tube)
        p20.dispense(primer_vol, mix_tube)
        primer_mix_vol = primer_vol + 3
        ## primer_mix_vol = volume for pipetting up and down                ##
        p20.mix(3, primer_mix_vol, mix_tube)
        p20.dispense(10, mix_tube)
        p20.drop_tip()
# =============================================================================
