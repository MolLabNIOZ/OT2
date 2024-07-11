"""
version: Jan_2024
"""
def trial(pipette, volume, source, destination):
   for well in destination:
       pipette.pick_up_tip()
       pipette.aspirate(volume, source)
       pipette.dispense(volume + 10, well.bottom(2))
       pipette.drop_tip()
   return      


def aliquoting_reagent(reagent_source, 
                       reagent_tube_type, 
                       reagent_startvolume,
                       aliquot_volume,
                       destination_wells,
                       p20,
                       p300,
                       tip_change,
                       action_at_bottom,
                       pause,
                       protocol):
    """
    A protocol for aliquoting reagent (mastermix, dilution buffer, etc)
    Parameters
    ----------
    reagent_source : list
        List of tube(s)/well(s) filled with reagent
    reagent_tube_type : brand / size
        'tube_1.5mL' / 'tube_5mL' / 'tube_15mL' / 'tube_50mL'
    reagent_startvolume : int
        exact volume in µL that is present in the reagent tube(s)
    aliquot_volume : float
        volume in µL that you want aliquoted
    destination_wells : list
        List of tube(s)/well(s) to be filled with reagent
    p20 : labware definition
    p300 : labware definition
    tip_change : int
        After how many aliquots do you want to change the tip?
    action_at_bottom : string
        'next_tube' / 'continue_at_bottom' / 'raise_error'
    pause : boolean True or False
        Do you want the robot to pause after aliquoting the reagent?
        Useful if you want to keep stock tubes closed as much as possible.
    protocol : def run(protocol: protocol_api.ProtocolContext):

    Raises
    ------
    Exception
        If the bottom is reached, it's possible to let the protocol raise an
        error. Another option is to continue with a next tube, or to keep
        pipetting from the bottom

    Returns
    -------
    None.

    """   
    #### If a list of volumes is provided, 
    if isinstance(aliquot_volume, list):
        raise Exception("Use the aliquoting_varying_volumes module instead of the "
                        "aliquoting_reagentt module")
        
    from data.user_storage.mollab_modules import VolumeTracking as VT
    
    #### Variables for volume tracking and aliquoting        
    counter = 0
    source = reagent_source[counter]          
    
    #### Determine start_height (at the start, current_height = start_height)
    start_height = current_height = VT.cal_start_height(reagent_tube_type, 
                                                     reagent_startvolume)
    #### Determine which pipette to use
    if aliquot_volume > 19:
        pipette = p300
        gap = 10
        push_out_volume = 5
    else:
        pipette = p20
        gap = 1
        push_out_volume = 2
    
    ## Aspirate a little more for reverse pipetting
    aspiration_vol = aliquot_volume + gap
    
    #### Aliquot reagent in all destination wells
    ### Loop through destination wells
    for i, well in enumerate(destination_wells):
        # aliquot in the correct wells, for each well do the following:  
        
        ## If we are at the first well, start by picking up a tip
        if i == 0: 
          pipette.pick_up_tip()
        ## After every #th well, drop tip and pick up new          
        elif i % tip_change == 0:
              pipette.drop_tip()
              pipette.pick_up_tip()
        
        ## Call volume_tracking function
        current_height, pip_height, bottom_reached = VT.volume_tracking(
            reagent_tube_type, 
            aliquot_volume, 
            current_height, 
            'emptying')
              # obtain current_height, pip_height and whether bottom_reached
        
        ## What to do when the bottom of the tube is reached        
        if bottom_reached:
            
            ## Continue with next tube, reset volume_tracking
            if action_at_bottom == 'next_tube':
                                           
                current_height = start_height
                current_height, pip_height, bottom_reached = (
                    VT.volume_tracking(
                        reagent_tube_type, 
                        aliquot_volume, 
                        current_height, 
                        'emptying'))
                counter = counter + 1
                source = reagent_source[counter]
                aspiration_location = source.bottom(current_height)
                protocol.comment(
                "Continue with tube " + str(counter + 1) + " of reagent")
            
            ## Keep pipetting from the bottom
            elif action_at_bottom == 'continue_at_bottom':
                aspiration_location = source.bottom()
                protocol.comment("You've reached the bottom of the tube!")   
            
            ## Raise an error
            elif action_at_bottom == 'raise_error':
                raise Exception(
                    "There is not enough reagent to run this protocol")
        
        ## What to do when the bottom of the tube is not yet reached    
        else:
            aspiration_location = source.bottom(pip_height)
        
        ## The actual aliquoting by reverse pipetting
        # Aspirate specified volume + extra from the source tube
        pipette.aspirate(aspiration_vol, aspiration_location)
        
        # Sets boundries for when pipetting on the well bottom or when 2 mm above the well bottom
        if aliquot_volume <= 5:
            dispense_location = well
        else:
            dispense_location = well.bottom(2)
        # Dispense specified volume in destination well
        pipette.dispense(aliquot_volume, dispense_location)
        # introduce an airgap to avoid dripping
        pipette.air_gap(gap)
        # Dispense the remaining air + reagent back into the source tube
        pipette.dispense(gap*2, aspiration_location, push_out=push_out_volume) # Blow-out
        
    ## When finished, drop tip
    pipette.drop_tip()
    
    ## If desired, pause after aliquoting
    if pause:
        protocol.pause("Aliquoting of reagent is finished")
        
    return
        
