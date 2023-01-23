"""
A file with standard names for variables
"""
# OTHERS ======================================================================
# How many samples do you have? 
number_of_samples = 96

# Do you want to simulate the protocol?
simulate = True
  ## True for simulating protocol, False for robot protocol. 
# =============================================================================
  

# TIP LOCATIONS - TUBE TYPE & LOCATION=========================================

# What is the starting position of the first 20µL tip?
starting_tip_p20 = 'A1'
# What is the starting position of the first 200µL/300µL tip?
starting_tip_p300 = 'A1'

# What is the location of your first sample? 
first_sample = 'A1'
    ## 'A1' is standard for tubes and plates 
    ## 'A2' is standard for PCR_strips

# What labware are your samples in?
sample_tube_type = 'plate_96'
# Options: 
    ## sample_tube_type = 'plate_96' 
    ##   (BioRad skirted plate)
    ## sample_tube_type = 'cool_rack_plate_96' 
    ##   (BioRad skirted plate in Eppendorf cooler)
    ## sample_tube_type = 'NIOZ_plate_96' 
    ##   (BioRad skirted plate in NIOZ plate holder)
    ## sample_tube_type = 'non_skirted_plate_96' 
    ##   (Thermo non-skirted plate in BioRad skirted plate)
    ## sample_tube_type = 'PCR_strips' 
    ##   (Westburg flat-cap strips or similar in BioRad skirted plate)
    ## sample_tube_type = 'tubes_1.5mL'
    ##   (any 1.5mL tubes)   
# When using PCR strips as sample_tube_type:
sample_columns = ['2', '5', '8', '11']
# Options: 
    ## 3 strips per rack: ['2', '7', '11'] 
    ## 4 strips per rack: ['2', '5', '8','11'] = STANDARD
    ## 6 strips per rack: ['1', '3', '5', '7', '9', '11']       

# What labware are your primers in?
primer_tube_type = 'plate_96'
# Options: 
    ## primer_tube_type = 'plate_96' 
    ##   (BioRad skirted plate)
    ## primer_tube_type = 'cool_rack_plate_96' 
    ##   (BioRad skirted plate in Eppendorf cooler)
    ## primer_tube_type = 'NIOZ_plate_96' 
    ##   (BioRad skirted plate in NIOZ plate holder)
    ## primer_tube_type = 'non_skirted_plate_96' 
    ##   (Thermo non-skirted plate in BioRad skirted plate)
    ## primer_tube_type = 'PCR_strips' 
    ##   (Westburg flat-cap strips or similar in BioRad skirted plate)
    ## primer_tube_type = 'tubes_1.5mL'
    ##   (any 1.5mL tubes)  
# When using PCR strips as primer_tube_type:
primer_columns = ['2', '5', '8', '11']
# Options: 
    ## 3 strips per rack: ['2', '7', '11'] 
    ## 4 strips per rack: ['2', '5', '8','11'] = STANDARD
    ## 6 strips per rack: ['1', '3', '5', '7', '9', '11']
    
# What labware is you reagent in?
reagent_tube_type = 'tubes_1.5mL'
# Options: 
    ## reagent_tube_type = 'tubes_1.5mL'
    ##   (any 1.5mL tubes)  
    ## reagent_tube_type = 'tubes_5mL'
    ##   (eppendorf screw cap 5mL tubes, clear or dark)
    ## reagent_tube_type = 'tubes_5mL_snap'
    ##   (eppendorf snap cap 5mL tubes, clear or dark)
    ## reagent_tube_type = 'tubes_5mL_snap'
    ##   (eppendorf snap cap 5mL tubes)
    ## reagent_tube_type = 'tubes_15mL'
    ##   (greiner bio or VWR 15mL screw cap tubes)
    ## reagent_tube_type = 'tubes_50mL'
    ##   (greiner bio or VWR 50mL screw cap tubes)


