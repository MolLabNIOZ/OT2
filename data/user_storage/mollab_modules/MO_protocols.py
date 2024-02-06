# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 14:38:14 2024
@author: rdebeer
"""
def tapestation(tapestation_kit,
                starting_tip,
                number_of_reactions,
                skipped_wells,
                simulate,
                protocol):
# =============================================================================   
    
    """
    Parameters
    ----------
    tapestation_kit : which kit do you use for the tapestation kit
        'D1000', 'D5000', 'gDNA', 'RNA'.
    starting_tip : Well number of the first tip you will need.
    number_of_reactions : Amount of reactions.

    Returns
    -------
    None.
    """

    from data.user_storage.mollab_modules import Pipetting_Modules as PM
    from data.user_storage.mollab_modules import LabWare as LW
# =============================================================================
    protocol_dict = {
        'D1000' :[3,1,2],
        'D5000' :[10,1,5],
        'gDNA'  :[10,1,5],
        'RNA'   :[5,1,3]}
    reagent_volume, sample_volume, sample_mix_volume = protocol_dict[tapestation_kit]
    
    reagent_startvolume = reagent_volume * (number_of_reactions + 10)
    
    
# =============================================================================
    #### Pipette tips
    # calls the p20 pipette
    amount_tips_20 = 2
    tips_20 = LW.loading_tips(simulate = simulate,
                              tip_type = 'tipone_20uL',
                              amount = amount_tips_20,
                              deck_positions = [10,7],
                              protocol = protocol) 
    # Loading pipette
    P20 = True
    P300 = False
    tips_300 = False
    starting_tip_p300 = False
    p20, p300 = LW.loading_pipettes(P20,
                             tips_20,
                             starting_tip,
                             P300, 
                             tips_300,
                             starting_tip_p300,
                             protocol)
    
    # Deciding which tube type we need
    tube_type_reagent, number_of_tubes, max_volume = LW.which_tube_type(reagent_startvolume, 
                                                                        False)
    
    
    # Loading reagent rack
    reagent_racks = LW.loading_tube_racks(simulate = simulate,
                                          tube_type = tube_type_reagent,
                                          reagent_type = 'amber_reagent_tube',
                                          amount = 1,
                                          deck_positions = [4],
                                          protocol = protocol)
    
    ## Specific location of reagent tube
    reagent_tube = LW.tube_locations(source_racks = reagent_racks,
                                       specific_columns = False,
                                       skip_wells = False,
                                       number_of_tubes = 1)
    
    # Loading destination-plate
    tapestation_plate = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = 'skirted_plate_96',
                                           reagent_type = 'destination-plate',
                                           amount = 1,
                                           deck_positions = [11],
                                           protocol = protocol)
    
    # Mastermix destinations
    tapestation_plate_wells = LW.tube_locations(source_racks = tapestation_plate,
                                               specific_columns = False,
                                               skip_wells = False,
                                               number_of_tubes = number_of_reactions)
    
    # Loading sample-plate
    sample_plate = LW.loading_tube_racks(simulate = simulate,
                                           tube_type = 'skirted_plate_96',
                                           reagent_type = 'sample-plate',
                                           amount = 1,
                                           deck_positions = [9],
                                           protocol = protocol)
    
    # Mastermix destinations
    sample_plate_wells = LW.tube_locations(source_racks = sample_plate,
                                               specific_columns = False,
                                               skip_wells = skipped_wells,
                                               number_of_tubes = number_of_reactions)
   
    ## PIPETTING===============================================================
    ## ========================================================================
    # Pipetting reagent--------------------------------------------------------
    PM.aliquoting_reagent(reagent_source = reagent_tube,
                          reagent_tube_type = tube_type_reagent,
                          reagent_startvolume = reagent_startvolume,
                          aliquot_volume = reagent_volume,
                          destination_wells = tapestation_plate_wells,
                          p20 = p20,
                          p300 = p300,
                          tip_change = 16,
                          action_at_bottom = 'continue_at_bottom',
                          pause = False,
                          protocol = protocol)  
    
    # # Transfering sample
    PM.transferring_reagents(source_wells = sample_plate_wells,
                              destination_wells = tapestation_plate_wells,
                              transfer_volume = sample_volume,
                              airgap = True,
                              mix = sample_mix_volume,
                              p20 = p20,
                              p300 = p300,
                              protocol = protocol)
    
    
    return