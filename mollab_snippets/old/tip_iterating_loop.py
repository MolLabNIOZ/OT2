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



p300.drop_tip()      
# =============================================================================