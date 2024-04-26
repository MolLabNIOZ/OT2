"""
version: Jan_2024
"""

def loading_pipettes(P20, 
                     tips_20,
                     starting_tip_p20,
                     P300, 
                     tips_300,
                     starting_tip_p300,
                     protocol):
    """    
    Parameters
    ----------
    P20 : boolean True or False
        Is the p20 used in the protocol or not
    tips_20 : labware, a list with loaded tip racks
        Pass the result of loading_tips()
    P300 : boolean True or False
        Is the p300 used in the protocol or not
    tips_300 : labware, a list with loaded tip racks
        Pass the result of loading_tips()
    protocol : def run(protocol: protocol_api.ProtocolContext):

    Returns
    -------
    p20 : labware
    p300 : labware
    """

    if P20:
        p20 = protocol.load_instrument('p20_single_gen2',
                                       'left',
                                       tip_racks=tips_20)
        p20.starting_tip = tips_20[0].well(starting_tip_p20)
    
    else: 
        p20 = False
    
    if P300:
        p300 = protocol.load_instrument('p300_single_gen2',
                                        'right',
                                        tip_racks=tips_300)
        p300.starting_tip = tips_300[0].well(starting_tip_p300)
        
    else:
        p300 = False     
    
    return p20, p300

#=============================================================================

def loading_tips(simulate, 
                 tip_type, 
                 amount, 
                 deck_positions, 
                 protocol):
    """   
    Parameters
    ----------
    simulate : boolean True or False
        Are you simulating the protocol or running it on the robot?
    tip_type : brand / size
        opentrons_20uL / tipone_20uL / opentrons_200uL / tipone_300uL
    amount : int
        How many racks of this type do you want to load?
    deck_positions : list
        Where do you want the tip_racks to be located on the deck
    protocol : def run(protocol: protocol_api.ProtocolContext):

    Returns
    -------
    tip_racks : list of labware
        List with all tip racks for one of the pipettes
    """
    labware_dict = {
            'opentrons_20uL':
                ['opentrons_96_filtertiprack_20ul',
                 'noncustom'],
            'tipone_20uL': 
                ['tipone_96_tiprack_20ul',
                 'custom'],
            'opentrons_200uL': 
                ['opentrons_96_filtertiprack_200ul', 
                 'noncustom'],
            'tipone_300uL': 
                ['tipone_96_tiprack_300ul',
                 'custom'],
            }
    
    tip_racks = []
    
    for i in range(amount):
        rack_name = f"{tip_type}_{i + 1}"
        
        if simulate and labware_dict[tip_type][1] == 'custom':
            import json
            with open(
                    f"labware/"
                    f"{labware_dict[tip_type][0]}/"
                    f"{labware_dict[tip_type][0]}.json") as labware_file:
                labware = json.load(labware_file)
            tip_rack = protocol.load_labware_from_definition( 
                labware, 
                deck_positions[i],                    
                rack_name)
        else:
            tip_rack = protocol.load_labware(
                labware_dict[tip_type][0], 
                deck_positions[i], 
                rack_name)
         
    
        tip_racks.append(tip_rack)

    return tip_racks
        
#==============================================================================
   
def loading_tube_racks(simulate, 
                       tube_type, 
                       reagent_type, 
                       amount, 
                       deck_positions, 
                       protocol):
    """
    Parameters
    ----------
    simulate : boolean True or False
        Are you simulating the protocol or running it on the robot?
    tube_type : type of tube to be loaded
        skirted_plate_96 / plate_96_NIOZholder / non_skirted_plate_96 /
        PCR_strips / 1.5mL_tubes / 5mL_screwcap_tubes / 5mL_snapcap_tubes /
        15mL_tubes / 50mL_tubes
    reagent_type : string
        will be included in deck set-up for conveniance
    amount : int
        How many racks of this specific type should be loaded?
    deck_positions : list
        Where do you want these racks located on the deck
    protocol : def run(protocol: protocol_api.ProtocolContext):

    Returns
    -------
    tube_racks : list of labware
        List with all tube racks for this specific type

    """
      
    labware_dict = {
            'skirted_plate_96':
                ['biorad_96_wellplate_200ul_pcr',
                 'noncustom'],
            'plate_96_NIOZholder': 
                ['biorad_qPCR_plate_nioz_plateholder',
                 'custom'],
            'non_skirted_plate_96': 
                ['thermononskirtedinbioradskirted_96_wellplate_200ul',
                 'custom'],
            'PCR_strips': 
                ['pcrstrips_96_wellplate_200ul',
                 'custom'],
            '1.5mL_tubes': 
                ['opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 
                 'noncustom'],
            '5mL_screwcap_tubes': 
                ['eppendorfscrewcap_15_tuberack_5000ul',
                 'custom'],
            '5mL_snapcap_tubes': 
                ['eppendorf_15_tuberack_5000ul',
                 'custom'],
            '15mL_tubes': 
                ['opentrons_15_tuberack_falcon_15ml_conical',
                 'noncustom'],
            '50mL_tubes': 
                ['opentrons_6_tuberack_falcon_50ml_conical',
                 'noncustom']
            }
    
    tube_racks = []
    
    for i in range(amount):
        rack_name = f"{reagent_type}_{tube_type}_{i + 1}"
        
        if simulate and labware_dict[tube_type][1] == 'custom':
            import json
            with open(
                    f"labware/"
                    f"{labware_dict[tube_type][0]}/"
                    f"{labware_dict[tube_type][0]}.json") as labware_file:
                labware = json.load(labware_file)
            tube_rack = protocol.load_labware_from_definition( 
                labware, 
                deck_positions[i],                    
                rack_name)
        else:
            tube_rack = protocol.load_labware(
                labware_dict[tube_type][0], 
                deck_positions[i], 
                rack_name)
         
    
        tube_racks.append(tube_rack)
        
    return tube_racks
        
