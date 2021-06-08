# =============================================================================
# Author(s): Sanne Vreugdenhil
# Creation date: 210608
# Description: protocol to aliquot PCR mix into PCR strips
#   and then add (barcoded) primers to them 
# =============================================================================

# ==========================IMPORT STATEMENTS==================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
  
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
# =============================================================================


# =====================VOLUME TRACKING FUNCTIONS===============================
# =============================================================================
## Because we could not manage to get the robot working with separate       ##
## modules and we do want to try-out the protocol, in this version the      ##
## module is integrated into the main protocol.                             ##

##### Import statements
import math
  ## Import math module to allow using π in calculations                    ##

def cal_start_height(container, start_vol):
    """Module to calculate the liquid height in a tube at the start"""
    ##### Defining container dimensions
    ## Depending on the type of container, these are the dimensions         ##
    if container == 'tube_1.5mL':
        diameter_top = 8.7          #diameter of the top of the tube in mm
        diameter_tip = 3.6          #diameter of the tip of the tube in mm
        height_conical_tip = 17.8   #tube - straight part
    elif container == 'tube_2mL':
        diameter_top = 9.85         #diameter of the top of the tube in mm
        diameter_tip = 2.4          #diameter of the tip of the tube in mm
        height_conical_tip = 6.8    #tube - straight part
    elif container == 'tube_5mL':
        diameter_top = 13           #diameter of the top of the tube in mm
        diameter_tip = 3.3          #diameter of the tip of the tube in mm
        height_conical_tip = 66.1 - 43.6 - 1.3 #tube - straight part - bottom wall
    elif container == 'tube_5mL_snap':
        diameter_top = 13.3         #diameter of the top of the tube in mm
        diameter_tip = 3.3          #diameter of the tip of the tube in mm
        height_conical_tip = 55.4 - 2.2 - 34.12 #tube - straight part - rim
    elif container == 'tube_15mL':
        diameter_top = 15.16        #diameter of the top of the tube in mm
        diameter_tip = 2.16         #diameter of the tip of the tube in mm
        height_conical_tip = 22.1   #tube - straight part
    elif container == 'tube_50mL':
        diameter_top = 27.48        #diameter of the top of the tube in mm
        diameter_tip = 4.7          #diameter of the tip of the tube in mm
        height_conical_tip = 15.3   #tube - straight part
        
    
    radius_top = diameter_top / 2         #radius of the top of the tube in mm
    radius_tip = diameter_tip / 2         #radius of the tip of the tube in mm
    vol_conical_tip = ((1/3) * math.pi * height_conical_tip *
                    ((radius_tip**2) + (radius_tip*radius_top) +
                     (radius_top**2)))
    ## How much volume fills up the conical tip: v = (1/3)*π*h*(r²+r*R+R²)  ##
    
    ##### Calculating start height
    cylinder_vol = start_vol - vol_conical_tip    # vol in straight part
    start_height = (
            height_conical_tip +        # current_height = height conical part 
            (cylinder_vol /             # + height cylindrical part
            (math.pi*((radius_top)**2)))
            )
    ## Initially start higher in a 15mL tube. Due to the shape of the tube, ##
    ## volume tracking doesn't work perfect when assuming that the entire   ##
    ## tube is cylindrical. This is partly solved by adding 7 mm to the     ##
    ## start_height.                                                        ##
    if container == 'tube_15mL':
        start_height = start_height + 7
    
    return start_height

