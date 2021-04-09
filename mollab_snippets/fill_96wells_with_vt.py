# =============================================================================
# How to fill an entrie 96 wells plate.
# =============================================================================

##### Aliquoting the mix
    p300.pick_up_tip()
      ## p300 picks up tip from location specified in variable starting_tip ##
    for well in plate_96.wells():
      ## Name all the wells in the plate 'well', for all these do:          ##  
        tv = volume_tracking(
            container, dispension_vol, current_height)  
        current_height, delta_height = tv
          ## The volume_tracking function needs the arguments container,    ##
          ## current_vol and the aspiration_vol which we have set in this   ##
          ## protocol. With those variables, the function calculates the    ##
          ## current_height, current_vol and delta_height of the liquid     ##
          ## after the next aspiration step. The outcome is stored as tv and##
          ## then the specific variables are updated.                       ##
        pip_height = current_height - 2
          ## Make sure that the pipette tip is always submerged by setting  ##
          ## the current height 1 mm below its actual height                ##
        if current_height - delta_height <= 1: 
            aspiration_location = tubes_5mL['C3'].bottom(z=1)
            protocol.comment("You've reached the bottom!")
        else:
            aspiration_location = tubes_5mL['C3'].bottom(pip_height) #!!!
          ## If the level of the liquid in the next run of the loop will be ##
          ## smaller than 1 we have reached the bottom of the tube. To      ##
          ## prevent the pipette from crashing into the bottom, we tell it  ##
          ## to go home and pause the protocol so that this can never happen##
          ## Set the location of where to aspirate from. Because we put this##
          ## in the loop, the location will change to the newly calculated  ##
          ## height after each pipetting step.                              ##
        well_c = str(well)

        if (well_c == 'A3 of 96well_plate on 9' or 
            well_c == 'A5 of 96well_plate on 9' or 
            well_c == 'A7 of 96well_plate on 9' or
            well_c == 'A9 of 96well_plate on 9' or
            well_c == 'A11 of 96well_plate on 9'):
            p300.drop_tip()
            p300.pick_up_tip()
          ## Pick up a new tip every two rows.                              ##
        p300.aspirate(aspiration_vol, aspiration_location)
         ## Aspirate the amount specified in aspiration_vol from the        ##
         ## location specified in aspiration_location.                      ##
        p300.dispense(dispension_vol, well)
          ## Dispense the amount specified in dispension_vol to the location##
          ## specified in well (so a new well every time the loop restarts) ##
        p300.dispense(10, aspiration_location) #!!!
          ## Blow out any remaining liquid (disposal volume) in the source  ##
          ## tube before we want to aspirate again.                         ##
    p300.drop_tip()                    
      ## Drop the final tip in the trash bin.                               ##