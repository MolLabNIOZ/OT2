"""
VERSION: April 2023
This is a protocol written for WALL-E for the addition of mastermix and 
barcoded primers to a 96-wells plate.

In this new version, we added the option to skip a list of primers. In a first 
round of PCRs for a specific sample batch we saw that some of the samples did
not work. In the duplicate and triplicate PCRs we wanted to skip the not 
working samples. 

You have to provide:
    Location of the starting tips in both the P20 and P200 
    Number of samples (excl. NTC and mock)
    Number of NTCs 
        NOTE: The NTC should ALWAYS be at the end of the plate, this is
        for the protocol for EVE (that skips the last well)
        NOTE: If you want NTCs in the middle, pretend that they are samples and
        do not put a sample at that position in EVE.
    Do you want the robot to add a mock sample?:
        if True -- robot adds an extra well + primer combination 
    
    Whether you are doing a qPCR or not 
    Tube your mastermix is in (1.5mL or 5mL tube)
        (Location of your mastermix tube in the rack)
    Tube type of the mastermix
    Volume of your mastermix
    Volume of the mastermix that is to be dispensed
    Tube type of the primers
    Volume of the primers that is to be dispensed
    Location of the first Forward primer
    Location of the first Reverse primer
    List with wells of primers to skip
      
The number of unique primer combinations is based on the number of samples +
the number of NTCs + the mock. The maximum is 96!

When not doing a qPCR:
    Lights are turned on and off
    Mastermix is aliquoted from the mastermix tube into the plate
    Primers are added from the primer source to the plate 

In addition for the qPCR:
    The lights are not turned on and off
    Primer is added from a separate 1.5mL tube to the standard
    series and the standard sample wells. 
        NOTE: the standard series are pipetted into the last 3 columns of 
        the plate. The standard sample is pipetted in the wells directly 
        following the sample wells (incl. NTC and mock).
    A big_primer_source is added on deck position 8, this is a 1.5mL tube
    that contains 1 primerpair that is to be added to the standard series and
    the standard sample.

Updates:
(SV) 211027: 
    - added choice between 5mL or 1.5mL mm tube
(MB) 211203: 
    - use p20 instead of p300 for MM volumes <19µL
(SV) 211213: 
    - added choice between 96_well plate and primers as primer source
    - rearranged variables to set
    - primer for standards is added from a separate tube to standard series
    and standard sample
    - clean up
(SV) 220616:
    - major update of the protocol, remove option for strips, pipette a forward
    and a reverse primer, starting well of reverse primer changable so that
    the lab team can provide a protocol with unique barcode combinations for 
    each user
    - addition of labware offsets for the new robot update and API level 2.12
(MB) 220728:
    - added the option to shift forward primers as well. 
    - added the option to only use certain columns of the PCR plate.
(MB) 230123:
    -changed to tipone p20 tips
(MB) 230419:
    -added the option to skip specific primers
    -removed specification of mastermix well
    
"""
# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the 20µL tips?
starting_tip_p20 = 'A1'
# If mastermix dispense > 19: What is the starting position of the 200µL tips?
starting_tip_p200 = 'A1'
  ## If not applicable, you do not have to change anything
  
# How many samples do you want to include?
number_of_samples = 95
# Including all skipped wells!           

# What primers do you want to skip
primers_to_skip = [4,5,7,9,12,13,16,31,32,39,40,41,42,53,54,
                    56,57,58,59,68,70,71,72,73,78,79,84,86,87]
# This is the index of the primers, where the first_F/R_primer = 0
# Wells in the PCR plate will also be skipped to make pooling easier

# How many NTCs to include 
number_of_NTCs = 0 
  ## NOTE: The NTC should ALWAYS be at the end of your plate!!              

# Will a mock sample be included?
mock = False
  ## True if mock has to be added by the robot.                             
  ## False if mock is not added by the robot.                               

# Are you doing a qPCR or a regular PCR?
qPCR = False
  ## True or False                                                          
  ## Lights off if qPCR, standard sample and/or standard dilution series
if qPCR:
    # How many dilution serie replicates do you want to include?
    number_of_std_series = 1  
    # How many dilutions are in the standard dilution series?
    length_std_series = 8  
      ## length_of_std_series  MAX == 8                                     
    # How many replicates of the standard sample are you taking?
    number_of_std_samples = 6
    # In what well is the primer for the standards (sample and series) located?
    std_primer_loc = 'D1'                   
else:
    ## If we are not doing a qPCR - protocol uses these values.             
    number_of_std_series = 0  
    length_std_series = 0
    number_of_std_samples = 0