def aliquoting_varying_volumes(reagent_source, 
                               reagent_tube_type, 
                               reagent_startvolume,
                               aliquot_volumes,
                               destination_wells,
                               p20,
                               p300,
                               tip_change,
                               action_at_bottom,
                               pause,
                               protocol):
    """
    A protocol for aliquoting reagent (mastermix, dilution buffer, etc) in
    varying volumes, from 1 source to multiple destination wells.
    Parameters
    ----------
    reagent_source : list
        List of tube(s)/well(s) filled with reagent
    reagent_tube_type : string
        'tube_1.5mL' / 'tube_5mL' / 'tube_15mL' / 'tube_50mL'
    reagent_startvolume : int
        exact volume in µL that is present in the reagent tube(s)
    aliquot_volumes : list
        volumes in µL that you want aliquoted
    destination_wells : list
        List of tube(s)/well(s) to be filled with reagent
    p20 : labware definition
    p300 : labware definition
    tip_change : int
        After how many aliquots do you want to change the tip?
    action_at_bottom : string
        'next_tube' / 'continue_at_bottom' / 'raise_error'
    pause : boolean True or False
        Do you want the robot to pause after aliquoting the reagent?
        Useful if you want to keep stock tubes closed as much as possible.
    protocol : def run(protocol: protocol_api.ProtocolContext):

    Raises
    ------
    Exception
        If the bottom is reached, it's possible to let the protocol raise an
        error. Another option is to continue with a next tube, or to keep
        pipetting from the bottom

    Returns
    -------
    None.

    """   
    protocol.comment("newest version of module")
    #### Import volume tracking module
    from data.user_storage.mollab_modules import VolumeTracking as VT
    
    #### Determine start_height (at the start, current_height = start_height)
    start_height = current_height = VT.cal_start_height(reagent_tube_type, 
                                                        reagent_startvolume)
    
    #### If only 1 volume is provided, 
    if not isinstance(aliquot_volumes, list):
        raise Exception("Use the aliquoting_reagent module instead of the "
                        "aliquoting_varying_volumes module")

    #### Variables for volume tracking and when to change tubes     
    counter = 0
    source = reagent_source[counter]
    
    #### Looping through pipettes:
    for pipette in [p20,p300]:
        #### to keep track of tip use, to determine when to change tip
        tip_counter = 0
        
        ### Loop through list of volumes and destinations
        for well, aliquot_volume in zip(destination_wells, 
                                        aliquot_volumes):
            if pipette  == p20:
                min_volume = 0
                max_volume = 19
                gap = 1
                push_out_volume = 1
            elif pipette == p300:
                min_volume = 19
                max_volume = 195
                gap = 10
                push_out_volume = 5
                
            if min_volume < aliquot_volume <= max_volume:
                
                    ## If we are at the first well, start by picking up a tip
                    if tip_counter == 0:
                        pipette.pick_up_tip()
                    ## Change tips after x number of aliquots
                    elif tip_counter % tip_change == 0:
                        pipette.drop_tip()
                        pipette.pick_up_tip()
                    
                    #### Call volume_tracking function
                    current_height, pip_height, bottom_reached = (
                        VT.volume_tracking(
                            reagent_tube_type,
                            aliquot_volume, 
                            current_height, 
                            'emptying'))
                    
                    ### What to do when the bottom of the tube is reached        
                    if bottom_reached:
                        # Continue with next tube, reset volume_tracking
                        if action_at_bottom == 'next_tube':                                          
                            current_height = start_height
                            current_height, pip_height, bottom_reached = (
                                VT.volume_tracking(
                                    reagent_tube_type, 
                                    aliquot_volume, 
                                    current_height, 
                                    'emptying'))
                            counter = counter + 1
                            source = reagent_source[counter]
                            aspiration_location = source.bottom(current_height)
                            protocol.comment(f"Continue with tube "
                                             f"{str(counter + 1)} of reagent")
                    
                        # Keep pipetting from the bottom
                        elif action_at_bottom == 'continue_at_bottom':
                            aspiration_location = source.bottom()
                            protocol.comment("You've reached the bottom "
                                             "of the tube!")   
                        
                        # Raise an error
                        elif action_at_bottom == 'raise_error':
                            raise Exception("There is not enough reagent to run "
                                            "this protocol")
            
                    ### What to do when the bottom of the tube is not yet reached    
                    else:
                        aspiration_location = source.bottom(pip_height)
            
                    ## The actual aliquoting by reverse pipetting
                    # Aspirate specified volume + extra from the source tube
                    pipette.aspirate(aliquot_volume + gap, aspiration_location)
                    # Dispense specified volume in destination well
                    pipette.dispense(aliquot_volume, well.bottom(2))
                    # introduce an airgap to avoid dripping
                    pipette.air_gap(gap)
                    # Dispense the remaining air + reagent back into the source tube
                    pipette.dispense(gap * 2, aspiration_location, push_out=push_out_volume) # Blow-out
                    
                    # Add 1 use to the tip_counter
                    tip_counter += 1
                
        ## When finished with pipette, drop tip and reset counter
        try:
            pipette.drop_tip()    
        except:
            continue
            
    ## If desired, pause after aliquoting
    if pause:
        protocol.pause("Aliquoting of reagent is finished")
        
    return

