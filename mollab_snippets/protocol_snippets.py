"""
A file with snippets of code
"""

# LOADING PIPETTES AND TIPS====================================================
#Pipette - p20
p20 = protocol.load_instrument(
    'p20_single_gen2',                  
    'left',                             
    tip_racks=tips_20)
#Pipette - p300
p300 = protocol.load_instrument(
    'p300_single_gen2',                  
    'right',                             
    tip_racks=tips_y)
#-->tips_200 if using Opentrons, tips_300 if using TipOne

# NOTE: locations are set to y, you'll need to change these in your protocol

#Pipette tips - TipOne 20
if simulate:
    with open("labware/tipone_96_tiprack_20ul/"
              "tipone_96_tiprack_20ul.json") as labware_file:
            labware_def_tipone_96_tiprack_20ul = json.load(labware_file)
    tips_20_1 = protocol.load_labware_from_definition(
        labware_def_tipone_96_tiprack_20ul,
        y,                                  
        'tipone_20tips_1')
    tips_20_2 = protocol.load_labware_from_definition(
        labware_def_tipone_96_tiprack_20ul,
        y,                                  
        'tipone_20tips_2')
    tips_20_3 = protocol.load_labware_from_definition(
        labware_def_tipone_96_tiprack_20ul,
        y,                                  
        'tipone_20tips_3')
    tips_20_4 = protocol.load_labware_from_definition(
        labware_def_tipone_96_tiprack_20ul,
        y,                                  
        'tipone_20tips_4')
else:    
    tips_20_1 = protocol.load_labware(
        'tipone_96_tiprack_20uL',  
        y,                                  
        'tipone_20tips_1')        
    tips_20_2 = protocol.load_labware(
        'tipone_96_tiprack_20uL',  
        y,                                  
        'tipone_20tips_2')
    tips_20_3 = protocol.load_labware(
        'tipone_96_tiprack_20uL',  
        y,                                  
        'tipone_20tips_3')        
    tips_20_4 = protocol.load_labware(
        'tipone_96_tiprack_20uL',  
        y,                                  
        'tipone_20tips_4')       
tips_20 = [tips_20_1, tips_20_2, tips_20_3, tips_20_4]

#Pipette tips - TipOne 300
if simulate:
    with open("labware/tipone_96_tiprack_300uL/"
              "tipone_96_tiprack_300uL.json") as labware_file:
            labware_def_tipone_96_tiprack_300uL = json.load(labware_file)
    tips_300_1 = protocol.load_labware_from_definition(
        labware_def_tipone_96_tiprack_300uL,
        y,                                  
        'tipone_300tips_1')
    tips_300_2 = protocol.load_labware_from_definition(
        labware_def_tipone_96_tiprack_300uL,
        y,                                  
        'tipone_300tips_2')
    tips_300_3 = protocol.load_labware_from_definition(
        labware_def_tipone_96_tiprack_300uL,
        y,                                  
        'tipone_300tips_3')
    tips_300_4 = protocol.load_labware_from_definition(
        labware_def_tipone_96_tiprack_300uL,
        y,                                  
        'tipone_300tips_4')
else:    
    tips_300_1 = protocol.load_labware(
        'tipone_96_tiprack_300uL',  
        y,                                  
        'tipone_300tips_1')        
    tips_300_2 = protocol.load_labware(
        'tipone_96_tiprack_300uL',  
        y,                                  
        'tipone_300tips_2')
    tips_300_3 = protocol.load_labware(
        'tipone_96_tiprack_300uL',  
        y,                                  
        'tipone_300tips_3')        
    tips_300_4 = protocol.load_labware(
        'tipone_96_tiprack_300uL',  
        y,                                  
        'tipone_300tips_4')    
tips_300 = [tips_300_1, tips_300_2, tips_300_3, tips_300_4]

#Pipette tips - Opentrons 20
tips_20_1 = protocol.load_labware(
    'opentrons_96_filtertiprack_20ul',  
    y,                                  
    '20tips_1')        
tips_20_2 = protocol.load_labware(
    'opentrons_96_filtertiprack_20ul',  
    y,                                  
    '20tips_2')
tips_20_3 = protocol.load_labware(
    'opentrons_96_filtertiprack_20ul',  
    y,                                  
    '20tips_3')        
tips_20_4 = protocol.load_labware(
    'opentrons_96_filtertiprack_20ul',  
    y,                                  
    '20tips_4')   
tips_20 = [tips_20_1, tips_20_2, tips_20_3, tips_20_4]


#Pipette tips - Opentrons 200
tips_200_1 = protocol.load_labware(
    'opentrons_96_filtertiprack_200ul',  
    y,                                  
    '200tips_1')        
