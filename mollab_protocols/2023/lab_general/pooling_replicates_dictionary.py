"""
VERSION: V_Dec22
pooling_replicates.py is a protocol for pooling replicate PCR reactions.
It takes PCR product from 1 or 2 different locations and pools it in a third 
location.
This protocol assumes the 2 or 3 PCRs are done in the same labware
(either plate_96, non_skirted_plate_96 or PCR_strips), and the placement of 
samples is the exact same for all 3.
It is however possible to skip certain reactions.

You have to provide:
    Location of the starting tip in P20 or P200 (depending on the PCR
        reaction volume x 2 + airgap)
    Location of first sample in the plate
    Location of last sample in the plate
    List with specific sample locations to skip
    PCR reaction volume
    Number of replicates

221206 MB:  -added the option for non-skirted plates and PCR strips
            -removed off-set stuff
            -tip_one 20uL tips + 300uL tips outcommented but ready
            -moved the slice for first and last well into the if skipp_samples loop
"""

# VARIABLES TO SET#!!!=========================================================
# =============================================================================
# What is the starting position of the tips?
starting_tip = 'A1'
  ## Either p20 or p200 or p300. 
  ## You need the tips that fit PCR reaction volume x (number of replicates -1)
  ## + 1µL extra per (number of replicate -1)

# What kind of tubes are your replicates in?
sample_tube_type = 'non_skirted_plate_96'
  ## options: 'plate_96', 'non_skirted_plate_96', 'PCR_strips'
  ## max 1 rack per PCR 
# In which columns are the strips in the plate (ignored if not using strips)?
sample_columns = ['2', '5', '8','11']
  ## optional: ['2', '7', '11'] or ['2', '5', '8','11']                     
   
# Are there any wells between the first and last sample that need to be skipped
skipp_samples = False
  ## The following skipped wells will only be used when skipp_samples = True
# What is the location of the first and last sample you want to pool
first_sample_well = 'A1'
  ## If you want to skip the first couple of samples, please indicate the 
  ## location in the plates of the first sample you want to pool.
last_sample_well = 'H12'
  ## If you want to skip the last couple of samples, or your PCR plates are not 
  ## completely filled, please indicate the location in the plates of the last
  ## sample you want to pool.
# Are there any other samples that you want to skip?
skipped_wells = ([])
    ## Fill in the wells that need to be skipped while pooling
    ## If you don't want to skip, set an empty list: skipped_wells = ([])
    
# What is the PCR reaction_volume (per reaction)?
reaction_volume = 20

# How many replicates do you have?
replicates = 3
  ## How many reactions do you want to pool, including the original PCR?
  ## For now 3 is max. If you want more, protocol needs to be adjusted

# Do you want to simulate the protocol?
simulate = False
  ## True for simulating protocol, False for robot protocol 
# =============================================================================

# IMPORT STATEMENTS AND FILES==================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.
if simulate: #Simulator
    import json 
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.   
# =============================================================================