def transferring_reagents(source_wells,
                          destination_wells,
                          transfer_volume,
                          airgap,
                          mix,
                          p20,
                          p300,
                          protocol):
    """
    Parameters
    ----------
    source_wells : list
        List of tube(s)/well(s) to get reagent from
    destination_wells : list
        List of tube(s)/well(s) to trasfer reagent to
    transfer_volume : float
        volume in µL that you want tranferred
    airgap : Boolean True or False
        Do you want an airgap after aspiration and after dispensing
    mix : Boolean True or False
        Do you want to mix (pipette up and down) after dispensing
    p20 : labware definition
    p300 : labware definition
    protocol : def run(protocol: protocol_api.ProtocolContext):

    Returns
    -------
    None.

    """
    #### If a list of volumes is provided, 
    if isinstance(transfer_volume, list):
        raise Exception("Use the transferring_variable_volumes module instead of the "
                        "transferring_reagent module")
    
    #### Determine which pipette to use:
    if transfer_volume <= 15:
        pipette = p20
        push_out_volume = 2
    else:
        pipette = p300
        push_out_volume = 5
    
    #### Calculate airgap and mix volumes
    if airgap:
        if pipette == p20:
            airgap_volume = 1
        else:
            airgap_volume = 10
    if mix:
        if pipette == p20:
            mix_volume = 5
        else:
            if transfer_volume <= 50:
                mix_volume = transfer_volume
            else:
                mix_volume = 50
    
    #### The actual transfer
    for source_well, destination_well in zip(source_wells, destination_wells):
        ## Pick up a pipette_tip
        pipette.pick_up_tip()
        ## Aspirate specified volume from the source_well
        pipette.aspirate(transfer_volume, source_well)
        ## If desired, include an airgap
        if airgap:
            pipette.air_gap(airgap_volume)
            dispense_volume = transfer_volume + airgap_volume
        else:
            dispense_volume = transfer_volume
        ## Dispense in the destination_well
        pipette.dispense(dispense_volume, destination_well, push_out=push_out_volume)
        ## If desired, mix
        if mix:
            pipette.mix(3, mix_volume, destination_well)
        ## blow out
        pipette.blow_out()
        ## drop tip
        pipette.drop_tip()
        
    return
        
    