tips_200_2 = protocol.load_labware(
    'opentrons_96_filtertiprack_200ul',  
    y,                                  
    '200tips_2')
tips_200_3 = protocol.load_labware(
    'opentrons_96_filtertiprack_200ul',  
    y,                                  
    '200tips_3')        
tips_200_4 = protocol.load_labware(
    'opentrons_96_filtertiprack_200ul',  
    y,                                  
    '200tips_4')   
tips_200 = [tips_200_1, tips_200_2, tips_200_3, tips_200_4]
# =============================================================================

# LOADING LABWARE==============================================================
# NOTES: 
# copy-paste the protocol snippet in your protocol 
# after pasting, select the protocol snippet, use CTRL-R to find and replace:
#   the 'xx' by primer or sample or reagent or water
#   the '-' by source or destination
#   when not specifying the type replace 'xx_-' by source or destination
# locations are set to y, you'll need to change these in your protocol

#plate_96 (BioRad skirted plate)
if xx_tube_type == 'plate_96':
    xx_-_1 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    
        y,                                  
        'xx_-_1_plate_96')
    xx_-_2 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    
        y,                                  
        'xx_-_2_plate_96')
    xx_-_3 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    
        y,                                  
        'xx_-_3_plate_96')
    xx_-_4 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',    
        y,                                  
        'xx_-_4_plate_96')

#cool_rack_plate_96 (BioRad skirted plate in Eppendorf cooler)
if xx_tube_type == 'cool_rack_plate_96':
    if simulate:
        with open("labware/biorad_qpcr_plate_eppendorf_cool_rack/"
                  "biorad_qpcr_plate_eppendorf_cool_rack.json") as labware_file:
                labware_def_biorad_qpcr_plate_eppendorf_cool_rack = json.load(labware_file)
        xx_-_1 = protocol.load_labware_from_definition( 
            labware_def_biorad_qpcr_plate_eppendorf_cool_rack,     
            y,     
            'xx_-_1_cool_rack_plate_96')                    
        xx_-_2 = protocol.load_labware_from_definition( 
            labware_def_biorad_qpcr_plate_eppendorf_cool_rack,     
            y,                         
            'xx_-_2_cool_rack_plate_96') 
        xx_-_3 = protocol.load_labware_from_definition( 
            labware_def_biorad_qpcr_plate_eppendorf_cool_rack,     
            y,                         
            'xx_-_3_cool_rack_plate_96') 
        xx_-_4 = protocol.load_labware_from_definition( 
            labware_def_biorad_qpcr_plate_eppendorf_cool_rack,     
            y,                         
            'xx_-_4_cool_rack_plate_96') 
    else:
        xx_-_1 = protocol.load_labware(
            'biorad_qpcr_plate_eppendorf_cool_rack',
            y,
            'xx_-_1_cool_rack_plate_96')
        xx_-_2 = protocol.load_labware(
            'biorad_qpcr_plate_eppendorf_cool_rack',
            y,
            'xx_-_2_cool_rack_plate_96')
        xx_-_3 = protocol.load_labware(
            'biorad_qpcr_plate_eppendorf_cool_rack',
            y,
            'xx_-_3_cool_rack_plate_96')
        xx_-_4 = protocol.load_labware(
            'biorad_qpcr_plate_eppendorf_cool_rack',
            y,
            'xx_-_4_cool_rack_plate_96')
        
#NIOZ_plate_96 (BioRad skirted plate in NIOZ plate holder)
if xx_tube_type == 'NIOZ_plate_96':
    if simulate:
        with open("labware/biorad_qpcr_plate_nioz_plateholder/"
                  "biorad_qpcr_plate_nioz_plateholder.json") as labware_file:
                labware_def_biorad_qpcr_plate_nioz_plateholder = json.load(labware_file)
        xx_-_1 = protocol.load_labware_from_definition( 
            labware_def_biorad_qpcr_plate_nioz_plateholder,     
            y,                         
            'xx_-_1_NIOZ_plate_96')
        xx_-_2 = protocol.load_labware_from_definition( 
            labware_def_biorad_qpcr_plate_nioz_plateholder,     
            y,                         
            'xx_-_2_NIOZ_plate_96')   
        xx_-_3 = protocol.load_labware_from_definition( 
            labware_def_biorad_qpcr_plate_nioz_plateholder,     
            y,                         
            'xx_-_3_NIOZ_plate_96')   
        xx_-_4 = protocol.load_labware_from_definition( 
            labware_def_biorad_qpcr_plate_nioz_plateholder,     
            y,                         
            'xx_-_4_NIOZ_plate_96')   
    else:        
        xx_-_1 = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',
            y,
            'xx_-_1_NIOZ_plate_96')        
        xx_-_2 = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',
            y,
            'xx_-_2_NIOZ_plate_96')
        xx_-_3 = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',
            y,
            'xx_-_3_NIOZ_plate_96')
        xx_-_4 = protocol.load_labware(
            'biorad_qpcr_plate_nioz_plateholder',
            y,
            'xx_-_4_NIOZ_plate_96')
        