def volume_tracking(container, dispension_vol, current_height):
    """
    At this moment the OT-2 doesn't have a volume tracking function.
    By default, aspiration occurs from the bottom of a container. When a
    container is filled with liquid, this can cause the pipette to be 
    submurged beyond the pipette tip, possibly damaging the pipette. 
    Furthermore, when a container is already full, it will overflow when the 
    pipette is reaching for the bottom. Also, when the pipette goes far into 
    the liquid, a lot of liquid will stick to the outside of the pipette tip.
    This will make pipetting less acurate and increases the risk of cross-
    contamination.
    
    This module introduces calculations for liquid levels in tubes
    and allows for tracking the height of the liquid in a container 
    during a protocol.
    
    Input for this function is:
        container = type of container. Several options are available:
            'tube_1.5mL'
            'tube_2mL'
            'tube_5mL'
            'tube_5mL_snap'
            'tube_15mL'
            'tube_50mL'
        current_vol = current volume during the run. At the start of the
        protocol this should be set at the start_vol of the protocol.
        aspiration_vol = the volume that will be aspirated in the tracked steps
    
    Output of this function is:
        current_height = the height of the current liquid level in mm from the 
        bottom of the container.
        delta_height = The height difference in mm of the liquid inside the 
        container between before and after aspiration. Delta_height is returned 
        so that in the main protocol a safety-step can be implemented:
        (if current_height - delta_height <= 1: some kind of error handling)
    """

    ##### Defining container dimensions
    ## Depending on the type of container, these are the dimensions         ##
    if container == 'tube_1.5mL':
        diameter = 8.7          #diameter of the top of the tube in mm
    elif container == 'tube_2mL':
        diameter = 9.85         #diameter of the top of the tube in mm
    elif container == 'tube_5mL':
        diameter = 13           #diameter of the top of the tube in mm
    elif container == 'tube_5mL_snap':
        diameter = 13.3         #diameter of the top of the tube in mm
    elif container == 'tube_15mL':
        diameter = 15.16        #diameter of the top of the tube in mm
        height_conical_tip = 22.1   #tube - straight part
        offset_height = height_conical_tip + 18 
        ## offset_height = height from where to start using                 ##
        ## current_height - 1 so that the pipette tip stays submerged.      ##
    elif container == 'tube_50mL':
        diameter = 27.48        #diameter of the top of the tube in mm
    
    ## volume of a cylinder is calculated as follows:                       ##
    ## v = π*r²*h  -->  h = v/(π*r²)                                        ##
    
    radius = diameter / 2         #radius of the top of the tube in mm
    
    ##### Calculate delta height per dispensed volume
    delta_height =  (dispension_vol/(math.pi*((radius)**2)))

    ##### Update current_height 
    current_height = current_height - delta_height
    ## The current_height (after aspiration) must be updated before the     ##
    ## actual aspiration, because during aspiration the liquid will reach   ## 
    ## that level.                                                          ##
    if container == 'tube_15mL' and current_height < offset_height:
        current_height = current_height - 1
    ## Volume tracking when assuming the entire tube is cylindrical doesn't ##
    ## work very well with a 15 mL tube. Therefore, we need to adjust some  ##
    ## values so that we do the volume tracking as good as possible.        ##
    ## start_height is already adjusted so that we start a little heigher,  ##
    ## however at the offset_height the pipette didn't reach the liquid     ##
    ## anymore. So we lower the current_height with 1 so that the pipette   ##
    ## tip is always submerged and the entire tube is emptied.              ##
    
    return current_height, delta_height
# =============================================================================