def tube_locations(source_racks,
                   specific_columns,
                   skip_wells,
                   number_of_tubes):
    """
    Parameters
    ----------
    source_racks : list
        List with all loaded tube_racks for this reagent
    specific_columns : False or list with column numbers
        PCR strips are only located in specific columns of a plate_96
    skip_wells : False or list with indexes
        List with indexes of wells to skip
    number_of_tubes : int
        How many tubes/wells are used for this specific type
    
    Returns
    -------
    tubes : list of tube locations
        List with all tubes for this specific type
        

    """
    #### Make an empty list to append tubes/wells to
    tubes = []
    
    #### Append all wells from all racks to the list
    if not specific_columns:
        for rack in source_racks:
            for tube in rack.wells():
                tubes.append(tube)
    
    else: # if specific_columns
        ## Separate racks into specified columns
        for rack in source_racks:
            rack_columns = (
                [rack.columns_by_name()[column]
                for column in specific_columns])
            ## Separate columns into wells and add wells to list
            for column in rack_columns:
                for well in column:
                    tubes.append(well)

    #### Remove tubes/wells to skip
    if skip_wells:
        for index in sorted(skip_wells, reverse=True):
            del tubes[index]
            # In reverse order, so that the index does not shift

    #### Cut off the list, after a specified number of tubes/wells    
    tubes = tubes[:number_of_tubes]                           
   
    return tubes   

def which_tube_type(total_volume, tube_type):
    """
    depending on total_volume a specific tube is necesarry  

    Parameters
    ----------
    total_volume : float
        total_volume in µL
    tube_type : Boolean False or string
        If you want the protocol to recommend a tube_type, put False
        If you want to know how many of a specific tube_type you need put
        the desired tube type string.
        Optional: 

    Returns
    -------
    tube_type: string with name of labware
    number_of_tubes: int, how many tubes should be used
    max_volume: float, how much reagent fits max in this specific type of tube
    """
    #### Import math module to allow rounding up
    import math

    #### How much volume can a tube hold?
    tube_dict = {'1.5mL_tubes'          : 1500,
                 '5mL_screwcap_tubes'   : 5000,
                 '15mL_tubes'           : 15000,
                 '50mL_tubes'           : 50000
                 }    
    
    if not tube_type:
        for key, value in tube_dict.items():
            if value >= total_volume:
                tube_type = key
                break
            tube_type = '50mL_tubes'
    
    max_volume = tube_dict[tube_type]
    number_of_tubes = math.ceil((total_volume)/max_volume)

                    
    return tube_type, number_of_tubes, max_volume

#=============================================================================

def number_of_racks(number_of_tubes, tube_type, strip_columns):
    """
    Parameters
    ----------
    number_of_tubes : int
    tube_type : TYPE
        Optional: skirted_plate_96 / plate_96_NIOZholder / non_skirted_plate_96 
        PCR_strips / 1.5mL_tubes
    strip_columns: Boolean False or list
        Only used with tube_type PCR_strips, to determine how many tubes strips
        are placed in 1 rack
    Returns
    -------
    number_of_racks

    """
    #### Import math module to allow rounding up
    import math
    
    #### How many tubes fit a rack of this tube_type
    rack_dict = {'skirted_plate_96' 
                 'plate_96_NIOZholder'
                 'non_skirted_plate_96'
                 'PCR_strips'
                 '1.5mL_tubes'
                 }