#non_skirted_plate_96 (Thermo non-skirted plate in BioRad skirted plate)
if xx_tube_type == 'non_skirted_plate_96':
    if simulate:
        with open("labware/thermononskirtedinbioradskirted_96_wellplate_200ul/"
                  "thermononskirtedinbioradskirted_96_wellplate_200ul.json") as labware_file:
                labware_def_thermononskirtedinbioradskirted_96_wellplate_200ul = json.load(labware_file)
        xx_-_1 = protocol.load_labware_from_definition( 
            labware_def_thermononskirtedinbioradskirted_96_wellplate_200ul,     
            y,                         
            'xx_-_1_non_skirted_plate_96')   
        xx_-_2 = protocol.load_labware_from_definition( 
            labware_def_thermononskirtedinbioradskirted_96_wellplate_200ul,     
            y,                         
            'xx_-_2_non_skirted_plate_96')   
        xx_-_3 = protocol.load_labware_from_definition( 
            labware_def_thermononskirtedinbioradskirted_96_wellplate_200ul,     
            y,                         
            'xx_-_3_non_skirted_plate_96')   
        xx_-_4 = protocol.load_labware_from_definition( 
            labware_def_thermononskirtedinbioradskirted_96_wellplate_200ul,     
            y,                         
            'xx_-_4_non_skirted_plate_96')   
    else:
        xx_-_1 = protocol.load_labware(
            'thermononskirtedinbioradskirted_96_wellplate_200ul',
            y,
            'xx_-_1_non_skirted_plate_96')        
        xx_-_2 = protocol.load_labware(
            'thermononskirtedinbioradskirted_96_wellplate_200ul',
            y,
            'xx_-_2_non_skirted_plate_96')    
        xx_-_3 = protocol.load_labware(
            'thermononskirtedinbioradskirted_96_wellplate_200ul',
            y,
            'xx_-_3_non_skirted_plate_96')  
        xx_-_4 = protocol.load_labware(
            'thermononskirtedinbioradskirted_96_wellplate_200ul',
            y,
            'xx_-_4_non_skirted_plate_96')  

#PCR_strips (Westburg flat-cap strips or similar in BioRad skirted plate)      
if xx_tube_type == 'PCR_strips':
    if simulate:
        with open("labware/pcrstrips_96_wellplate_200ul/"
                  "pcrstrips_96_wellplate_200ul.json") as labware_file:
                labware_def_pcrstrip_96_wellplate_200ul = json.load(labware_file)
        xx_-_1 = protocol.load_labware_from_definition(
                labware_def_pcrstrips_96_wellplate_200ul,
                y,
                'xx_-_1_PCR_strips')
        xx_-_2 = protocol.load_labware_from_definition(
                labware_def_pcrstrips_96_wellplate_200ul,
                y,
                'xx_-_2_PCR_strips')
        xx_-_3 = protocol.load_labware_from_definition(
                labware_def_pcrstrips_96_wellplate_200ul,
                y,
                'xx_-_3_PCR_strips')
        xx_-_4 = protocol.load_labware_from_definition(
                labware_def_pcrstrips_96_wellplate_200ul,
                y,
                'xx_-_4_PCR_strips')
    else:
        xx_-_1 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                y,                                      
                'xx_-_1_PCR_strips') 
        xx_-_2 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                y,                                      
                'xx_-_2_PCR_strips') 
        xx_-_3 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                y,                                      
                'xx_-_3_PCR_strips')
        xx_-_4 = protocol.load_labware(
                'pcrstrips_96_wellplate_200ul',         
                y,                                      
                'xx_-_4_PCR_strips') 
        
#tubes_1.5mL
if xx_tube_type == 'tubes_1.5mL':
    xx_-_1 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',         
            y,                                      
            'xx_-_1_tubes_1.5mL') 
    xx_-_2 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',         
            y,                                      
            'xx_-_2_tubes_1.5mL') 
    xx_-_3 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',         
            y,                                      
            'xx_-_3_tubes_1.5mL')
    xx_-_4 = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',         
            y,                                      
            'xx_-_4_tubes_1.5mL') 