# What labware is you water in?
water_tube_type = 'tubes_1.5mL'
# Options: 
    ## water_tube = 'tubes_1.5mL'
    ##   (any 1.5mL tubes)  
    ## water_tube_type = 'tubes_5mL'
    ##   (eppendorf screw cap 5mL tubes, clear or dark)
    ## water_tube_type = 'tubes_5mL_snap'
    ##   (eppendorf snap cap 5mL tubes, clear or dark)
    ## water_tube_type = 'tubes_5mL_snap'
    ##   (eppendorf snap cap 5mL tubes)
    ## water_tube_type = 'tubes_15mL'
    ##   (greiner bio or VWR 15mL screw cap tubes)
    ## water_tube_type = 'tubes_50mL'
    ##   (greiner bio or VWR 50mL screw cap tubes)

# What is your destination labware?
destination_tube_type == 'plate_96'
# Options: 
    ## destination_tube_type = 'plate_96' 
    ##   (BioRad skirted plate)
    ## destination_tube_type = 'cool_rack_plate_96' 
    ##   (BioRad skirted plate in Eppendorf cooler)
    ## destination_tube_type = 'NIOZ_plate_96' 
    ##   (BioRad skirted plate in NIOZ plate holder)
    ## destination_tube_type = 'non_skirted_plate_96' 
    ##   (Thermo non-skirted plate in BioRad skirted plate)
    ## destination_tube_type = 'PCR_strips' 
    ##   (Westburg flat-cap strips or similar in BioRad skirted plate)
    ## destination_tube_type = 'tubes_1.5mL'
    ##   (any 1.5mL tubes)  
    ## destination_tube_type = 'tubes_5mL'
    ##   (eppendorf screw cap 5mL tubes, clear or dark)
    ## destination_tube_type = 'tubes_5mL_snap'
    ##   (eppendorf snap cap 5mL tubes, clear or dark)
    ## destination_tube_type = 'tubes_5mL_snap'
    ##   (eppendorf snap cap 5mL tubes)
    ## destination_tube_type = 'tubes_15mL'
    ##   (greiner bio or VWR 15mL screw cap tubes)
    ## destination_tube_type = 'tubes_50mL'
    ##   (greiner bio or VWR 50mL screw cap tubes)
# =============================================================================

# VOLUMES======================================================================

# What is the volume of sample that you want to transfer?
sample_trans_vol = 5
sample_mix_vol = 5

# What is the volume of primer that you want to transfer?
primer_trans_vol = 5
primer_mix_vol = 5

# What is the volume of reagent/buffer that you want to transfer?
reagent_trans_vol = 50
reagent_mix_vol = 50
# The total volume of your reagent/buffer that is in your tube.
reagent_vol = 5000

# What is the volume of water that you want to transfer?
water_trans_vol = 50
water_mix_vol = 50
# The total volume of your water that is in your tube.
water_vol = 5000

# NO OF RACKS==================================================================

# How many xx racks are needed? 

# NOTES: 
# copy-paste:
#   if for the first labware 
#   elif loop for all nexxt labwares
# after pasting, select the protocol snippet, use CTRL-R to find and replace:
#   the xx by primer or sample or reagent or water

#if any plate = always if because if it is in the protocol it should be first
if (xx_tube_type == 'plate_96' or 
      xx_tube_type == 'cool_rack_plate_96' or 
      xx_tube_type == 'NIOZ_plate_96' or 
      xx_tube_type == 'non_skirted_plate_96'):
    xx_racks = math.ceil(number_of_xxs / 96)

#if PCR_strips
if xx_tube_type == 'PCR_strips':
    if xx_columns == ['2', '7','11']:
        xx_racks = math.ceil(number_of_xxs / 24)
    elif xx_columns == ['2', '5', '8','11']:
        xx_racks = math.ceil(number_of_xxs / 32)
    elif xx_columns == ['1', '3', '5', '7', '9', '11']:
        xx_racks = math.ceil(number_of_xxs / 48)