def transferring_varying_volumes(source_wells,
                                 destination_wells,
                                 transfer_volumes,
                                 airgap,
                                 mix,
                                 p20,
                                 p300,
                                 protocol):
    """
    Parameters
    ----------
    source_wells : list
        List of tube(s)/well(s) to get reagent from
    destination_wells : list
        List of tube(s)/well(s) to trasfer reagent to
    stock_volumes : list
       list with volumes in µL to take from every stock
    reagent_volumes : list
       list with volumes in µL to use of the dilution reagent
    final_volume : Boolean False or float
        if float, this will be used to calculate how much reagent to add
        if False, the list with reagent_volumes will be used
    airgap : Boolean True or False
        Do you want an airgap after aspiration and after dispensing
    mix : Boolean True or False
        Do you want to mix (pipette up and down) after dispensing
    p20 : labware definition
    p300 : labware definition
    protocol : def run(protocol: protocol_api.ProtocolContext)

    Returns
    -------
    None.

    """
    
    #### If only 1 volume is provided, 
    if not isinstance(transfer_volumes, list):
        raise Exception("Use the transferring_reagent module instead of the "
                        "transferring_varying_volumes module")
    
    #### Loop through list of volumes, sources and destinations
    for i, (source_well, destination_well, transfer_volume) in enumerate(
            zip(source_wells, destination_wells, transfer_volumes)):
        #### Determine which pipette to use:
        if transfer_volume <= 15:
            pipette = p20
            push_out_volume = 2
        else:
            pipette = p300
            push_out_volume = 5
        
        #### Calculate airgap and mix volumes
        if pipette == p20:
            airgap_volume = 1
        else:
            airgap_volume = 10
        
        if pipette == p20:
            mix_volume = 5
        else:
            if transfer_volume <= 50:
                mix_volume = transfer_volume
            else:
                mix_volume = 50
       
        #### The actual transfer
        ## Pick up a pipette_tip
        pipette.pick_up_tip()
        ## Aspirate specified volume from the source_well
        pipette.aspirate(transfer_volume, source_well)
        ## If desired, include an airgap
        if airgap:
            pipette.air_gap(airgap_volume)
            dispense_volume = transfer_volume + airgap_volume
        else:
            dispense_volume = transfer_volume
        ## Dispense in the destination_well
        pipette.dispense(dispense_volume, destination_well, push_out=push_out_volume)
        ## If desired, mix
        if mix:
            pipette.mix(3, mix_volume, destination_well)
        ## blow out
        pipette.blow_out()
        
        ## drop tip
        pipette.drop_tip()
            
    return

def transferring_reagents_no_bubbles(source_wells,
                                     destination_wells,
                                     transfer_volume,
                                     mix,
                                     p20,
                                     p300,
                                     protocol):
    """
    Parameters
    ----------
    source_wells : list
        List of tube(s)/well(s) to get reagent from
    destination_wells : list
        List of tube(s)/well(s) to trasfer reagent to
    transfer_volume : float
        volume in µL that you want tranferred
    mix : Boolean True or False or number that you want to mix it with
        Do you want to mix (pipette up and down) after dispensing
    p20 : labware definition
    p300 : labware definition
    protocol : def run(protocol: protocol_api.ProtocolContext):

    Returns
    -------
    None.

    """
    #### If a list of volumes is provided, 
    if isinstance(transfer_volume, list):
        raise Exception("Use the transferring_variable_volumes module instead of the "
                        "transferring_reagent module")
    
    #### Determine which pipette to use:
    if transfer_volume <= 15:
        pipette = p20
    else:
        pipette = p300
    
    #### Calculate airgap and mix volumes
    if mix:
        if pipette == p20:
            if mix == True:
                mix_volume = 5
            else:
                mix_volume = mix
        else:
            if transfer_volume <= 50:
                mix_volume = transfer_volume
            else:
                mix_volume = 50
    
    #### The actual transfer
    for source_well, destination_well in zip(source_wells, destination_wells):
        ## Pick up a pipette_tip
        pipette.pick_up_tip()
        ## Aspirate specified volume from the source_well
        pipette.aspirate(transfer_volume, source_well)
        ## If desired, include an airgap
        dispense_volume = transfer_volume
        ## Dispense in the destination_well
        pipette.dispense(dispense_volume, destination_well)
        ## If desired, mix
        if mix:
            pipette.mix(3, mix_volume, destination_well)
        ## drop tip
        pipette.drop_tip()
        
    return

        