# Which tube are you using for your mastermix? (options 1.5mL or 5mL)
mastermix_tube_type = 'tube_5mL'
  ## For volume < 1300: 'tube_1.5mL'                                        
  ## For volume > 1300: 'tube_5mL'                                          

# What is the total volume (µL) of your mix?
start_vol = 1800
  ## The start_vol_m is the volume (µL) of mix that is in the source        
  ## labware at the start of the protocol.                                  
  
# What is the volume (µL) of mastermix that needs to be dispensed?
dispension_vol = 19.5   

# What labware are your primers in?
primer_tube_type = 'PCR_strips'
  ## Primers in strips = 'PCR_strips'                                       
  ## Primers in plate = 'plate_96'
if primer_tube_type == 'PCR_strips':
  # In which columns are the strips in the plate (ignore if not using strips)?
    primer_loc = ['1', '3', '5', '7', '9', '11']
      ## max 2 racks with strips!       
# What is the volume (µL) of primer that needs to be added to the mix?
primer_vol = 1.25           
   
# In what well should WALL-E start pipetting?
first_F_primer = 'A1'
first_R_primer = 'B1'         
# record this in the name of the protocol so that user knows which reverse 
# primer is added to his PCR
# =============================================================================
# IMPORTANT: this is only to be changed by the lab team

# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol  
# =============================================================================

# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                    
if simulate: #Simulator
    from mollab_modules import volume_tracking_v1 as vt
    import json 
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.     
else: #Robot
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
number_of_primers = number_of_samples + number_of_NTCs
  ## Calculate how many unique primer pairs are needed.                    
if mock:
    number_of_primers = number_of_primers + 1    
      ## If a mock is used, there should be 1 more unique primer pair.     
# =============================================================================

# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'general_illumina_PCR_WALL-E',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('Illumina (q)PCR - aliquoting mix and primers '),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting mastermix;
    Adding barcoded primers.
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    labwares = {}
      ## empty dict to add labware and labware_names to, to loop through
    # Pipette tips
    if dispension_vol >= 19:
      ## When the mm volume to be dispensed >= 19, 200µL tips are          
      ## needed in addition to the 20µL tips.                              
        tips_200 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', 
            8,                                  
            '200tips')                             
        if simulate:
            with open("labware/tipone_96_tiprack_20ul/"
                 "tipone_96_tiprack_20ul.json") as labware_file:
                      labware_def_tipone_20ul = json.load(labware_file)
            tips_20_1 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
                7,                         
                'tipone_20tips_1')
            tips_20_2 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
               10,                         
                'tipone_20tips_2')
        else:
            tips_20_1 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                7,                                  
                'tipone_20tips_1')                                
            tips_20_2 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                10,                                 
                'tipone_20tips_2')                         
        tips_20 = [tips_20_1, tips_20_2]
    else:
      ## When the mm volume to be dispensed <=19, only 20µL are needed      
        if simulate:
            with open("labware/tipone_96_tiprack_20ul/"
                 "tipone_96_tiprack_20ul.json") as labware_file:
                      labware_def_tipone_20ul = json.load(labware_file)
            
            tips_20_1 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
                2,                         
                'tipone_20tips_1')
            tips_20_2 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
                7,                         
                'tipone_20tips_2')
            tips_20_3 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
                10,                         
                'tipone_20tips_3')
        else:    
            tips_20_1 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                2,                                  
                'tipone_20tips_1')                           
            tips_20_2 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                7,                                  
                'tipone_20tips_2')                           
            tips_20_3 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                10,                                 
                'tipone_20tips_3')                             
            tips_20 = [tips_20_1, tips_20_2, tips_20_3]
   
    # Tube_racks & plates                                                     
    if simulate:
        with open("labware/biorad_qpcr_plate_nioz_plateholder/"
             "biorad_qpcr_plate_nioz_plateholder.json") as labware_file:
                  labware_def_plate_96_NIOZholder = json.load(labware_file)
        plate_96 = protocol.load_labware_from_definition( 
            labware_def_plate_96_NIOZholder,           
            5,                         
            'plate_96_NIOZholder')
    else:
        plate_96 = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',        
            5,                                      
            'plate_96_NIOZholder')
    if qPCR:
        big_primer_source = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            11,
            'big_primer_source')                           
    
    if mastermix_tube_type == 'tube_1.5mL':
        mastermix_tube = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            9,
            'mastermix_tube')      
    if primer_tube_type == 'plate_96':
        F_primer_source = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            4,                                  
            'F_primer_source')  
        labwares[F_primer_source] = 'plate_96'  
        R_primer_source = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',    
            6,                                  
            'R_primer_source')                    
                        
    if simulate: #Simulator
        if mastermix_tube_type == 'tube_5mL': 
            with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                      labware_def_5mL = json.load(labware_file)
            mastermix_tube = protocol.load_labware_from_definition( 
                labware_def_5mL,           
                9,                         
                'mastermix_tube')  
        if primer_tube_type == 'PCR_strips':
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                    labware_def_pcrstrips = json.load(labware_file)
            F_primer_source_1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                1,                         
                'F_primer_source_1')
            F_primer_source_2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                4,                         
                'F_primer_source_2')
            R_primer_source_1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                3,                         
                'R_primer_source_1')
            R_primer_source_2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,     
                6,                         
                'R_primer_source_2')
            

    else: #Robot
        if mastermix_tube_type == 'tube_5mL': 
            mastermix_tube = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',
                9,                                     
                'mastermix_tube')                                
        if primer_tube_type == 'PCR_strips':
            F_primer_source_1 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                1,                                     
                'F_primer_source_1')
            F_primer_source_2 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                4,                                     
                'F_primer_source_2')            
            R_primer_source_1 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                3,                                     
                'R_primer_source_1')
            R_primer_source_2 = protocol.load_labware( 
                'pcrstrips_96_wellplate_200ul',        
                6,                                     
                'R_primer_source_2')
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