# CALCULATED VARIABLES=========================================================
# =============================================================================
# What volume needs to be aspirated (all replicates combined + airgaps of 5µL)
transfer_volume = (reaction_volume * (replicates -1)) + ((replicates -1) * 5)
# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'pooling_replicates.py',
    'author': 'MB <maartje.brouwer@nioz.nl>',
    'description': ('pooling replicates after replicate PCRs'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    pooling replicate PCR reactions into one of the reaction tubes
    
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    ##### Loading pipettetips
    if simulate:
        # with open("labware/tipone_96_tiprack_300ul/"
        #      "tipone_96_tiprack_300ul.json") as labware_file:
        #           labware_def_tipone_300ul = json.load(labware_file)
        with open("labware/tipone_96_tiprack_20ul/"
             "tipone_96_tiprack_20ul.json") as labware_file:
                  labware_def_tipone_20ul = json.load(labware_file)
        
        if transfer_volume > 20:
            # tips_1 = protocol.load_labware_from_definition( 
            #     labware_def_tipone_300ul,           
            #     11,                         
            #     'tipone_300tips_1')
            # tips_2 = protocol.load_labware_from_definition( 
            #     labware_def_tipone_300ul,           
            #     10,                         
            #     'tipone_300tips_2')
            tips_1 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',  
                11,                                  
                '200tips_1')
            tips_2 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',  
                10,                                  
                '200tips_2')
        else: 
            tips_1 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
                11,                         
                'tipone_20tips_1')
            tips_2 = protocol.load_labware_from_definition( 
                labware_def_tipone_20ul,           
                10,                         
                'tipone_20tips_2')
            
    else:
        if transfer_volume > 20:
            tips_1 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',  
                11,                                  
                '200tips_1')
            tips_2 = protocol.load_labware(
                'opentrons_96_filtertiprack_200ul',  
                10,                                  
                '200tips_2')
            # tips_1 = protocol.load_labware(
            #     'tipone_96_tiprack_300ul',  
            #     11,                                  
            #     'tipone_300tips_1')
            # tips_2 = protocol.load_labware(
            #     'tipone_96_tiprack_300ul',  
            #     10,                                  
            #     'tipone_300tips_2')
        else:    
            tips_1 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                11,                                  
                'tipone_20tips_1')
            tips_2 = protocol.load_labware(
                'tipone_96_tiprack_20ul',  
                10,                                  
                'tipone_20tips_2')
        
    ##### Loading labware
    if sample_tube_type == 'plate_96':
        PCR1 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            9,
            'PCR1_plate_96')
    
        PCR2 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            8,
            'PCR2_plate_96')
        if replicates > 2:
            PCR3 = protocol.load_labware(
                'biorad_96_wellplate_200ul_pcr',
                7,
                'PCR3_plate_96')
    
    if sample_tube_type == 'non_skirted_plate_96':
        if simulate:
            with open("labware/thermononskirtedinbioradskirted_96_wellplate_200ul/"
                 "thermononskirtedinbioradskirted_96_wellplate_200ul.json") as labware_file:
                      labware_def_non_skirted_plate_96 = json.load(labware_file)
            PCR1 = protocol.load_labware_from_definition( 
                labware_def_non_skirted_plate_96,           
                9,                         
                'PCR1_non_skirted_plate_96')
            PCR2 = protocol.load_labware_from_definition( 
                labware_def_non_skirted_plate_96,           
                8,                         
                'PCR2_non_skirted_plate_96')
            if replicates > 2:
                PCR3 = protocol.load_labware_from_definition( 
                    labware_def_non_skirted_plate_96,           
                    7,                         
                    'PCR3_non_skirted_plate_96')
                
        else:
            PCR1 = protocol.load_labware(
                'thermononskirtedinbioradskirted_96_wellplate_200ul',        
                9,                                      
                'PCR1_non_skirted_plate_96')
            PCR2 = protocol.load_labware(
                'thermononskirtedinbioradskirted_96_wellplate_200ul',        
                8,                                      
                'PCR2_non_skirted_plate_96')
            if replicates > 2:
                PCR3 = protocol.load_labware(
                    'thermononskirtedinbioradskirted_96_wellplate_200ul',        
                    7,                                      
                    'PCR3_non_skirted_plate_96')
    
    if sample_tube_type == 'PCR_strips':
        if simulate:
            with open("labware/pcrstrips_96_wellplate_200ul/"
                      "pcrstrips_96_wellplate_200ul.json") as labware_file:
                      labware_def_pcrstrips = json.load(labware_file)
            PCR1 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,           
                9,                         
                'PCR1_PCR_strips')
            PCR2 = protocol.load_labware_from_definition( 
                labware_def_pcrstrips,           
                8,                         
                'PCR2_PCR_strips')
            if replicates > 2:
                PCR3 = protocol.load_labware_from_definition( 
                    labware_def_pcrstrips,           
                    7,                         
                    'PCR3_PCR_strips')
                
        else:
            PCR1 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',        
                9,                                      
                'PCR1_PCR_strips')
            PCR2 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',        
                8,                                      
                'PCR2_non_skirted')
            if replicates > 2:
                PCR3 = protocol.load_labware(
                    'pcrstrips_96_wellplate_200ul',        
                    7,                                      
                    'PCR3_PCR_strips')

    ##### Loading pipettes
    if transfer_volume >= 20:
        pipette = protocol.load_instrument(
            'p300_single_gen2',             
            'right',                        
            tip_racks=[tips_1, tips_2])
    else:
        pipette = protocol.load_instrument(
            'p20_single_gen2',                  
            'left',                             
            tip_racks=[tips_1, tips_2])    
