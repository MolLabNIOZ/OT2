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
    else:
        pipette = p20
        gap = 1
    
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
        # Dispense specified volume in destination well
        pipette.dispense(aliquot_volume, well.bottom(2))
        # introduce an airgap to avoid dripping
        pipette.air_gap(gap)
        # Dispense the remaining air + reagent back into the source tube
        pipette.dispense(gap * 3, aspiration_location) # Blow-out
        
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
    reagent_tube_type : brand / size
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
    from data.user_storage.mollab_modules import VolumeTracking as VT
    
    #### Determine start_height (at the start, current_height = start_height)
    start_height = current_height = VT.cal_start_height(reagent_tube_type, 
                                                        reagent_startvolume)
    
    #### If only 1 volume is provided, 
    if not isinstance(aliquot_volumes, list):
        raise Exception("Use the aliquoting_reagent module instead of the "
                        "aliquoting_varying_volumes module")

    #### Variables for volume tracking and aliquoting        
    counter = 0
    source = reagent_source[counter]          
    
    #### to keep track of tip use, to determine when to change tip
    tip_counter = 0
    
    #### First small volumes, then large volumes
    for pipette in [p20,p300]:
        ### Set airgap size, depending on pipette size
        if pipette  == p20:
            gap = 1
        elif pipette == p300:
            gap = 10
        
        ### Loop through list of volumes and destinations
        for i, (well, aliquot_volume) in enumerate(zip(destination_wells, 
                                                       aliquot_volumes)):
            ## Aspirate a little more for reverse pipetting
            aspiration_vol = aliquot_volume + gap
            
            ## Determine which wells to fill with which pipette
            if (p20 and pipette == p20 and 0 < aspiration_vol <= 20 or 
                p300 and pipette == p300 and aspiration_vol > 20):
                
                # At the first well, start by picking up a tip
                if tip_counter == 0:
                    pipette.pick_up_tip()
                # Change tips after x number of aliquots
                if tip_counter % tip_change == 0:
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
                pipette.aspirate(aspiration_vol, aspiration_location)
                # Dispense specified volume in destination well
                pipette.dispense(aliquot_volume, well.bottom(2))
                # introduce an airgap to avoid dripping
                pipette.air_gap(gap)
                # Dispense the remaining air + reagent back into the source tube
                pipette.dispense(gap * 3, aspiration_location) # Blow-out
                
                # Add 1 use to the tip_counter
                tip_counter = tip_counter + 1
        
        ## When finished with specified pipette, drop tip and reset counter
        try:
            pipette.drop_tip()    
        except:
            continue
        tip_counter = 0
    
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
    else:
        pipette = p300
    
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
        ## Dispense in the destination_well
        pipette.dispense(transfer_volume + airgap_volume, destination_well)
        ## If desired, mix
        if mix:
            pipette.mix(3, mix_volume, destination_well)
        ## Alternative for blow out
        pipette.dispense(mix_volume, destination_well)
        ## drop tip
        pipette.drop_tip()
        
    return
        
    
def transferring_varying_volumes(source_wells,
                                  destination_wells,
                                  transfer_volumes,
                                  reagent_volumes,
                                  final_volume,
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
    protocol : def run(protocol: protocol_api.ProtocolContext):

    Returns
    -------
    None.

    """
    
    #### If only 1 volume is provided, 
    if not isinstance(transfer_volumes, list):
        raise Exception("Use the transferring_reagent module instead of the "
                        "transferring_varying_volumes module")
    
    #### Loop through list of volumes and destinations
    for i, (source_well, destination_well, transfer_volume) in enumerate(
            zip(source_wells, destination_wells, transfer_volumes)):
        #### Determine which pipette to use:
        if transfer_volume <= 15:
            pipette = p20
        else:
            pipette = p300
        
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
        ## Pick up a pipette_tip
        pipette.pick_up_tip()
        ## Aspirate specified volume from the source_well
        pipette.aspirate(transfer_volume, source_well)
        ## If desired, include an airgap
        if airgap:
            pipette.air_gap(airgap_volume)
        ## Dispense in the destination_well
        pipette.dispense(transfer_volume + airgap_volume, destination_well)
        ## If desired, mix
        if mix:
            pipette.mix(3, mix_volume, destination_well)
        ## Alternative for blow out
        pipette.dispense(mix_volume, destination_well)
        ## drop tip
        pipette.drop_tip()
            
    return
        
        