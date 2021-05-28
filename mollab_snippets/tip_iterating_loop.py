# =============================================================================
# Author(s): Sanne Vreugdenhil
# Creation date: 210528
# Description: Picking up a tip before the first tube, then dropping the tip 
#   and picking up a new tip after every 8 tubes untill we run out of tubes
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
        aspiration_location = tubes_5mL['A1'].bottom(z=1) #!!!
        protocol.comment("You've reached the bottom!")
    else:
        aspiration_location = tubes_5mL['A1'].bottom(pip_height) #!!!
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