#=============================================================================    
def number_of_pipette_racks(starting_tip_p20,
                  starting_tip_p200,
                  tips_needed_p20,
                  tips_needed_p200):
    """
    Parameters
    ----------
    starting_tip_p20 : tuble with a well 'coordinate'.
    starting_tip_p200 : tuble with a well 'coordinate'.
    tips_needed_p20 : amount of tips needed for the P20 pipette. This needs to
        be calculated in the protocol.
    tips_needed_p200 :amount of tips needed for the P200 pipette. This needs 
        to be calculated in the protocol.
    Returns
    -------
    amount_tip_racks_p20  : number
    amount_tip_racks_p200 : number
    """
    
    # Generate rack positions from A1 to H12
    rack = [f"{chr(65 + i)}{j}" for i in range(8) for j in range(1, 13)]
    
    # Imports math
    import math
    if starting_tip_p20:
        
        # Calculate the total number of racks needed to hold the specified number of tips
        amount_tip_racks_p20 = math.ceil((tips_needed_p20 - (96 - rack.index(starting_tip_p20))) / 96) + 1
    # If there is no     
    else:
        amount_tip_racks_p20 = 0
    
    if starting_tip_p200:
        
        # Calculate the total number of racks needed to hold the specified number of tips
        amount_tip_racks_p200 = math.ceil((tips_needed_p200 - (96 - rack.index(starting_tip_p200))) / 96) + 1
    
    else:
        amount_tip_racks_p200 = 0
    
    return amount_tip_racks_p20, amount_tip_racks_p200

#=============================================================================

def amount_of_single_pipette_tips_needed(reagent_volume,
                 sample_volume,
                 number_of_reactions,
                 number_of_repeats_sample_pipetting):
    """
    Parameters
    ----------
    reagent_volume : Could be a list or a iterable. Are the volume(s) aliquoted
        for the mastermix/water/other reagents.
    sample_volume : Could be a list or a iterable. Are the volume(s) transfered
        for the samples/primers/other things.
    number_of_reactions : A iterable of the amount of reactions are performed
    repeat_of_sample_pipetting : A iterable. This number represents the number
        of replicates of the samples (example: if you add barcoded primers,
        you pipette forward and reverse primers with the same variable.
        Therefore the variable 'number_of_repeats_sample_pipetting' = 2)
    
    Returns
    -------
    p20_tips_needed : number of single p20 pipette tips used for the run
    p200_tips_needed : number of single p200 pipette tips used for the run
    """
    import math
    
    # Checks whether or not the variable reagent_volume is a lost or not
    if isinstance(reagent_volume,list):  
        p20_tips_needed_reagent = 0 # Creates a counter to count the tips needed for the reagents pipetted with the p20
        p200_tips_needed_reagent = 0 # Creates a counter to count the tips needed for the reagents pipetted with the p200
        
        # Creates a for loop to go through the list of reagent_volume and counts
        # with which pipette it will be transferred and adds 1 to the variables above.
        for value in reagent_volume: 
            if 0.001 < value <= 19:
                p20_tips_needed_reagent += 1
            elif value > 19:
                p200_tips_needed_reagent += 1
            else: pass
    else:
        reagent_volume_list = [reagent_volume] # Creates a list of the single iterable
        for value in reagent_volume_list:
            if 0.001 < reagent_volume <= 19: # Checks if the desired volume is between 0.001 and 19
                p20_tips_needed_reagent = number_of_reactions 
                p200_tips_needed_reagent = 0
            elif reagent_volume > 19: # Checks if the desired volume is bigger than 19
                p200_tips_needed_reagent = number_of_reactions
                p20_tips_needed_reagent = 0
            else: pass
    
    # Checks whether or not the variable reagent_volume is a lost or not 
    if isinstance(sample_volume,list):
        p20_tips_needed_sample = 0 # Creates a counter to count the tips needed for the samples pipetted with the p20
        p200_tips_needed_sample = 0 # Creates a counter to count the tips needed for the samples pipetted with the p200
       
        # Creates a for loop to go through the list of sample_volume and counts
        # with which pipette it will be transferred and adds 1 to the variables above.
        for value in sample_volume: 
            if 0.001 < value <= 15:
                p20_tips_needed_sample += 1
            elif value > 15:
                p200_tips_needed_sample += 1
            else: pass
    else:
        sample_volume_list = [sample_volume] # Creates a list of the single iterable
        for value in sample_volume_list:
            if 0.001 < sample_volume <= 19: # Checks if the desired volume is between 0.001 and 19
                p20_tips_needed_sample = math.ceil(number_of_reactions*number_of_repeats_sample_pipetting) # Multiplies the number of reactions by the number of repeats
                p200_tips_needed_sample = 0
            elif sample_volume > 19:
                p200_tips_needed_sample = math.ceil(number_of_reactions*number_of_repeats_sample_pipetting) # Multiplies the number of reactions by the number of repeats
                p20_tips_needed_sample = 0
            else: pass
    # Calculates the tips needed by deviding the number of tips needed for the reagents by 16 (and rounding up) + the tips needed for the transfering of the samples.
    p20_tips_needed = ((math.ceil(p20_tips_needed_reagent/16)) + p20_tips_needed_sample)
    p200_tips_needed = ((math.ceil(p200_tips_needed_reagent/16)) + p200_tips_needed_sample)

    return p20_tips_needed,p200_tips_needed