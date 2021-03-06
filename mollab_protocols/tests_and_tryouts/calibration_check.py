# =============================================================================
# Author(s): Maartje Brouwer & Sanne Vreugdenhil
# Creation date: 210412
# Description: short protocol to check if the calibration of 1.5mL tubes is ok
#   Sometimes the calibration seems to be a bit off after restart. This short
#   protocol checks if the bottom of the tubes is not touched.
# =============================================================================

##### Import statements
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##

# =============================================================================

##### Metadata
metadata = {
    'protocolName': 'Calibration check 1.5mL tubes 210412',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('Checks if the bottom of the tubes is not touched'),
    'apiLevel': '2.9'}

##### Define function
def run(protocol: protocol_api.ProtocolContext):
    """
    Pick up tip, followed by aspiration and dispension in a 1.5mL tube. 
    Then drop tip.
    """
      
# =============================================================================
    ##### Loading labware
    ## For available labware see "labware/list_of_available_labware".       ##
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',  #labware definition
        10,                                  #deck position
        '200tips')                           #custom name
    tips_20 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        11,                                 #deck position
        '20tips')                           #custom name
    plate_96 = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr',
        1,
        '96well_plate')
    high_plate_96 = protocol.load_labware(
        'biorad_qpcr_plate_eppendorf_cool_rack',
        2,
        '96well_plate_rack')
    sample_tubes = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        4,                                                       #deck position
        'sample_tubes')                                          #custom name
    pcr_strips = protocol.load_labware(
        'pcrstrips_96_wellplate_200ul',     #labware definition
        3,                                  #deck position
        'pcr_strips')                       #custom name
    tubes_5mL = protocol.load_labware(
        'eppendorfscrewcap_15_tuberack_5000ul', #labware definition
        5,                                      #deck position 
        'tubes_5mL')                            #custom name
    
    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                  #instrument definition
        'right',                             #mount position
        tip_racks=[tips_200])                #assigned tiprack
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20])                #assigned tiprack
    
# =============================================================================
    
    protocol.set_rail_lights(True)
    # p300.starting_tip = tips_200.well('A1')
    p20.starting_tip = tips_20.well('A1')
    # p300.pick_up_tip()
    p20.pick_up_tip()
    
# =============================================================================
# test PCR plate
# =============================================================================
    
    # wells
    # aspiration_location_wells = []
    # aspiration_wells = (
    #     [plate_96.wells_by_name()[well_name] for well_name in 
    #       ['A1', 'A7', 'A11']])
    # for well in aspiration_wells:
    #     aspiration_location_wells.append(well)
            
    # for well in aspiration_location_wells:
        # p300.aspirate(10, well)
        # p300.dispense(10, well)
        # p300.blow_out(well)
        # p20.aspirate(10, well)
        # p20.dispense(10, well)
        # p20.blow_out(well)

    # protocol.pause('was this ok?')  
    
    # columns
    # aspiration_location_columns = []
    # aspiration_columns = (
    #     [plate_96.columns_by_name()[column_name] for column_name in
    #       ['2', '6', '12']]
    #     )
    # for column in aspiration_columns:
    #     for well in column:
    #         aspiration_location_columns.append(well)
    
    # for well in aspiration_location_columns:
        # p300.aspirate(10, well)
        # p300.dispense(10, well)
        # p300.blow_out(well)
        # p20.aspirate(10, well)
        # p20.dispense(10, well)
        # p20.blow_out(well)

    # protocol.pause('was this ok?')    

# =============================================================================
# test PCR plate + rack
# =============================================================================
    
    # wells
    # aspiration_location_wells = []
    # aspiration_wells = (
    #     [high_plate_96.wells_by_name()[well_name] for well_name in 
    #       ['A1', 'A7', 'A11']])
    # for well in aspiration_wells:
    #     aspiration_location_wells.append(well)
            
    # for well in aspiration_location_wells:
        # p300.aspirate(10, well)
        # p300.dispense(10, well)
        # p300.blow_out(well)
        # p20.aspirate(10, well)
        # p20.dispense(10, well)
        # p20.blow_out(well)
    
    # protocol.pause('was this ok?')    
    
    # columns
    # aspiration_location_columns = []
    # aspiration_columns = (
    #     [high_plate_96.columns_by_name()[column_name] for column_name in
    #       ['2', '6', '12']]
    #     )
    # for column in aspiration_columns:
    #     for well in column:
    #         aspiration_location_columns.append(well)
    
    # for well in aspiration_location_columns:
    #     p300.aspirate(10, well)
    #     p300.dispense(10, well)
    #     p300.blow_out(well)
    # for well in aspiration_location_columns:
    #     p20.aspirate(10, well)
    #     p20.dispense(10, well)
    #     p20.blow_out(well)

    # protocol.pause('was this ok?')    


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
    # aspiration_location_wells = []
    # aspiration_wells = (
    #     [pcr_strips.wells_by_name()[well_name] for well_name in 
    #       ['A1', 'A7', 'A11']])
    # for well in aspiration_wells:
    #     aspiration_location_wells.append(well)
            
    # for well in aspiration_location_wells:
    #     p300.aspirate(10, well)
    #     p300.dispense(10, well)
    #     p300.blow_out(well)
    #     p20.aspirate(10, well)
    #     p20.dispense(10, well)
    #     p20.blow_out(well)

    # protocol.pause('was this ok?')  
    
    # columns
    # aspiration_location_columns = []
    # aspiration_columns = (
    #     [pcr_strips.columns_by_name()[column_name] for column_name in
    #       ['1', '7', '11']]
    #     )
    # for column in aspiration_columns:
    #     for well in column:
    #         aspiration_location_columns.append(well)
    
    # for well in aspiration_location_columns:
        # p300.aspirate(10, well)
        # p300.dispense(10, well)
        # p300.blow_out(well)
    #     p20.aspirate(10, well)
    #     p20.dispense(10, well)
    #     p20.blow_out(well)

    # protocol.pause('was this ok?')       
    
# =============================================================================
# test 5mL (screw cap) tube
# =============================================================================
    # p300.aspirate(10, tubes_5mL['A1'])
    # p300.dispense(10, tubes_5mL['A1'])
    # p300.blow_out(tubes_5mL['A1'])
    # p20.aspirate(10, tubes_5mL['A1'])
    # p20.dispense(10, tubes_5mL['A1'])
    # p20.blow_out(tubes_5mL['A1'])
    
    # p300.aspirate(10, tubes_5mL['C5'])
    # p300.dispense(10, tubes_5mL['C5'])
    # p300.blow_out(tubes_5mL['C5'])
    # p20.aspirate(10, tubes_5mL['C5'])
    # p20.dispense(10, tubes_5mL['C5'])
    # p20.blow_out(tubes_5mL['C5'])
    

    # protocol.pause('was this ok?')    
 
    
# =============================================================================
# =============================================================================
    # p300.return_tip()
    p20.return_tip()
    protocol.set_rail_lights(False)