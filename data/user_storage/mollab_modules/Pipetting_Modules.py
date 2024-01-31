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
    from data.user_storage.mollab_modules import VolumeTracking as VT
    
    #### Variables for volume tracking and aliquoting        
    counter = 0
    source = reagent_source[counter]          
    
    #### Determine start_height (at the start, current_height = start_height)
    start_height = current_height = VT.cal_start_height(reagent_tube_type, 
                                                     reagent_startvolume)
    #### Determine which pipette to use
    if aliquot_volume >= 19:
        pipette = p300
        gap = 10
    else:
        pipette = p20
        gap = 1
    
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
        pipette.aspirate(aliquot_volume + gap, aspiration_location)
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
        protocol.pause("Aliquoting is finished")
        
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
    #### Determine which pipette to use:
    if transfer_volume <= 15:
        pipette = p20
    else:
        pipette = p300
    
    #### Calculate airgap and mix volumes
    if airgap:
        if pipette == p20:
            airgap_volume = 2
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
        
    
def transferring_variable_volumes(source_wells,
                                  destination_wells,
                                  stock_volumes,
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
    from data.user_storage.mollab_modules import VolumeTracking as VT
    
    start_height = current_height = VT.cal_start_height('tube_5mL', 4600)
    
    protocol.comment("opening file in file worked")
        
    
        
    