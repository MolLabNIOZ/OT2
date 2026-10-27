simulate = False
# IMPORT STATEMENTS============================================================
# This region contains basic python/opentrons stuff
# =============================================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
#### For simulating in the app, set pathway to modules
import sys
sys.path.append("O:/")
sys.path.append("/mnt/c/Program files/Opentrons")
#### Import mollab protocol module
from data.user_storage.mollab_modules import LabWare_v4 as LW
from data.user_storage.mollab_modules import VolumeTracking as VT
####
import random

# =============================================================================

# METADATA=====================================================================
# This region contains metadata that will be used by the app while running
# =============================================================================
metadata = {'author': 'NIOZ Molecular Ecology',
            'protocolName': 'Opendag with P20',
            'description': "pipetting logo's and other images" 
            }
requirements = {'apiLevel': '2.27', 'robotType': 'OT-2'}
# =============================================================================
# PARAMETERS===================================================================
# This region contains all parameters that can be changed
# =============================================================================
def add_parameters(parameters: protocol_api.Parameters):
    parameters.add_int(variable_name="number_of_images",
                       display_name="number of images",
                       description="How many images do you want?",
                       default=30,
                       minimum=0,
                       maximum=30,
                       unit="images")
    parameters.add_int(variable_name="transfer_volume",
                       display_name="transfer volume",
                       description="How much do you want to transfer?",
                       default=2,
                       minimum=0,
                       maximum=20,
                       unit="µL")    
