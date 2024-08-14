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
            'plateholder_skirted_plate': 
                ['biorad_qpcr_plate_nioz_plateholder',
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
        rack_name = f"{i + 1}_{reagent_type}_{tube_type}"
        
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

def defining_liquids(reagent_type, 
                     protocol):
    """
    Parameters
    ----------
    reagent_type: 
        Discribe the reagent type. See reagent_dict in defining_liquids for the
        options.
    volume: int
        What is the volume that is present in the tube? If this is not clear,
        put in '1'
     protocol : def run(protocol: protocol_api.ProtocolContext):
         
    Returns
    -------
    liquid: 
        A defined liquid with a certain color from the dictonary.
    
    """
    
    reagent_dict = {
        'mastermix': ['Mastermix', 'Mastermix tube', '#FF0000'],
        'forward_primer': ['Forward Primers', 'Forward primer strips', '#00FF00'],
        'reverse_primer': ['Reverse Primers', 'Revers primer strips', '#00F3FF'],
        'primer_stocks': ['Primer stocks', 'The pcr strips containing the barcoded primer stocks','#800080'],
        'primer_working_dilution': ['Primer working dilution', 'The pcr strips containing the barcoded primer working dilution','#DD8AFF'],
        'first_primer': ['First Primer', 'The primer that will be assigned to the first sample','#FF0000'],
        'samples': ['Samples', 'The samples in the strips/tubes','#FF00FF'],
        'standard_samples': ['Standard samples', 'The samples used in the SVEC methode for normalization','#893EAE'],
        'dilution_series': ['Dilution serie samples', 'The samples used for the dilution serie','#00FF00'],
        'water': ['Water', 'Tube containing water','#0000FF'],
        'tapestation_buffer': ['Tapestation Buffer', 'Tube containing Tapestation buffer','#A52A2A'],
        'tapestation_sample': ['Tapestation Sample', 'Destination plate containing the Tapestation buffer and your sample','#1FB960'],
        'NTC': ['NTC', 'Reaction without template volume','#FF0000'],
        'Mock': ['MOCK', 'The tube containing your MOCK','#239B56'],
        'destination': ['Destination', 'This tubes/wells contains a mix of liquids, these are the destination tubes/wells of this protocol','#A52A2A'],
        'PB-buffer': ['PB buffer', 'The tube with the starting amount of PB-buffer for the equimolar pooling','#FFC500'],
        'Qmix': ['Qubit mix', 'The tube with the starting amount of Qubit mix','#FFDC00'],
        'other': ['Other', 'remaining liquids','#000000'],
        }
    
    liquid = protocol.define_liquid(
               name= reagent_dict[reagent_type][0],
               description= reagent_dict[reagent_type][1],
               display_color= reagent_dict[reagent_type][2],
               )
    
    return liquid

def tube_locations(source_racks,
                   specific_columns,
                   skip_wells,
                   number_of_tubes,
                   reagent_type,
                   volume,
                   protocol):
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
    reagent_type: 
        Discribe the reagent type. See reagent_dict in defining_liquids for the
        options.
    volume: int
        What is the volume that is present in the tube? If this is not clear,
        put in '1'
     protocol : def run(protocol: protocol_api.ProtocolContext):
        
    
    Returns
    -------
    tubes : list of tube locations
        List with all tubes for this specific type with the color defined with
        the function defining_liquids

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
    
    liquid = defining_liquids(reagent_type, protocol)
    
    for well in tubes:
        well.load_liquid(liquid, volume)
        
    return tubes

def multiple_tube_locations(source_racks,
                            specific_columns,
                            skip_wells,
                            amount_dict,
                            volume,
                            protocol):
    """
    Parameters
    ----------
    source_racks : list
        List with all loaded tube_racks for this reagent
    specific_columns : False or list with column numbers
        PCR strips are only located in specific columns of a plate_96
    skip_wells : False or list with indexes
        List with indexes of wells to skip
    amount_dict: dict
        Dict containing the names of the liquids, see reagent_dict in 
        defining_liquids for the options and the numbers of how many times it 
        is present in the rack.
    volume: int
        What is the volume that is present in the tube? If this is not clear,
        put in '1'
     protocol : def run(protocol: protocol_api.ProtocolContext):
        
    
    Returns
    -------
    tubes : list of tube locations
        List with all tubes for this specific type with the color defined with
        the function defining_liquids

    """

    #### Make an empty list to append tubes/wells to
    total_tubes = []
    
    #### Append all wells from all racks to the list
    if not specific_columns:
        for rack in source_racks:
            for tube in rack.wells():
                total_tubes.append(tube)
    
    else: # if specific_columns
        ## Separate racks into specified columns
        for rack in source_racks:
            rack_columns = (
                [rack.columns_by_name()[column]
                for column in specific_columns])
            ## Separate columns into wells and add wells to list
            for column in rack_columns:
                for well in column:
                    total_tubes.append(well)
    
    #### Remove total_tubes/wells to skip
    if skip_wells:
        for index in sorted(skip_wells, reverse=True):
            del total_tubes[index]
            # In reverse order, so that the index does not shift

                   
    # Creates a new list. This will be the variable that is used for the return value
    return_list = []    

    # For-loop to iterate through the dict. In the loop the following will happen
    for reagent, number in amount_dict.items():
        # Creates a variable depending on the amount of reactions
        tubes_reagent = (total_tubes[slice(number)])
        return_list.append(tubes_reagent)
        
        # Calls function definging_liquids depending on the reagent in the dict
        # It will save the color under liquid
        liquid = defining_liquids(reagent, protocol)
        
        # Paints every liquid the right color
        for well in tubes_reagent:
            well.load_liquid(liquid, volume)
        
        # Deletes the used wells from the list
        total_tubes = total_tubes[number:]
    
    return return_list


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

# def number_of_racks(number_of_tubes, tube_type, strip_columns):
#     """
#     Parameters
#     ----------
#     number_of_tubes : int
#     tube_type : TYPE
#         Optional: skirted_plate_96 / plate_96_NIOZholder / non_skirted_plate_96 
#         PCR_strips / 1.5mL_tubes
#     strip_columns: Boolean False or list
#         Only used with tube_type PCR_strips, to determine how many tubes strips
#         are placed in 1 rack
    
#     Returns
#     -------
#     number_of_racks

#     """
#     #### Import math module to allow rounding up
#     import math
    
#     #### How many tubes fit a rack of this tube_type
#     rack_dict = {'skirted_plate_96' 
#                  'plate_96_NIOZholder'
#                  'non_skirted_plate_96'
#                  'PCR_strips'
#                  '1.5mL_tubes'
#                  }

#=============================================================================    
def number_of_tipracks(starting_tip,
                       tips_needed):
    """
    Parameters
    ----------
    starting_tip : string with a well coordinate, e.g, 'A1'.
    tips_needed : amount of tips needed for the specific pipette. 
    
    Returns
    -------
    amount_tip_racks  : int
    """
    #### Imports math
    import math
    
    #### Generate list with all possible coordinates in a rack (A1 to H12)
    rack = [f"{chr(65 + i)}{j}" for j in range(1, 13) for i in range(8)]

    #### Calculate how many racks are needed
    amount_tip_racks = math.ceil((tips_needed - (96 - rack.index(starting_tip))) / 96) + 1
    
    if amount_tip_racks > 0:
        pipette = True
    else:
        pipette = False

    #### Return
    return amount_tip_racks, pipette

#=============================================================================

def amount_of_tips(volumes,
                   number_of_transfers,
                   tip_change,
                   max_p20_volume):
    """
    Parameters
    ----------
   volumes : float or list of floats
        The volume(s) to be aliquoted or transfered
    number_of_transfers : int
        How many pipetting actions will be performed will be made
    tip_change : int
        After how many transfers do you want to change the tip?
    max_p20_volume: float
        What is the maximum volume that the p20 can handle? This depends on 
        optional airgap and mix_volume
    
    Returns
    -------
    p20_tips_needed : number of single p20 pipette tips used
    p300_tips_needed : number of single p300 pipette tips used
    """
    #### Imports math
    import math
    
    ### Make 2 counters
    p20_tips_needed = 0
    p300_tips_needed = 0
    
    ### Check whether it's a list or a single int
    if isinstance(volumes,list):
        ## Make 2 counters

        # Creates a for loop to go through the list of volumes
        # Count up specific pipette use
        for value in volumes: 
            if 0 < value <= max_p20_volume:
                p20_tips_needed += 1
            elif value > max_p20_volume:
                p300_tips_needed += 1

    else:
        if 0 < volumes <= max_p20_volume: # Checks if the desired volume is between 0.001 and 19
            p20_tips_needed = number_of_transfers 

        elif volumes > max_p20_volume: # Checks if the desired volume is bigger than 19
            p300_tips_needed = number_of_transfers
    

    # Calculates the tips needed by deviding the number of tips needed for the reagents by 16 (and rounding up) + the tips needed for the transfering of the samples.
    p20_tips_needed = math.ceil(p20_tips_needed/tip_change)
    p300_tips_needed = math.ceil(p300_tips_needed/tip_change)
    
    return p20_tips_needed , p300_tips_needed

#=============================================================================

def number_of_tip_racks_2_0(volumes_aliquoting,
                            number_of_aliquotes,
                            volumes_transfering,
                            number_of_transfers,
                            starting_tip_p20,
                            starting_tip_p300):
    """
    Parameters
    ----------
    volumes_aliquoting : False, list or single number
        The volume(s) to be aliquoted. If this is not used, set False
    number_of_aliquotes : int
        Number of pipette actions will be performed for aliquoting
    volumes_transfering : False, list or single number
        The volume(s) to be transfered. If this is not used, set False
    number_of_transfers : int
        Number of pipette actions will be performed for transfering
    starting_tip_p20 : string
        Well coordinate of the starting tip for the p20 pipette, e.g, 'A1'
    starting_tip_p300 : string
        Well coordinate of the starting tip for the p300 pipette, e.g, 'A1'
   
    Returns
    -------
    tip_racks_p20 : int
        Number of tip racks for the p20 tips
    tip_racks_p300 : int
        Number of tip racks for the p300 tips
    P20 : Boolean
        True or False, it will be True if there are any pipette racks needed,
        else it will be False.
    P300 : Boolean
        True or False, it will be True if there are any pipette racks needed,
        else it will be False.
    """

    if volumes_aliquoting:
        tips_aliquoting = amount_of_tips(volumes = volumes_aliquoting,
                                         number_of_transfers = number_of_aliquotes,
                                         tip_change = 16,
                                         max_p20_volume = 19)
                
    else:
        tips_aliquoting = (0,0)
    
    if volumes_transfering:
        tips_transfering = amount_of_tips(volumes = volumes_transfering,
                                          number_of_transfers = number_of_transfers,
                                          tip_change = 1,
                                          max_p20_volume = 15)
    else:
        tips_transfering = (0,0)

    amount_tips_20 = tips_aliquoting[0] + tips_transfering[0]
    amount_tips_300 = tips_aliquoting[1] + tips_transfering[1]
    
    tip_racks_p20, P20 = number_of_tipracks(starting_tip_p20,
                                            amount_tips_20)
    tip_racks_p300, P300 = number_of_tipracks(starting_tip_p300,
                                              amount_tips_300)
    
    return tip_racks_p20, tip_racks_p300, P20, P300