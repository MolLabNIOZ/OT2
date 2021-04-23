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
    Pick-up tip, followed by aspiration and dispension in a 1.5mL tube. 
    Then drop-tip.
    """
      
# =============================================================================
    ##### Loading labware
    ## For available labware see "labware/list_of_available_labware".       ##
    tips_200 = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul',  #labware definition
        10,                                 #deck position
        '200tips')                           #custom name
    sample_tubes = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        2,                                                       #deck position
        'sample_tubes')                                          #custom name
    pcr_strips = protocol.load_labware(
        'pcrstrips_96_wellplate_200ul',     #labware definition
        1,                                  #deck position
        'pcr_strips')                        #custom name
    
    ##### Loading pipettes
    p300 = protocol.load_instrument(
        'p300_single_gen2',                  #instrument definition
        'right',                             #mount position
        tip_racks=[tips_200])                #assigned tiprack
# =============================================================================
    
    protocol.set_rail_lights(True)
    p300.starting_tip = tips_200.well('A1')
    p300.pick_up_tip()
    p300.aspirate(10, sample_tubes['D1'])
    p300.dispense(10, sample_tubes['D1'])
    p300.blow_out(sample_tubes['D1'])
    
    protocol.pause('was this ok?')
    
    p300.aspirate(10, pcr_strips['A1'])
    p300.dispense(10, pcr_strips['A1'])
    p300.blow_out(pcr_strips['A1'])
    p300.aspirate(10, pcr_strips['A7'])
    p300.dispense(10, pcr_strips['A7'])
    p300.blow_out(pcr_strips['A7'])
    p300.aspirate(10, pcr_strips['A11'])
    p300.dispense(10, pcr_strips['A11'])
    p300.blow_out(pcr_strips['A11'])      
    
    p300.return_tip()
    protocol.set_rail_lights(False)
    
    