# LABWARE OFFSET===============================================================    
# =============================================================================
    # if not simulate:
    #     for labware in labwares:
    #         offset_x = offsets.at[labwares[labware],'x_offset']
    #         offset_y = offsets.at[labwares[labware],'y_offset']
    #         offset_z = offsets.at[labwares[labware],'z_offset']
    #         labware.set_offset(
    #             x = offset_x, 
    #             y = offset_y, 
    #             z = offset_z)
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
    primer_mix_vol = primer_vol + 3
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
    MasterMix = mastermix_tube['A1']
    
    # Make a list with all wells MasterMix and primers should go                         
    wells = []
    for well in plate_96.wells():
        wells.append(well)
    
    # Create the list of wells where MM and primers should go
    sample_wells = wells[:number_of_primers]
      ## cuts off the list after the number_of_primers number of wells
    ## Remove wells to skip
    for index in sorted(primers_to_skip, reverse=True):
        del sample_wells[index]
        # In reverse order, so that the index does not shift
    
    # Create the list of wells where standard sample replicates should go
    slice_std_wells = slice(
        number_of_primers, number_of_primers + number_of_std_samples)
      ## Slice the list - I need the number_of_std_samples of wells after   
      ## the number_of_samples wells. So I need a certain amount of wells   
      ## after the sample wells, but not all of the wells after that.       
      ## This slices the list after the samples and after the std sample    
      ## so that we only take the wells in between.                         
    std_sample_wells = wells[slice_std_wells]

    # Create the list of wells where standerd series should go
    std_series_wells = [] 
    std_series_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in
         ['12', '11', '10']])
    std_series_columns = std_series_columns[:number_of_std_series]
    ## Reserve a column at the end of the plate for every std_series        
    ## Separate the columns into wells and append them to list              
    for column in std_series_columns:
        column = column[:length_std_series]
        ## cut off the columns after a certain std_series length            
        for well in column:
            std_series_wells.append(well)

    # Add the wells of the standards into 1 list 
      ## This needs to be a list separate from the rest of the wells because
      ## they need the same primer from a separate tube.                    
    std_wells = std_sample_wells + std_series_wells 
    # Add all the wells that need mastermix into 1 list
    MasterMixAliquots = sample_wells + std_wells
    
    
    # Primer location
    F_primer_wells = []
    F_primer_wells_string = []
      # The string list is needed to be able to start at a different well.
    R_primer_wells = []
    R_primer_wells_string = [] 
      # The string list is needed to be able to start at a different well.
      
    if primer_tube_type == 'PCR_strips':
        F_primer_columns = (
            ([F_primer_source_1.columns_by_name()[column_name] 
              for column_name in primer_loc])) + (
                  ([F_primer_source_2.columns_by_name()[column_name] 
                    for column_name in primer_loc]))
        for column in F_primer_columns:
            for well in column:
                F_primer_wells.append(well)
                F_primer_wells_string.append(str(well))
        R_primer_columns = (
            ([R_primer_source_1.columns_by_name()[column_name] 
              for column_name in primer_loc])) + (
                  ([R_primer_source_2.columns_by_name()[column_name] 
                    for column_name in primer_loc]))
        for column in R_primer_columns:
            for well in column:
                R_primer_wells.append(well)
                R_primer_wells_string.append(str(well))
                
    if primer_tube_type == 'plate_96':
        for well in F_primer_source.wells():
            F_primer_wells.append(well)
            F_primer_wells_string.append(str(well))
        for well in R_primer_source.wells():
            R_primer_wells.append(well)
            R_primer_wells_string.append(str(well))
    
    # Creating a list of primers, starting anywhere in the plate, making it
    # possible that after it reached the end of the plate, we start at the 
    # beginning again.
    # Indicate the index of the primer that should be the first.
    first_F_primer_index = F_primer_wells_string.index(
        first_F_primer + ' of F_primer_source_1 on 1')
    first_R_primer_index = R_primer_wells_string.index(
        first_R_primer + ' of R_primer_source_1 on 3')
    
    # Indicate the index of the first well in the plate.
    first_F_primer_on_plate_index = 0
    first_R_primer_on_plate_index = 0
    # Indicate the index of the last primer in the plate.
    last_F_primer_on_plate_index = 96
    last_R_primer_on_plate_index = 96
    
    # Create a list with wells from the primer that is indicated as the first
    # primer to the last well of the plate.
    slice_from_starting_F_primer_to_end = slice(
        first_F_primer_index, last_F_primer_on_plate_index)
    from_starting_F_primer_to_end = F_primer_wells[
        slice_from_starting_F_primer_to_end]
    slice_from_starting_R_primer_to_end = slice(
        first_R_primer_index, last_R_primer_on_plate_index)
    from_starting_R_primer_to_end = R_primer_wells[
        slice_from_starting_R_primer_to_end]
    # Create a list with wells from the first well of the plate to the 
    # primer that is indicated as the first.
    slice_from_start_to_starting_F_primer = slice(
        first_F_primer_on_plate_index, first_F_primer_index)
    from_start_to_starting_F_primer = F_primer_wells[
        slice_from_start_to_starting_F_primer]
    slice_from_start_to_starting_R_primer = slice(
        first_R_primer_on_plate_index, first_R_primer_index)
    from_start_to_starting_R_primer = R_primer_wells[
        slice_from_start_to_starting_R_primer]
    # Adding both lists to each other, so that we have a list of wells that 
    # starts at the well with indicated first primer and ends at the last 
    # well before that first primer.
    F_primers = from_starting_F_primer_to_end + from_start_to_starting_F_primer
    R_primers = from_starting_R_primer_to_end + from_start_to_starting_R_primer

    # Creating the list with wells for the amount of primer combinations that
    # are needed. WALL-E will start at the given first primer, and end after
    # the given number of primers were pipetted. WALL-E will start at the 
    # beginning of the primer plate if it needs to pipette more primers 
    # than remain after the given well.
    F_primer_wells = F_primers[:number_of_primers]
    R_primer_wells = R_primers[:number_of_primers]
    
    # Remove primers to skip
    for index in sorted(primers_to_skip, reverse=True):
        del F_primer_wells[index]
        del R_primer_wells[index]
    
    # Set location for primer for standards
    if number_of_std_samples >= 1:
        std_primer = big_primer_source.wells_by_name()[std_primer_loc]