# =============================================================================
# IMAGE DICTS==================================================================
# This regions contains a dict with all image information
# =============================================================================
images = {'groot_logo': {'sand':[], 'orange':[7,14,15,19,20,22,23,26,27,28,29,30,34,35,36,37,38,45,46,53,54,61,62,65,66,67,68,69,70,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,113,114,115,116,121,122,123,124,154,155,156,162,163,164,171,172], 'blue':[192,193,194,195,196,197,198,199,201,202,211,212,221,222,224,225,226,227,228,229,230,231,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,290,291,292,293,297,298,299,300,301,302,304,305,310,311,312,313,318,319,321,322,323,324,325,326,330,331,332,333,344,345,350,351,352,353,357,358,359,360,361,363,364,366,367,368,369,370,374,375,376,377,382,383,395,402,403,410,411,412,418,419,420,426,427,428,429,434,435,436,437,442,443,444,445,446,450,451,452,453,454,458,459,460,461,462,467,468,469,470,471,475,476,477,478,479,480,481,482,483,484,485,486,487,489,490,491,492,493,494,495,498,499,500,501,502,506,507,508,509,510,514,515,516,517,518,522,523,524,525,530,531,532,533,538,539,540,546,547,548,554,555,561,562,563,568,569], 'cyan':[], 'green':[], 'black':[]},
          'klein_logo': {'sand':[], 'orange':[6,7,14,15,19,20,21,22,23,30,31,34,35,36,37,38,39,40,41,42,43,44,45,46,47,58,59,60,61,75,76,77], 'blue':[98,99,106,107,108,114,115,116,117,122,123,124,125,126,130,131,132,133,134,139,140,141,142,143,144,145,146,147,148,149,150,151,153,154,155,156,157,158,162,163,164,165,166,170,171,172,173,177,178,179,180,184,185,186,187], 'cyan':[], 'green':[], 'black':[]},
          'NIOZ_kleuren': {'sand':[0,8,16,24,32,40,48,56,64,72,80,88], 'orange':[1,9,17,25,33,41,49,57,65,73,81,89,2,10,18,26,34,42,50,58,66,74,82,90], 'blue':[3,11,19,27,35,43,51,59,67,75,83,91,4,12,20,28,36,44,52,60,68,76,84,92], 'cyan':[5,13,21,29,37,45,53,61,69,77,85,93,6,14,22,30,38,46,54,62,70,78,86,94], 'green':[7,15,23,31,39,47,55,63,71,79,87,95], 'black':[]},
          'NIOZ_kleuren_150': {'sand':[0,16,24,56,64,88], 'orange':[17,25,41,49,57,73,81,2,18,26,42,50,58,74,82], 'blue':[3,19,27,51,59,75,83,4,20,28,36,44,60,76,84], 'cyan':[5,21,29,37,45,61,77,85,6,22,30,38,46,62,78,86], 'green':[31,63,71,95], 'black':[8,32,40,48,72,80,1,9,33,65,89,10,34,66,90,11,35,43,67,91,12,52,68,92,13,53,69,93,14,54,70,94,7,15,23,39,47,55,79,87]},
          'DNA': {'sand':[], 'orange':[32,25,11,4,13,22,31,88,81,67,60,69,78,87], 'blue':[0,9,18,27,36,29,15,56,65,74,83,92,85,71], 'cyan':[], 'green':[], 'black':[]},
          'inktvis': {'sand':[], 'orange':[], 'blue':[6,13,17,18,19,22,24,25,27,28,29,31,32,33,35,36,38,40,41,42,43,44,45,48,49,50,51,52,53,56,57,59,60,62,64,65,67,68,69,71,73,74,75,78,85,94], 'cyan':[34,58], 'green':[], 'black':[]},
          'vis': {'sand':[], 'orange':[3,4,10,11,12,13,17,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,49,50,51,52,53,54,58,59,60,61,65,66,67,68,69,70,72,73,74,75,76,77,78,79,80,81,82,85,86,87,88,95], 'blue':[18], 'cyan':[], 'green':[], 'black':[]},
          'schildpad': {'sand':[], 'orange':[], 'blue':[3,4,11,12,16,23,80,81,86,87], 'cyan':[], 'green':[18,19,20,21,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,66,67,68,69,70,74,75,76,77,83,84], 'black':[]},          
          'visje': {'sand':[12,43,44,58,59,60], 'orange':[11,13,19,20,21,28,35,36,42,45,49,50,51,52,53,57,61,62,66,67,68,69,74,76,77,83,84], 'blue':[2,3,5,6,10,14,18,22,27,29,34,37,41,46,48,54,55,56,63,65,70,73,78,82,85,91,92], 'cyan':[0,1,4,7,8,9,15,16,17,23,24,25,26,30,31,32,33,38,39,40,47,64,71,72,79,80,81,86,87,88,89,90,93,94,95], 'green':[75], 'black':[]},
          'H2O': {'sand':[], 'orange':[], 'blue':[0,1,2,3,4,10,16,17,18,19,20,35,37,38,43,44,46,57,58,59,64,68,72,76,81,82,83], 'cyan':[], 'green':[], 'black':[]},
          'rog': {'sand':[], 'orange':[], 'blue':[3,10,11,12,17,18,19,20,21,24,25,27,29,30,32,33,35,37,38,41,42,43,44,45,50,51,52,58,59,60,67,75,83,91], 'cyan':[], 'green':[], 'black':[]},
          'kwal': {'sand':[], 'orange':[], 'blue':[], 'cyan':[18,23,25,26,27,30,32,33,34,35,36,37,40,41,42,43,46,47,48,49,50,51,54,55,56,57,58,59,60,61,65,66,67,70,74,79], 'green':[], 'black':[]},
          'vis3': {'sand':[], 'orange':[], 'blue':[19], 'cyan':[3,10,11,17,18,26,29,30,32,35,38,39,40,43,44,48,49,52,56,57,58,65], 'green':[4,12,13,20,21,25,27,28,33,34,36,37,41,42,45,50,51,53,54,59,60,61,62,67,68,70,75,76,82,83,84,85,90,93], 'black':[]}, 
          #'kwal': {'sand':[], 'orange':[], 'blue':[], 'cyan':[], 'green':[], 'black':[]},
          }

def run(protocol: protocol_api.ProtocolContext):
# =============================================================================
# LIGHTS ON====================================================================
# =============================================================================
    protocol.set_rail_lights(True)
