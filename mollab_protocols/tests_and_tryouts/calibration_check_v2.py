# =============================================================================
# Creation date: 211122
# Description: short protocol to check if the calibration is ok.
# =============================================================================

# IMPORT STATEMENTS============================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
# =============================================================================

# VARIABLES TO SET=============================================================
pipette20 = True
p20_start_tip = 'A1'
pipette300 = True
p300_start_tip = 'A1'
plate = True
plate_on_rack = True #plate on coolrack
strips = True
tubes = True #Tubes 1.5mL
tubes5mL = True
# =============================================================================

# RUN==========================================================================
##### Metadata
metadata = {
    'protocolName': 'Calibration check v2',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('Checks if the bottom of the tubes is not touched'),
    'apiLevel': '2.9'}

##### Define function
def run(protocol: protocol_api.ProtocolContext):
    """
    Pick up p20 and/or p300 tips, followed by touch bottom of tubes 
    of different labware
    """
# =============================================================================

# LOADING LABWARE==============================================================
    if pipette300:
        tips_200 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  #labware definition
            10,                                  #deck position
            '200tips')                           #custom name
    if pipette20:
        tips_20 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  #labware definition
            11,                                 #deck position
            '20tips')                           #custom name
    if plate:
        plate_96 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            1,
            '96well_plate')
    if plate_on_rack:
        high_plate_96 = protocol.load_labware(
            'biorad_qpcr_plate_eppendorf_cool_rack',
            2,
            '96well_plate_rack')
    if tubes:
        sample_tubes = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
            4,                                                       #deck position
            'sample_tubes')
    if strips:                                          #custom name
        pcr_strips = protocol.load_labware(
            'pcrstrips_96_wellplate_200ul',     #labware definition
            3,                                  #deck position
            'pcr_strips')                       #custom name
    if tubes5mL:
        tubes_5mL = protocol.load_labware(
            'eppendorfscrewcap_15_tuberack_5000ul', #labware definition
            5,                                      #deck position 
            'tubes_5mL')                            #custom name
    
    ##### Loading pipettes
    if pipette300:
        p300 = protocol.load_instrument(
            'p300_single_gen2',                  #instrument definition
            'right',                             #mount position
            tip_racks=[tips_200])                #assigned tiprack
    if pipette20:
        p20 = protocol.load_instrument(
            'p20_single_gen2',                  #instrument definition
            'left',                             #mount position
            tip_racks=[tips_20])                #assigned tiprack
# =============================================================================

# PREDEFINED VARIABLES=========================================================    
    protocol.set_rail_lights(True)
    
    if pipette300:
        p300.starting_tip = tips_200.well(p300_start_tip)
        p300.pick_up_tip()
    if pipette20:
        p20.starting_tip = tips_20.well(p20_start_tip)
        p20.pick_up_tip()
# =============================================================================


# test PCR plate
# =============================================================================
    
    # wells
    aspiration_location_wells = []
    aspiration_wells = (
        [plate_96.wells_by_name()[well_name] for well_name in 
          ['A1', 'A7', 'A11']])
    for well in aspiration_wells:
        aspiration_location_wells.append(well)
            
    for well in aspiration_location_wells:
        p300.aspirate(10, well)
        p300.dispense(10, well)
        p300.blow_out(well)
        p20.aspirate(10, well)
        p20.dispense(10, well)
        p20.blow_out(well)

    protocol.pause('was this ok?')  
    
    # columns
    aspiration_location_columns = []
    aspiration_columns = (
        [plate_96.columns_by_name()[column_name] for column_name in
          ['2', '6', '12']]
        )
    for column in aspiration_columns:
        for well in column:
            aspiration_location_columns.append(well)
    
    for well in aspiration_location_columns:
        p300.aspirate(10, well)
        p300.dispense(10, well)
        p300.blow_out(well)
        p20.aspirate(10, well)
        p20.dispense(10, well)
        p20.blow_out(well)

    protocol.pause('was this ok?')    