# =============================================================================

# SETTING LOCATIONS============================================================
# =============================================================================
    # Setting starting tip
    pipette.starting_tip = tips_1.well(starting_tip)
    
    # Make lists with all wells of the PCR plates
    if sample_tube_type == 'PCR_strips':
        PCR1_columns = (
                ([PCR1.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
        PCR1_wells = []
        for column in PCR1_columns:
            for well in column:
                PCR1_wells.append(well)
        PCR2_columns = (
                ([PCR2.columns_by_name()[column_name] 
                  for column_name in sample_columns]))
        PCR2_wells = []
        for column in PCR2_columns:
            for well in column:
                PCR2_wells.append(well)
        if replicates > 2:
            PCR3_columns = (
                    ([PCR3.columns_by_name()[column_name] 
                      for column_name in sample_columns]))
            PCR3_wells = []
            for column in PCR3_columns:
                for well in column:
                    PCR3_wells.append(well)
    else:    
        PCR1_wells = PCR1.wells()
        PCR2_wells = PCR2.wells()
        if replicates > 2:
            PCR3_wells = PCR3.wells()

    if skipp_samples:
    # skipp wells at start and end
        # Get indexes for wells to skip
        PCR1_wells_string = []
          ## Make an empty list to append well_names (string) to
        for well in PCR1_wells:
            PCR1_wells_string.append(str(well))  
        # Get indexes of first and last wells
        first_well_index = PCR1_wells_string.index(
            first_sample_well + ' of PCR1_' + sample_tube_type + ' on 9')
        last_well_index = PCR1_wells_string.index(
            last_sample_well + ' of PCR1_' + sample_tube_type + ' on 9')
        # Slice list with wells at first and after last well (+1)
        PCR1_wells = PCR1_wells[slice(first_well_index, last_well_index +1)]
        PCR2_wells = PCR2_wells[slice(first_well_index, last_well_index +1)]
        if replicates > 2:
            PCR3_wells = PCR3_wells[slice(first_well_index, last_well_index +1)]
    
    # Skip wells in the middle    
        # Get new list to get indexes for wells to skip
        PCR1_wells_string = []
          ## Make an empty list to append well_names (string) to
        for well in PCR1_wells:
            PCR1_wells_string.append(str(well))    
        # Get indexes for the different wells
        counter = -1
        for well in skipped_wells:
            counter = counter + 1
            skipped_well_index = PCR1_wells_string.index(
                well + ' of PCR1_' + sample_tube_type + ' on 9')
            # pop the to be skipped wells from the lists
            PCR1_wells.pop(skipped_well_index - counter)
            PCR2_wells.pop(skipped_well_index - counter)
            if replicates > 2:
                PCR3_wells.pop(skipped_well_index - counter)
# =============================================================================

## PIPETTING===================================================================
## ============================================================================
    # Turn on lights    
    protocol.set_rail_lights(True)
    
    if replicates == 2:
        for well_PCR2, well_PCR1 in zip(PCR2_wells, PCR1_wells):
            pipette.pick_up_tip()
            pipette.aspirate(transfer_volume, well_PCR2)
            pipette.dispense(transfer_volume, well_PCR1)
            pipette.dispense(10, well_PCR1)
            pipette.drop_tip()
    
    if replicates == 3:
        for well_PCR3, well_PCR2, well_PCR1 in zip(
                PCR3_wells, PCR2_wells, PCR1_wells):
            pipette.pick_up_tip()
            pipette.aspirate(reaction_volume + 5, well_PCR3)
            pipette.aspirate(reaction_volume + 5, well_PCR2)
            pipette.dispense(transfer_volume, well_PCR1)
            pipette.dispense(10, well_PCR1)
            pipette.drop_tip()        
# =============================================================================

# TURN RAIL LIGHT OFF==========================================================
# =============================================================================
    protocol.set_rail_lights(False)   
# =============================================================================

    
    
    
    
    