def pooling_varying_volumes(source_wells,
                            pool_volumes,
                            pool_tube,
                            pool_tube_type,
                            start_volume,
                            pool_volume_per_tube,
                            airgap,
                            mix,
                            p20,
                            p300,
                            protocol):
    """
    Parameters
    ----------
    source_wells : list
        List of tube(s)/well(s) to get pool from
    pool_volumes : list
        volumes in µL that you want to pool
    pool_tube : list
        List of tube(s)/well(s) to pool in
    pool_tube_type : string
        'tube_1.5mL' / 'tube_5mL' / 'tube_15mL' / 'tube_50mL'
    start_volume : float
        exact volume in µL that is already present in the pool tube(s)
    pool_volume_per_tube, : float
        exact volume in µL that is max pooled in 1 tube
    airgap : Boolean True or False
        Do you want an airgap after aspiration and after dispensing
    mix : Boolean True or False
        Do you want to mix (pipette up and down) after dispensing
    p20 : labware definition
    p300 : labware definition
    protocol : def run(protocol: protocol_api.ProtocolContext)

    Returns
    -------
    None.

    """
    #### Import volume tracking module
    from data.user_storage.mollab_modules import VolumeTracking as VT
    
    #### Determine start_height (at the start, current_height = start_height)
    start_height = current_height = VT.cal_start_height(pool_tube_type, 
                                                        start_volume)
    
    #### Variables for volume tracking and aliquoting        
    pooled_volume = 0
    counter = 0
    pool = pool_tube[counter]
    
    #### If only 1 volume is provided, 
    if not isinstance(pool_volumes, list):
        raise Exception("This protocol only works with a list of volumes.")
             
    #### First small volumes, then large volumes
    for pipette in [p20,p300]:
        ### Set airgap size, depending on pipette size
        if pipette  == p20:
            min_volume = 0
            max_volume = 19
            gap = 1
            push_out_volume = 2
                
        elif pipette == p300:
            min_volume = 19
            max_volume = 195
            gap = 10
            push_out_volume = 5
                
        ### Loop through list of volumes and destinations
        for well, pool_volume in zip(source_wells, pool_volumes):
            ## Aspirate a little more for reverse pipetting
            aspiration_vol = pool_volume + gap
            
            ## Determine which wells to fill with which pipette
            if min_volume < aspiration_vol <= max_volume:

                #### Call volume_tracking function
                current_height, pip_height, bottom_reached = (
                    VT.volume_tracking(pool_tube_type,
                                       pool_volume, 
                                       current_height,
                                       'filling'))
                pooled_volume += pool_volume
                
                #### If necesarry, continue with next tube
                # if bottom_reached or pooled_volume > pool_volume_per_tube:
                #     # Continue with next tube, reset volume_tracking
                #     current_height = start_height
                #     current_height, pip_height, bottom_reached = (
                #         VT.volume_tracking(pool_tube_type,
                #                            pool_volume, 
                #                            current_height,
                #                            'filling'))
                #     pooled_volume = 0
                #     counter += 1
                #     pool = pool_tube[counter]

                #### The actual pipetting                
                # Pick up a tip
                pipette.pick_up_tip()
                
                # Take up the specified volume per sample       
                pipette.aspirate(pool_volume, well)
                # Take an air gap, to prevent cross_contamination
                if airgap:
                    pipette.air_gap(gap)
                    dispense_volume = pool_volume + gap
                else:
                    dispense_volume = pool_volume
                    
                # Dispense in the pool_tube
                pipette.dispense(dispense_volume, pool.bottom(pip_height), push_out=push_out_volume)
                # Mix by pipetting up and down 3x
                pipette.mix(3, aspiration_vol, pool.bottom(pip_height + 5))
                # Blow out
                pipette.blow_out()
                              
                # drop tip
                pipette.drop_tip()
                