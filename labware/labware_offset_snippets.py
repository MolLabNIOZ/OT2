import pandas as pd
  ## For accessing offset .csv file


# If not simulated, import the .csv from the robot with robot_specific 
# labware off_set values
if not simulate:
    offsets = pd.read_csv(
        "data/user_storage/mollab_modules/labware_offset.csv", sep=';'
        )
      ## import .csv
    offsets = offsets.set_index('labware')
      ## remove index column

# in de def

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================
    labwares = {}
      ## empty dict to add labware and labware_names to, to loop through
    
      
    ## Examples per labware
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',  
        11,                                  
        '200tips')
    labwares[tips_200] = 'filtertips_200'    
    
    PCR1 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',
        9,
        'PCR1')
    labwares[PCR1] = 'plate_96'
    

# correct naming of labware:
    # filtertips_20
    # filtertips_200
    # plate_96
    # plate_plateholder
    # pcr_strips
    # 1.5mL_tubes
    # 5mL_screw_cap
    # 15mL_tubes
    # 50mL_tubes
    
    
# LABWARE OFFSET===============================================================    
# =============================================================================
    if not simulate:
        for labware in labwares:
            offset_x = offsets.at[labwares[labware],'x_offset']
            offset_y = offsets.at[labwares[labware],'y_offset']
            offset_z = offsets.at[labwares[labware],'z_offset']
            labware.set_offset(
                x = offset_x, 
                y = offset_y, 
                z = offset_z)
# =============================================================================    