# =============================================================================
# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    #### PIPETTE TIPS
    tips_20 = LW.loading_tips(simulate = simulate,
                               tip_type = 'tipone_20uL',
                               amount = 2,
                               deck_positions = [10,11],
                               protocol = protocol)
    tip_counter = 0
    #### PIPETTES       
    p20, p300 = LW.loading_pipettes('P20',
                                    False,
                                    tips_20,
                                    'A1', 
                                    False,
                                    False,
                                    protocol)
    #### LABWARE
    # Colored liquids
    color_rack = LW.loading_tube_racks(simulate = simulate,
                                       tube_type = '15mL_tubes',
                                       reagent_type = 'colored liquids',
                                       amount = 1,
                                       deck_positions = [9],
                                       protocol = protocol)
    color_tubes = LW.multiple_reagent_tube_locations(source_racks = color_rack,
                                                     specific_columns = False,
                                                     skip_wells = False,
                                                     reagent_and_numbers_dict = {'NIOZ1': 1, 'NIOZ2': 1, 'NIOZ3': 1, 'NIOZ4': 1, 'NIOZ5': 1, 'black': 1},
                                                     volume = 15000,
                                                     protocol = protocol)
    # Which color is where
    color_sources = {'sand': color_tubes[0][0],
                     'orange': color_tubes[1][0],
                     'blue': color_tubes[2][0],
                     'cyan': color_tubes[3][0],
                     'green': color_tubes[4][0],
                     'black': color_tubes[5][0]}
    
    ## Volume tracking
    start_height = VT.cal_start_height('15mL_tubes', 14500)
    current_heights = {'sand':start_height, 'orange':start_height, 'blue':start_height, 'cyan':start_height, 'green':start_height, 'black':start_height}

    # Plates
    PCR_plates = LW.loading_tube_racks(simulate = simulate,
                                      tube_type = 'non_skirted_plate_96',
                                      reagent_type = 'logo',
                                      amount = 8,
                                      deck_positions = [1,2,3,4,5,6,7,8],
                                      protocol = protocol)

    # For tracking if well is filled, and with what color
    plate_states = {}
    for plate in PCR_plates:
        plate_states[plate] = {}

    image_plates = {'groot_logo': [[PCR_plates[6] , PCR_plates[7] , PCR_plates[3] , PCR_plates[4] , PCR_plates[0] , PCR_plates[1]]],
                    'klein_logo': [[PCR_plates[5] , PCR_plates[2]],[ PCR_plates[3] , PCR_plates[0]],[ PCR_plates[4] , PCR_plates[1]],[ PCR_plates[6] , PCR_plates[3]],[ PCR_plates[7] , PCR_plates[4]]],
                    'NIOZ_kleuren': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]],
                    'NIOZ_kleuren_150': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]],
                    'DNA': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]],
                    'inktvis': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]],
                    'vis': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]],
                    'visje': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]],
                    'schildpad': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]],
                    'rog': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]],
                    'kwal': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]],
                    'vis3': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]],
                    'H2O': [[PCR_plates[0]],[ PCR_plates[1]],[ PCR_plates[2]],[ PCR_plates[3]],[ PCR_plates[4]],[ PCR_plates[5]],[ PCR_plates[6]],[ PCR_plates[7]]]
                    }
