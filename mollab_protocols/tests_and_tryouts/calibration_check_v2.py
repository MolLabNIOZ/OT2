# =============================================================================
# Creation date: 211122
# Description: short protocol to check if the calibration is ok.
# =============================================================================


# IMPORT STATEMENTS============================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
# =============================================================================


# VARIABLES TO SET=============================================================
# =============================================================================
pipette20 = True
p20_start_tip = 'A1'
pipette300 = True
p300_start_tip = 'A1'
plate = True
plate_on_rack = True #Plate on coolrack
strips = True
tubes = True #Tubes 1.5mL
tubes5mL = True
test_wells = True #Test 3 wells spread over the labware
test_columns = True #Test 3 columns spread over the labware
# =============================================================================


# RUN==========================================================================
# =============================================================================
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
# =============================================================================
    labwares = []
      ## empty list to add labware to, to loop through
    
    ##### Loading pipettetips
    if pipette300:
        tips_200 = protocol.load_labware(
            'opentrons_96_filtertiprack_200ul',  
            10,                                  
            '200tips')                           
    if pipette20:
        tips_20 = protocol.load_labware(
            'opentrons_96_filtertiprack_20ul',  
            11,                                 
            '20tips')                           
    
    ##### Loading labware
    if plate:
        plate_96 = protocol.load_labware(
            'biorad_96_wellplate_200ul_pcr',
            1,
            '96well_plate')
        labwares.append(plate_96)
    if plate_on_rack:
        plate_coolrack = protocol.load_labware(
            'biorad_qpcr_plate_eppendorf_cool_rack',
            2,
            '96well_plate_on_rack')
        labwares.append(plate_coolrack)
    if strips:                                          
        pcr_strips = protocol.load_labware(
            'pcrstrips_96_wellplate_200ul',     
            3,                                 
            'pcr_strips')                       
        labwares.append(pcr_strips)
    if tubes:
        sample_tubes = protocol.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            4,                                                       
            'sample_tubes')
        labwares.append(sample_tubes)

    if tubes5mL:
        tubes_5mL = protocol.load_labware(
            'eppendorfscrewcap_15_tuberack_5000ul', 
            5,                                      
            'tubes_5mL')                            
        labwares.append(tubes_5mL)
    
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

# START-UP=====================================================================    
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
    for labware in labwares:
    # wells
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
                    
            for well in wells:
                if p300:
                    p300.move_to(well.bottom())
                    protocol.delay(seconds=1)
            for well in wells:
                if p20:
                    p20.move_to(well.bottom()) 
                    protocol.delay(seconds=1)

    
# =============================================================================
# =============================================================================
    p300.return_tip()
    p20.return_tip()
    protocol.set_rail_lights(False)