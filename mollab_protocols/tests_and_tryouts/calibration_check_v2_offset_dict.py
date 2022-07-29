# =============================================================================
# Creation date: 211122
# Description: short protocol to check if the calibration is ok.
# =============================================================================


# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.
import pandas as pd

# =============================================================================


# VARIABLES TO SET=============================================================
# =============================================================================
pipette20 = True
p20_start_tip = 'A1'
pipette300 = True
p300_start_tip = 'A1'
plate = True
plate_on_rack = True #Plate on NIOZ plateholder
strips = True
tubes = True #Tubes 1.5mL
tubes5mL = True
tubes15mL = True
tubes50mL = True
test_wells = True #Test 3 wells spread over the labware
test_columns = False #Test 3 columns spread over the labware
# =============================================================================


# RUN==========================================================================
# =============================================================================
##### Metadata
metadata = {
    'protocolName': 'calibration_check_v2_offset_dict',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('Checks if the bottom of the tubes is not touched'),
    'apiLevel': '2.12'}

##### Define function
def run(protocol: protocol_api.ProtocolContext):
    """
    Pick up p20 and/or p300 tips, followed by touch bottom of tubes 
    of different labware
    """
# =============================================================================
    if not protocol.is_simulating:
        offsets = pd.read_csv(
            "data/user_storage/mollab_modules/labware_offset.csv", 
            sep=';'
            )
        offsets = offsets.set_index('labware')

# LOADING LABWARE==============================================================
# =============================================================================
    labwares = {}
      ## empty dict to add labware and labware_names to, to loop through
    
    ##### Loading pipettetips
    if pipette300:
        tips_200 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  
            10,                                  
            '200tips')
        labwares[tips_200] = 'filtertips_200'
        
                         
    if pipette20:
        tips_20 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            11,                                 
            '20tips')                           
        labwares[tips_20] = 'filtertips_20'

    ##### Loading labware
    if plate:
        plate_96 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            1,
            '96well_plate')
        labwares[plate_96] = 'plate_96'

    if plate_on_rack:
        plate_plateholder = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',
            2,
            '96well_plate_on_plateholder')
        labwares[plate_plateholder] = 'plate_plateholder'


    if strips:                                          
        pcr_strips = protocol.load_labware(
            'pcrstrips_96_wellplate_200ul',     
            3,                                 
            'pcr_strips')                   
        labwares[pcr_strips] = 'pcr_strips'

    if tubes:
        sample_tubes = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            4,                                                       
            'sample_tubes')
        labwares[sample_tubes] = '1.5mL_tubes'

    if tubes5mL:
        tubes_5mL = protocol.load_labware(
            'eppendorfscrewcap_15_tuberack_5000ul', 
            5,                                      
            'tubes_5mL')
        labwares[tubes_5mL] = '5mL_screw_cap'

    if tubes15mL or tubes50mL:
        large_tubes = protocol.load_labware(
            'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', 
            6,                                      
            'large_tubes')
        labwares[large_tubes] = '15mL_50mLtubes'
       
        
    ##### Loading pipettes
    if pipette300:
        p300 = protocol.load_instrument(
            'p300_single_gen2',                  
            'right',                            
            tip_racks=[tips_200])               
    if pipette20:
        p20 = protocol.load_instrument(
            'p20_single_gen2',                 
            'left',                            
            tip_racks=[tips_20])                
# =============================================================================


# LABWARE OFFSET===============================================================    
# =============================================================================
    if not protocol.is_simulating:    
        for labware in labwares:
            offset_x = offsets.at[labwares[labware],'x_offset']
            offset_y = offsets.at[labwares[labware],'y_offset']
            offset_z = offsets.at[labwares[labware],'z_offset']
            labware.set_offset(
                x = offset_x, 
                y = offset_y, 
                z = offset_z)
# =============================================================================


# START-UP=====================================================================    
# =============================================================================
    protocol.set_rail_lights(True)
      ## turn on lights 
    
    if pipette300:
        p300.starting_tip = tips_200.well(p300_start_tip)
          ## define first tip
        p300.pick_up_tip()
          ## pick up first tip
    if pipette20:
        p20.starting_tip = tips_20.well(p20_start_tip)
          ## define first tip
        p20.pick_up_tip()
          ## pick up first tip
# =============================================================================


# test labwares
# =============================================================================
    # Loop through all labware    
    for labware in labwares:
        # If the labware is not a tip rack
        if labware != tips_20 and labware != tips_200:
            
            # append appropriate wells to a list
            wells = []
            if test_wells:
                all_wells = labware.wells()
                total_number_of_wells = len(all_wells)
                middle = int(total_number_of_wells / 2)
                wells.append(all_wells[0])
                wells.append(all_wells[middle])
                wells.append(all_wells[-1])
                  ## pick 3 wells, nicely distributed of the labware
            if test_columns:
                all_columns = labware.columns()
                total_number_of_columns = len(all_columns)
                middle = int(total_number_of_columns / 2)
                columns = []
                columns.append(all_columns[0])
                columns.append(all_columns[middle])
                columns.append(all_columns[-1])
                  ## pick 3 columns, nicely distributed of the labware
                for column in columns:
                    for well in column:
                        wells.append(well)
            
            # test wells
            for well in wells:
                if pipette300:
                    p300.move_to(well.bottom())
                    protocol.delay(seconds=1)
            for well in wells:
                if pipette20:
                    p20.move_to(well.bottom()) 
                    protocol.delay(seconds=1)
# =============================================================================
    
# SHUT DOWN====================================================================
# =============================================================================
    if pipette300:
        p300.return_tip()
    if pipette20:
        p20.return_tip()
    protocol.set_rail_lights(False)
# =============================================================================