#elif PCR_strips
elif xx_tube_type == 'PCR_strips':
    if xx_columns == ['2', '7','11']:
        xx_racks = math.ceil(number_of_xxs / 24)
    elif xx_columns == ['2', '5', '8','11']:
        xx_racks = math.ceil(number_of_xxs / 32)
    elif xx_columns == ['1', '3', '5', '7', '9', '11']:
        xx_racks = math.ceil(number_of_xxs / 48)

#if tubes_1.5mL
if xx_tube_type == 'tubes_1.5mL':
    xx_racks = math.ceil(number_of_xxs / 24)
#elif tubes_1.5mL        
elif sample_tube_type == 'tubes_1.5mL':
    xx_racks = math.ceil(number_of_xxs / 24)
    
#if tubes_5mL
if xx_tube_type == 'tubes_5mL':
    xx_racks = math.ceil(number_of_xxs / 15)
#elif tubes_5mL
elif xx_tube_type == 'tubes_5mL':
    xx_racks = math.ceil(number_of_xxs / 15)

#if tubes_15mL
if xx_tube_type == 'tubes_15mL':
    xx_racks = math.ceil(number_of_xxs / 15)
#elif tubes_15mL
elif xx_tube_type == 'tubes_15mL':
    xx_racks = math.ceil(number_of_xxs / 15)
    
#if tubes_50mL
if xx_tube_type == 'tubes_50mL':
    xx_racks = math.ceil(number_of_xxs / 6)
#elif tubes_50mL
elif xx_tube_type == 'tubes_50mL':
    xx_racks = math.ceil(number_of_xxs / 6)
# =============================================================================

# CONTAINER FOR VOLUME TRACKING================================================
# NOTES: 
# copy-paste 
# after pasting, select the protocol snippet, use CTRL-R to find and replace:
#   the xx by reagent or water
if xx_tube_type == 'tubes_1.5mL':
    container = 'tube_1.5mL'
if xx_tube_type == 'tubes_5mL':
    container = 'tube_5mL'
if xx_tube_type == 'tubes_5mL_snap':
    container = 'tube_5mL_snap'
if xx_tube_type == 'tubes_15mL':
    container = 'tube_15mL'
if xx_tube_type == 'tubes_50mL':
    container = 'tube_50mL'
# =============================================================================    



# Create an empty list to append the wells for the xx_sources to
xx_sources = []
xx_sources_string = []
if xx_tube_type == 'PCR_strips':
    xx_source_columns = (
            ([xx_source_1.columns_by_name()[column_name] 
              for column_name in xx_columns]))
    if xx_racks >= 2:
        xx_columns_2 = (
            ([xx_source_2.columns_by_name()[column_name] 
              for column_name in xx_columns]))
        for column in xx_columns_2:
            xx_source_columns.append(column)
    if xx_racks >= 3:
        xx_columns_3 = (
            ([xx_source_3.columns_by_name()[column_name] 
              for column_name in xx_columns]))
        for column in xx_columns_3:
            xx_source_columns.append(column)
    if xx_racks >= 4:
        xx_columns_4 = (
            ([xx_source_4.columns_by_name()[column_name] 
              for column_name in xx_columns]))
        for column in xx_columns_4:
            xx_source_columns.append(column)
      ## Make a list of columns, this is a list of lists!   
    for column in xx_source_columns:
        for well in column:
            xx_sources.append(well)
            xx_sources_string.append(str(well))
          ## Separate the columns into wells and append them to list 
else:          
    if xx_racks >= 1:
        for well in xx_source_1.wells():
            xx_sources.append(well)
            xx_sources_string.append(str(well))
    if xx_racks >= 2:
        for well in xx_source_2.wells():
            xx_sources.append(well)
            xx_sources_string.append(str(well))
    if xx_racks >= 3:
        for well in xx_source_3.wells():
            xx_sources.append(well)
            xx_sources_string.append(str(well))
    if xx_racks >= 4:
        for well in xx_source_4.wells():
            xx_sources.append(well)
            xx_sources_string.append(str(well))