#tubes_5mL - screw cap
if xx_tube_type == 'tubes_5mL':
    if simulate:
        with open("labware/eppendorfscrewcap_15_tuberack_5000ul/"
                  "eppendorfscrewcap_15_tuberack_5000ul.json") as labware_file:
                labware_def_eppendorfscrewcap_15_tuberack_5000ul = json.load(labware_file)
        xx_-_1 = protocol.load_labware_from_definition(
                labware_def_eppendorfscrewcap_15_tuberack_5000ul,
                y,
                'xx_-_1_tubes_5mL')
        xx_-_2 = protocol.load_labware_from_definition(
                labware_def_eppendorfscrewcap_15_tuberack_5000ul,
                y,
                'xx_-_2_tubes_5mL')
        xx_-_3 = protocol.load_labware_from_definition(
                labware_def_eppendorfscrewcap_15_tuberack_5000ul,
                y,
                'xx_-_3_tubes_5mL')
        xx_-_4 = protocol.load_labware_from_definition(
                labware_def_eppendorfscrewcap_15_tuberack_5000ul,
                y,
                'xx_-_4_tubes_5mL')
    else:
        xx_-_1 = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',         
                y,                                      
                'xx_-_1_tubes_5mL') 
        xx_-_2 = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',         
                y,                                      
                'xx_-_2_tubes_5mL') 
        xx_-_3 = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',         
                y,                                      
                'xx_-_3_tubes_5mL')
        xx_-_4 = protocol.load_labware(
                'eppendorfscrewcap_15_tuberack_5000ul',         
                y,                                      
                'xx_-_4_tubes_5mL') 

#tubes_5mL_snap - snap cap
if xx_tube_type == 'tubes_5mL_snap':
    if simulate:
        with open("labware/eppendorf_15_tuberack_5000ul/"
                  "eppendorf_15_tuberack_5000ul.json") as labware_file:
                labware_def_eppendorf_15_tuberack_5000ul = json.load(labware_file)
        xx_-_1 = protocol.load_labware_from_definition(
                labware_def_eppendorf_15_tuberack_5000ul,
                y,
                'xx_-_1_tubes_5mL_snap')
        xx_-_2 = protocol.load_labware_from_definition(
                labware_def_eppendorf_15_tuberack_5000ul,
                y,
                'xx_-_2_tubes_5mL_snap')
        xx_-_3 = protocol.load_labware_from_definition(
                labware_def_eppendorf_15_tuberack_5000ul,
                y,
                'xx_-_3_tubes_5mL_snap')
        xx_-_4 = protocol.load_labware_from_definition(
                labware_def_eppendorf_15_tuberack_5000ul,
                y,
                'xx_-_4_tubes_5mL_snap')
    else:
        xx_-_1 = protocol.load_labware(
                'eppendorf_15_tuberack_5000ul',         
                y,                                      
                'xx_-_1_tubes_5mL_snap') 
        xx_-_2 = protocol.load_labware(
                'eppendorf_15_tuberack_5000ul',         
                y,                                      
                'xx_-_2_tubes_5mL_snap') 
        xx_-_3 = protocol.load_labware(
                'eppendorf_15_tuberack_5000ul',         
                y,                                      
                'xx_-_3_tubes_5mL_snap')
        xx_-_4 = protocol.load_labware(
                'eppendorf_15_tuberack_5000ul',         
                y,                                      
                'xx_-_4_tubes_5mL_snap') 
        
#tubes_15mL
if xx_tube_type == 'tubes_15mL':
    xx_-_1 = protocol.load_labware(
            'opentrons_15_tuberack_falcon_15ml_conical',         
            y,                                      
            'xx_-_1_tubes_15mL') 
    xx_-_2 = protocol.load_labware(
            'opentrons_15_tuberack_falcon_15ml_conical',         
            y,                                      
            'xx_-_2_tubes_15mL') 
    xx_-_3 = protocol.load_labware(
            'opentrons_15_tuberack_falcon_15ml_conical',         
            y,                                      
            'xx_-_3_tubes_15mL')
    xx_-_4 = protocol.load_labware(
            'opentrons_15_tuberack_falcon_15ml_conical',         
            y,                                      
            'xx_-_4_tubes_15mL') 

#tubes_50mL
if xx_tube_type == 'tubes_50mL':
    xx_-_1 = protocol.load_labware(
            'opentrons_6_tuberack_falcon_50ml_conical',         
            y,                                      
            'xx_-_1_tubes_50mL') 
    xx_-_2 = protocol.load_labware(
            'opentrons_6_tuberack_falcon_50ml_conical',         
            y,                                      
            'xx_-_2_tubes_50mL') 
    xx_-_3 = protocol.load_labware(
            'opentrons_6_tuberack_falcon_50ml_conical',         
            y,                                      
            'xx_-_3_tubes_50mL')
    xx_-_4 = protocol.load_labware(
            'opentrons_6_tuberack_falcon_50ml_conical',         
            y,                                      
            'xx_-_4_tubes_50mL')
# =============================================================================