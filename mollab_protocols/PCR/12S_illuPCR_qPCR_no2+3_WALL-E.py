# =============================================================================
# Author(s): Sanne Vreugdenhil
# Creation date: 210617
# Description: 
#   - aliquot mastermix in a 96 wells plate 
#   - add barcoded primers from PCR strips to the 96 wells plate
#   - add 1 barcode to the wells that are designated for the std dil series
# =============================================================================


# ==========================IMPORT STATEMENTS==================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
  
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##

#### !!! OPTION 1: ROBOT
# from data.user_storage.mollab_modules import volume_tracking_v1 as vt
##### !!! OPTION 2: SIMULATOR
from mollab_modules import volume_tracking_v1 as vt
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': '12S_illuPCR_qPCR_no1+2_WALL-E',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Illumina PCR - aliquoting mix and primers - 12S'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix from a 5 mL tube to a 96 wells plate;
    using volume tracking so that the pipette starts 
    aspirating at the starting height of the liquid and goes down as the 
    volume decreases.
    Adding primers from PCR strips (with 10 uM primer F&R primer mix)
    the 96 wells plate.
    """
# =============================================================================


# ======================LOADING LABWARE AND PIPETTES===========================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    # Pipette tips    
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        2,                                  #deck position
        '200tips')                          #custom name
    tips_20_1 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        7,                                  #deck position
        '20tips')                           #custom name       
    tips_20_2 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                 #deck position
        '20tips')                           #custom name    
       
    # Tube racks & plates
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    #labware definition
        6,                                  #deck position
        'plate_96')                         #custom name       
   ##### !!! OPTION 1: ROBOT      
    # mastermix_tube = protocol.load_labware(
    #     'eppendorfscrewcap_15_tuberack_5000ul',  #labware def
    #       3,                                     #deck position
    #       'mastermix_tube')                      #custom name          
    # primer_strips_1 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     4,                                 #deck position
    #     'primer strips 1')                 #custom name
    # primer_strips_2 = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     1,                                 #deck position
    #     'primer strips 2')                 #custom name                  
   ##### !!! OPTION 2: SIMULATOR      
    with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
              labware_def_5mL = json.load(labware_file)
    mastermix_tube = protocol.load_labware_from_definition( 
        labware_def_5mL,   #variable derived from opening json
        3,                 #deck position
        'mastermix_tube')         #custom name 
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
    primer_strips_1 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        4,                     #deck position
        'primer_strips_1')     #custom name  
    primer_strips_2 = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        1,                     #deck position
        'primer_strips_2')     #custom name                            

    # Pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                 #instrument definition
        'right',                            #mount position
        tip_racks=[tips_200])               #assigned tiprack
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20_1, tips_20_2])   #assigned tiprack
# =============================================================================


# ==========================VARIABLES TO SET#!!!===============================
# =============================================================================
    start_vol = 4452 
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##
    dispension_vol = 42 
      ## The dispension_vol is the volume (ul) that needs to be aliquoted   ##
      ## into the destination wells/tubes.                                  ##
    primer_vol = 3 
      ## The primer_vol is the volume (ul) of primer added to the PCR       ##
      ## reaction.                                                          ##
    p300.starting_tip = tips_200.well('A1')
    p20.starting_tip = tips_20_1.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##
    container = 'tube_5mL'
    mastermix_source = mastermix_tube['C1']
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
      ## There are several options to choose from:                          ##
      ## 'tube_1.5ml', 'tube_2mL', 'tube_5mL', 'tube_15mL', 'tube_50mL'   	##
    std_dilution_primer = primer_strips_2['B11']
# Mastermix destination wells==================================================
    mastermix_destination_wells = plate_96.wells()
# Primer source tubes==========================================================
    primer_source_tubes = []
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
            primer_source_tubes.append(well)
      ## Separate the columns into wells and append them to list            ##
    primer_wells = (
        [primer_strips_2.wells_by_name()[well_name] for well_name in
         ['A11', 'B11']]
        ) 
      ## Make a list of separate wells                                      ## 
    for well in primer_wells:
        primer_source_tubes.append(well)
      ## Append the wells to the list                                       ##  
# Primer destinations - odd columns============================================ 
    odd_primer_destinations = []
      ## Create an empty list to append wells to                            ##
    odd_primer_destinations_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in 
         ['1', '3', '5', '7', '9']]
        )
      ## Make a list of columns, this is a list of lists!                   ##
    for column in odd_primer_destinations_columns:
        for well in column:
            odd_primer_destinations.append(well)
      ## Separate the columns into wells and append them to list            ##
    odd_primer_destinations_wells = (
        [plate_96.wells_by_name()[well_name] for well_name in 
         ['G11', 'H11']]
        )
      ## Make a list of separate wells                                      ## 
    for well in odd_primer_destinations_wells:
        odd_primer_destinations.append(well)
      ## Append the wells to the list                                       ##  
# Primer destinations - even columns=========================================== 
    even_primer_destinations = []
       ## Create an empty list to append wells to                            ##
    even_primer_destinations_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in 
         ['2', '4', '6', '8', '10']]
        )
      ## Make a list of columns, this is a list of lists!                   ##
    for column in even_primer_destinations_columns:
        for well in column:
            even_primer_destinations.append(well)
      ## Separate the columns into wells and append them to list            ##
    even_primer_destinations_wells = (
        [plate_96.wells_by_name()[well_name] for well_name in 
         ['G12', 'H12']]
        )
      ## Make a list of separate wells                                      ## 
    for well in even_primer_destinations_wells:
        even_primer_destinations.append(well)
      ## Append the wells to the list                                       ##  
# Primer destinations - standard dilution series===============================
    standard_dil_primer_destinations = []
      ## Create an empty list to append wells to                            ##
    std_wells = (
        [plate_96.wells_by_name()[well_name] for well_name in
         ['A11', 'B11', 'C11', 'D11', 'E11', 'F11',
          'A12', 'B12', 'C12', 'D12', 'E12', 'F12']]
        )
      ## Make a list of separate wells                                      ## 
    for well in std_wells:
        standard_dil_primer_destinations.append(well)
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
    for i, well in enumerate(mastermix_destination_wells):
    ## Name all the wells in destination 'well', for all these do:          ## 
        if i == 0:
            p300.pick_up_tip()
        ## If we are at the first well, start by picking up a tip.          ##
        elif i % 8 == 0:
            p300.drop_tip()
            p300.pick_up_tip() 
        ## After every 8th well, drop tip and pick up a new one.            ##
        current_height, pip_height, bottom_reached = vt.volume_tracking(
            container, dispension_vol, current_height)  
          ## The volume_tracking function needs the arguments container,    ##
          ## dispension_vol, and the current_height which we have set in    ##
          ## this protocol. With those variables, the function updates      ##
          ## the current_height, the pip_height and calculates the          ##
          ## delta_height of the liquid after the next aspiration step.     ##
        if bottom_reached: 
            aspiration_location = mastermix_source.bottom(z=1)              
            protocol.comment("You've reached the bottom!")
        else:
            aspiration_location = mastermix_source.bottom(pip_height) 
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


# =========================ADDING PRIMERS TO SAMPLES===========================
# =============================================================================
# ==============adding primers to 1st half of the sample wells=================    
    ## For the columns in both the source (primers) and the destination     ##
    ## (mix): loop trough the wells in those columns.                       ##
    for primer_tube, mix_tube in zip(
            primer_source_tubes, odd_primer_destinations):
        p20.pick_up_tip()
        p20.aspirate(primer_vol, primer_tube)
        primer_mix_vol = primer_vol + 3
        ## primer_mix_vol = volume for pipetting up and down                ##
        p20.mix(3, primer_mix_vol, mix_tube)
        primer_dispense_vol = primer_mix_vol + 3
        ## primer_dispense_vol = volume to dispense that was mixed          ##
        p20.dispense(primer_dispense_vol, mix_tube)
        p20.drop_tip()
# ==============adding primers to 2nd half of the sample wells=================    
    ## For the columns in both the source (primers) and the destination     ##
    ## (mix): loop trough the wells in those columns.                       ##
    for primer_tube, mix_tube in zip(
            primer_source_tubes, even_primer_destinations):
        p20.pick_up_tip()
        p20.aspirate(primer_vol, primer_tube)
        primer_mix_vol = primer_vol + 3
        ## primer_mix_vol = volume for pipetting up and down                ##
        p20.mix(3, primer_mix_vol, mix_tube)
        primer_dispense_vol = primer_mix_vol + 3
        ## primer_dispense_vol = volume to dispense that was mixed          ##
        p20.dispense(primer_dispense_vol, mix_tube)
        p20.drop_tip()
# ==================adding primers to std dilution series======================
    ## For the columns in both the source (primers) and the destination     ##
    ## (mix): loop trough the wells in those columns.                       #
    for well in standard_dil_primer_destinations:
        p20.pick_up_tip()
        p20.aspirate(primer_vol, std_dilution_primer)
        primer_mix_vol = primer_vol + 3
        ## primer_mix_vol = volume for pipetting up and down                ##
        p20.mix(3, primer_mix_vol, well)
        primer_dispense_vol = primer_mix_vol + 3
        ## primer_dispense_vol = volume to dispense that was mixed      ##
        p20.dispense(primer_dispense_vol, well)
        p20.drop_tip()
# =============================================================================