# ================================METADATA=====================================
# =============================================================================
metadata = {
    'protocolName': '210608_eDNA_fish_test_PCR_WALL-E',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('eDNA fish 12S test PCR - aliquoting mix and primers'),
    'apiLevel': '2.9'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting Accustart toughmix with EvaGreen added from a 5 mL tube to a 
     96-wells plate; using volume tracking so that the pipette starts 
    aspirating at the starting height of the liquid and goes down as the 
    volume decreases.
    Adding primers from PCR strips (with 10 uM primer F&R primer mix) or
    1.5mL tubes (with 10 uM F or 10 uM R) to 96-wells plate (with mastermix).
    """
# =============================================================================


# ======================LOADING LABWARE AND PIPETTES===========================
# =============================================================================
    ## For available labware see "labware/list_of_available_labware".       ##
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', #labware definition
        3,                                  #deck position
        'tips_200')                         #custom name
    tips_20 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                 #deck position
        'tips_20')                          #custom name   
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',
        4,
        'plate_96')
    primer_tubes = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        1,                                                       #deck position
        'primer_tubes')                                          #custom name  
   ##### !!! OPTION 1: ROBOT      
    # tubes_5mL = protocol.load_labware(
    #     'eppendorfscrewcap_15_tuberack_5000ul', #labware def
    #     2,                                      #deck position
    #     '5mL_tubes')                            #custom name
    # primer_strips = protocol.load_labware(
    #     'pcrstrips_96_wellplate_200ul',    #labware definition
    #     7,                                 #deck position
    #     'primer strips')                   #custom name          
   ##### !!! OPTION 2: SIMULATOR      
    with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
              "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
            labware_def_5mL = json.load(labware_file)
    tubes_5mL = protocol.load_labware_from_definition( 
            labware_def_5mL,   #variable derived from opening json
            2,                 #deck position
            '5mL_tubes')       #custom name 
    with open("labware/pcrstrips_96_wellplate_200ul/"
              "pcrstrips_96_wellplate_200ul.json") as labware_file:
            labware_def_pcrstrips = json.load(labware_file)
    primer_strips = protocol.load_labware_from_definition( 
        labware_def_pcrstrips, #variable derived from opening json
        7,                     #deck position
        'primer_strips')       #custom name  
    
    ##### Loading pipettes
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
    start_vol = 2226 
      ## The start_vol is the volume (ul) that is in the source labware at  ##
      ## the start of the protocol.                                         ##
    dispension_vol = 42 
      ## The dispension_vol is the volume (ul) that needs to be aliquoted   ##
      ## into the destination wells/tubes.                                  ##
    primer_vol_label = 3
      ## The primer_vol_label is the volume (ul) of barcoded F&R primer that##
      ## needs to be added to the reactions that get a barcode.             ##
    primer_vol = 1.5
      ## The primer_vol is the volume (ul) of NON barcoded F or R primer    ##
      ## that needs to be added to the reactions that do NOT get a barcode. ##
    p300.starting_tip = tips_200.well('A1')
    p20.starting_tip = tips_20.well('A1')
      ## The starting_tip is the location of first pipette tip in the box   ##
# =============================================================================


# ==========================PREDIFINED VARIABLES===============================
# =============================================================================
    container = 'tube_5mL'
      ## The container variable is needed for the volume tracking module.   ##
      ## It tells the module which dimensions to use for the calculations   ##
      ## of the pipette height. It is the source labware from which liquid  ##
      ## is aliquoted.                                                      ##
      ## There are several options to choose from:                          ##
      ## 'tube_1.5ml', 'tube_2mL', 'tube_5mL', 'tube_15mL', 'tube_50mL'   	##
    aspiration_vol = dispension_vol + (dispension_vol/100*2)
      ## The aspiration_vol is the volume (ul) that is aspirated from the   ##
      ## container.                                                         ##
# ==========================creating mix well list=============================
## This is a list with wells in plate_96 that should be filled with mastermix##   
    mastermix = []
      ## Create an empty list to append wells to for the mastermix wells.   ##
    mm_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in
         ['1', '2', '3', '4', '5', '6']]
        )
    for column in mm_columns:
        for well in column:
            mastermix.append(well)
      ## Separate the columns into wells and append them to the empty       ##
      ## mastermix wells list                                               ##
# ======================create list for labeled primers========================
## This is a list with the wells in primer_strips where the primers should  ##
## be pipetted from. This list is used to pipette the labeled primers       ##
## to the corresponding wells in plate_96 (automatically first ~3.5 columns)##
    labeled_primers = []
      ## Create an empty list to append wells to for the primer wells.      ##
    labeled_primer_columns = (
        [primer_strips.columns_by_name()[column_name] for column_name in
         ['2', '7']]
        )
      ## Make a list of columns for the primers, this is a list of lists!   ##
    for column in labeled_primer_columns:
        for well in column:
            labeled_primers.append(well)
      ## Separate the columns into wells and append them to the empty primer## 
      ## wells list                                                         ##
    labeled_primer_wells = (
        [primer_strips.wells_by_name()[well_name] for well_name in
         ['A11', 'B11', 'C11', 'D11', 'E11']]
        ) 
      ## Make a list of the remaining primer wells.                         ## 
    for well in labeled_primer_wells:
        labeled_primers.append(well)
      ## Append the wells to the list of primer wells.                      ##
# =======================create list for unlabeled primers=====================
## This is a list with the wells in plate_96, that should be filled with    ##
## unlabeled primers (so the fish samples, NTCs and the std dilution series)##
## --> for the wells that do not get labeled primer                         ##
    unlabeled_primer_dest = []
      ## Create an empty list to append the wells where the unlabeled       ##
      ## primers should go.                                                 ##
    unlabeled_primer_wells = (
        [plate_96.wells_by_name()[well_name] for well_name in 
         ['F3', 'G3', 'H3' ]])
    for well in unlabeled_primer_wells:
        unlabeled_primer_dest.append(well)
    unlabeled_primer_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in
         ['5', '6']]
        )
    for column in unlabeled_primer_columns:
        for well in column:
            unlabeled_primer_dest.append(well)
# =============================================================================
# ==============================create a variable for ===============================================

    ##### Variables for volume tracking
    start_height = cal_start_height(container, start_vol)
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
        ## If we are at the first well, start by picking up a tip.          ##
        if i == 0: 
            p300.pick_up_tip()
        ## Then, after every 8th well, drop tip and pick up a new one.      ##
        elif i % 8 == 0:
            p300.drop_tip()
            p300.pick_up_tip()
        current_height, delta_height = volume_tracking(
            container, dispension_vol, current_height)  
          ## The volume_tracking function needs the arguments container ##
          ## dispension_vol and the current_height which we have set in ##
          ## this protocol. With those variables, the function updates  ##
          ## the current_height and calculates the delta_height of the  ## 
          ## liquid after the next aspiration step.                     ##
        pip_height = current_height - 2
          ## Make sure that the pipette tip is always submerged by      ##
          ## setting the current height 2 mm below its actual height    ##
        if current_height - delta_height <= 1: 
            aspiration_location = tubes_5mL['C1'].bottom(z=1) #!!!
            protocol.comment("You've reached the bottom!")
        else:
            aspiration_location = tubes_5mL['C1'].bottom(pip_height) #!!!
          ## If the level of the liquid in the next run of the loop will## 
          ## be smaller than 1 we have reached the bottom of the tube.  ##
          ## To prevent the pipette from crashing into the bottom, we   ##
          ## tell it to go home and pause the protocol so that this can ##
          ## never happen. Set the location of where to aspirate from.  ##
          ## Because we put this in the loop, the location will change  ##
          ## to the newly calculated height after each pipetting step.  ##
        p300.aspirate(aspiration_vol, aspiration_location)
          ## Aspirate the amount specified in aspiration_vol from the   ##
          ## location specified in aspiration_location.                 ##
        p300.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the     ##
          ## location specified in well (so a new well every time the   ##
          ## loop restarts)                                             ##
        p300.dispense(10, aspiration_location)
          ## Alternative for blow-out, make sure the tip doesn't fill   ##
          ## completely when using a disposal volume by dispensing some ##
          ## of the volume after each pipetting step. (blow-out to many ##
          ## bubbles)                                                   ##
    p300.drop_tip()      
# =============================================================================


# ==========================ADDING LABELED PRIMERS=============================
# =============================================================================
## For the columns in both the source (primers) and the destination     ##
    ## (mix): loop trough the wells in those columns.                       #
    for primer_tube, mix_tube in zip(labeled_primers, mastermix):
        p20.pick_up_tip()
        p20.aspirate(primer_vol, primer_tube)
        ## primer_mix_vol = volume for pipetting up and down            ##
        primer_mix_vol = primer_vol + 3
        p20.mix(3, primer_mix_vol, mix_tube)
        ## primer_dispense_vol = volume to dispense that was mixed      ##
        primer_dispense_vol = primer_mix_vol + 3
        p20.dispense(primer_dispense_vol, mix_tube)
        p20.drop_tip()
# =============================================================================


# ==========================ADDING UNLABELED PRIMERS===========================
# =============================================================================
## For the columns in both the source (primers) and the destination     ##
    ## (mix): loop trough the wells in those columns.                       #
    for well in unlabeled_primer_dest:
        p20.pick_up_tip()
        p20.aspirate(primer_vol, [primer_tubes.wells_by_name()[well_name]
                                  for well_name in ])
        ## primer_mix_vol = volume for pipetting up and down            ##
        primer_mix_vol = primer_vol + 3
        p20.mix(3, primer_mix_vol, well)
        ## primer_dispense_vol = volume to dispense that was mixed      ##
        primer_dispense_vol = primer_mix_vol + 3
        p20.dispense(primer_dispense_vol, mix_tube)
        p20.drop_tip()
# =============================================================================
