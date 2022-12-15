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
  

# TIPS, TUBES & LOCATIONS======================================================

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
    ##   (eppendorf snap cap 5mL tubes)
    ## water_tube_type = 'tubes_15mL'
    ##   (greiner bio or VWR 15mL screw cap tubes)
    ## water_tube_type = 'tubes_50mL'
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