# =============================================================================
# LOOP=========================================================================
# Loop for chosen amount of minutes
# =============================================================================
    ### Run for a specified amount of images
    images_todo = ['groot_logo','klein_logo','NIOZ_kleuren','NIOZ_kleuren_150','DNA','inktvis','vis','schildpad','visje','H2O','rog','kwal', 'vis3']    
    for i in range(protocol.params.number_of_images):
        ## Pick an image at random
        current_image = random.choice(images_todo)
        protocol.comment(f"Ik ga zo een {current_image} pipetteren!")
        ## Pick a random destination
        current_destination_plates = random.choice(image_plates[current_image])
        
        ## If necesarry, empty the plates that will contain the new image
        for plate in current_destination_plates:
            # Skip empty plates
            if not plate_states[plate]:
                continue
            protocol.comment("Eerst haal ik de plaat/platen die ik nodig heb weer leeg")
            # Group wells by color
            wells_by_color = {}
            for well, color in plate_states[plate].items():
                if color not in wells_by_color:
                    wells_by_color[color] = []
                wells_by_color[color].append(well)

            # Empty color by color
            
            for color, wells_to_empty in wells_by_color.items():
                # Skip unused colors
                if not wells_to_empty:
                    continue
                # Destination
                color_source_tube = color_sources[color]
                current_height = current_heights[color]
                
                # Pick up a tip
                p20.pick_up_tip()
                tip_counter += 1
                
                # Empty all wells with the apropriate color. Empty multiple wells at once and return to color tube
                batch_size = int(p20.max_volume // protocol.params.transfer_volume)
                for batch_start in range(0, len(wells_to_empty), batch_size):
                    batch = wells_to_empty[batch_start:batch_start + batch_size]
                    batch_volume = protocol.params.transfer_volume * len(batch)
                    
                    # Volume tracking
                    current_height, pip_height, bottom_reached = VT.volume_tracking('15mL_tubes',                                                                
                                                                                    batch_volume,
                                                                                    current_height, 
                                                                                    'filling')
                    
                    # Aspirate from multiple wells
                    for well in batch:
                        p20.aspirate(protocol.params.transfer_volume,
                                      well.bottom())
                        
                    # Return all at once
                    p20.dispense(batch_volume, color_source_tube.bottom(current_height))
                    p20.blow_out(color_source_tube.top(-2))
                
                
                # Return tip to tip rack            
                p20.return_tip()
                ## When 2 racks of tips have been used, reset the tip racks
                if tip_counter % 192 == 0:
                    p20.reset_tipracks()
            
                #Update the height of colored liquid
                current_heights[color] = current_height

            # Clear plate state after emptying
            plate_states[plate] = {}

        #### Filling plates
        all_wells = []
        for plate in current_destination_plates:
            for well in plate.wells():
                all_wells.append(well)
        
        ## Make dictionary for wells per color
        color_wells = {}
        for color, indices in images[current_image].items():
            color_wells[color] = [all_wells[i] for i in indices]
            
        ## Transfer by color
        protocol.comment(f"Ik ga nu een {current_image} pipetteren!")
        for color, wells in color_wells.items():  
            if not wells:
                continue
            # Source
            color_source_tube = color_sources[color]
            current_height = current_heights[color]
            
            # Destination
            wells_to_fill = [all_wells[i] for i in images[current_image][color]]
            
            # Pick up a tip
            p20.pick_up_tip()
            tip_counter += 1
            
            # Fill all wells with the apropriate color
            # Pick up 300µL and empty in several tubes
            batch_size = int(p20.max_volume // protocol.params.transfer_volume)
            for batch_start in range(0, len(wells_to_fill), batch_size):

                batch = wells_to_fill[batch_start:batch_start + batch_size]
                batch_volume = protocol.params.transfer_volume * len(batch)

                # Volume tracking
                current_height, pip_height, bottom_reached = VT.volume_tracking(
                    '15mL_tubes',
                    batch_volume,
                    current_height,
                    'emptying')
                
                ## When bottom is reached continue to next color        
                if bottom_reached:
                    protocol.comment(f"You've reached the bottom of the {color} tube!")
                    continue             
            
                aspiration_location = color_source_tube.bottom(pip_height)

                # Aspirate max volume from the right color
                p20.aspirate(batch_volume, aspiration_location)
                
                # Dispense specified volume in destination wells
                for well in batch:
                    p20.dispense(protocol.params.transfer_volume, well.bottom(1))
                
                    ## Update plate_stat
                    parent_plate = well.parent
                    plate_states[parent_plate][well] = color
                                 
            # Return tip to tip rack            
            p20.return_tip()
            ## When 2 racks of tips have been used, reset the tip racks
            if tip_counter % 192 == 0:
                p20.reset_tipracks()
                
            #Update the height of colored liquid
            current_heights[color] = current_height
    
    ### Empty all plates at the end           
    protocol.comment("Ik haal nu alle platen leeg")
    # Group wells by color
    wells_by_color = {}
    for plate in plate_states:
        for well, color in plate_states[plate].items():
            if color not in wells_by_color:
                wells_by_color[color] = []
            wells_by_color[color].append(well)
    # Empty color by color
    for color, wells_to_empty in wells_by_color.items():
        # Skip unused colors
        if not wells_to_empty: 
            continue
        # Destination
        color_source_tube = color_sources[color]
        current_height = current_heights[color]
        
        # Pick up a tip
        p20.pick_up_tip()
        tip_counter += 1
        
        # Empty all wells with the apropriate color. Empty multiple wells at once and return to color tube
        batch_size = int(p20.max_volume // protocol.params.transfer_volume)
        for batch_start in range(0, len(wells_to_empty), batch_size):
            batch = wells_to_empty[batch_start:batch_start + batch_size]
            batch_volume = protocol.params.transfer_volume * len(batch)
            
            # Volume tracking
            current_height, pip_height, bottom_reached = VT.volume_tracking('15mL_tubes',                                                                
                                                                            batch_volume,
                                                                            current_height, 
                                                                            'filling')
            # Aspirate from multiple wells                    
            for well in batch:
                p20.aspirate(protocol.params.transfer_volume,
                              well.bottom())   
            # Return all at once
            p20.dispense(batch_volume, color_source_tube.bottom(current_height))
            p20.blow_out(color_source_tube.top(-2))
                    
        # Return tip to tip rack            
        p20.return_tip()
        ## When 2 racks of tips have been used, reset the tip racks
        if tip_counter % 192 == 0:
            p20.reset_tipracks()
    
        #Update the height of colored liquid
        current_heights[color] = current_height

    # Clear plate state after emptying
    plate_states[plate] = {}


# =============================================================================
# LIGHTS OFF===================================================================
# =============================================================================
    protocol.set_rail_lights(False)
# =============================================================================
    