# =============================================================================

## PIPETTING===================================================================
## ============================================================================
## LIGHTS----------------------------------------------------------------------
    if qPCR:
        protocol.set_rail_lights(False)
    if not qPCR:
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
    for primer_well, sample_well in zip(F_primer_wells, sample_wells):
      ## Loop trough primer_wells and sample_wells                          
        p20.pick_up_tip()
        p20.aspirate(primer_vol, primer_well)
        p20.dispense(primer_vol, sample_well)
        p20.mix(3, primer_mix_vol, sample_well)
        p20.dispense(10, sample_well)
        p20.drop_tip()    
## ----------------------------------------------------------------------------        
## ADDING R PRIMERS TO THE MIX-------------------------------------------------
    for primer_well, sample_well in zip(R_primer_wells, sample_wells):
      ## Loop trough primer_wells and sample_wells                          
        p20.pick_up_tip()
        p20.aspirate(primer_vol, primer_well)
        p20.dispense(primer_vol, sample_well)
        p20.mix(3, primer_mix_vol, sample_well)
        p20.dispense(10, sample_well)
        p20.drop_tip()      
## ----------------------------------------------------------------------------
## ADDING PRIMERS FOR STANDARDS TO THE MIX-------------------------------------
    for well in std_wells:
        p20.pick_up_tip()
        p20.aspirate(primer_vol, std_primer)
          ## use last primer pair for NTC and std series
        p20.dispense(primer_vol, well)
        p20.mix(3, primer_mix_vol, well)
        p20.dispense(10, well)
        p20.drop_tip()   
## ----------------------------------------------------------------------------
## LIGHTS----------------------------------------------------------------------
    if not qPCR:
        protocol.set_rail_lights(False)
# ----------------------------------------------------------------------------
## ============================================================================