# =============================================================================
# test PCR plate + rack
# =============================================================================
    
    # wells
    aspiration_location_wells = []
    aspiration_wells = (
        [high_plate_96.wells_by_name()[well_name] for well_name in 
          ['A1', 'A7', 'A11']])
    for well in aspiration_wells:
        aspiration_location_wells.append(well)
            
    for well in aspiration_location_wells:
        p300.aspirate(10, well)
        p300.dispense(10, well)
        p300.blow_out(well)
        p20.aspirate(10, well)
        p20.dispense(10, well)
        p20.blow_out(well)
    
    protocol.pause('was this ok?')    
    
    # columns
    aspiration_location_columns = []
    aspiration_columns = (
        [high_plate_96.columns_by_name()[column_name] for column_name in
          ['2', '6', '12']]
        )
    for column in aspiration_columns:
        for well in column:
            aspiration_location_columns.append(well)
    
    for well in aspiration_location_columns:
        p300.aspirate(10, well)
        p300.dispense(10, well)
        p300.blow_out(well)
    for well in aspiration_location_columns:
        p20.aspirate(10, well)
        p20.dispense(10, well)
        p20.blow_out(well)

    protocol.pause('was this ok?')    


# =============================================================================
# test 1.5mL tubes
# =============================================================================
    aspiration_location = []
    aspiration_columns = (
        [sample_tubes.columns_by_name()[column_name] for column_name in 
          ['1', '4', '6']]
        )
    for column in aspiration_columns:
        for well in column:
            aspiration_location.append(well)
    
    for well in aspiration_location:
        # p300.aspirate(10, well)
        # p300.dispense(10, well)
        # p300.blow_out(well)
        p20.aspirate(10, well)
        p20.dispense(10, well)
        p20.blow_out(well)

    protocol.pause('was this ok?')    
    
# =============================================================================
# test PCR tube strips
# =============================================================================
    
    # wells
    aspiration_location_wells = []
    aspiration_wells = (
        [pcr_strips.wells_by_name()[well_name] for well_name in 
          ['A1', 'A7', 'A11']])
    for well in aspiration_wells:
        aspiration_location_wells.append(well)
            
    for well in aspiration_location_wells:
        p300.aspirate(10, well)
        p300.dispense(10, well)
        p300.blow_out(well)
        p20.aspirate(10, well)
        p20.dispense(10, well)
        p20.blow_out(well)

    # protocol.pause('was this ok?')  
    
    columns
    aspiration_location_columns = []
    aspiration_columns = (
        [pcr_strips.columns_by_name()[column_name] for column_name in
          ['1', '7', '11']]
        )
    for column in aspiration_columns:
        for well in column:
            aspiration_location_columns.append(well)
    
    for well in aspiration_location_columns:
        p300.aspirate(10, well)
        p300.dispense(10, well)
        p300.blow_out(well)
        p20.aspirate(10, well)
        p20.dispense(10, well)
        p20.blow_out(well)

    protocol.pause('was this ok?')       
    
# =============================================================================
# test 5mL (screw cap) tube
# =============================================================================
    p300.aspirate(10, tubes_5mL['A1'])
    p300.dispense(10, tubes_5mL['A1'])
    p300.blow_out(tubes_5mL['A1'])
    p20.aspirate(10, tubes_5mL['A1'])
    p20.dispense(10, tubes_5mL['A1'])
    p20.blow_out(tubes_5mL['A1'])
    
    p300.aspirate(10, tubes_5mL['C5'])
    p300.dispense(10, tubes_5mL['C5'])
    p300.blow_out(tubes_5mL['C5'])
    p20.aspirate(10, tubes_5mL['C5'])
    p20.dispense(10, tubes_5mL['C5'])
    p20.blow_out(tubes_5mL['C5'])
    

    protocol.pause('was this ok?')    
 
    
# =============================================================================
# =============================================================================
    p300.return_tip()
    p20.return_tip()
    protocol.set_rail_lights(False)