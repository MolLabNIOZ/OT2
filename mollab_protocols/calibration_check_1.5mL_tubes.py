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
    tips_20 = protocol.load_labware(
        'opentrons_96_filtertiprack_20ul',  #labware definition
        10,                                 #deck position
        '20tips')                           #custom name
    sample_tubes = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',#labware def
        11,                                                      #deck position
        'sample_tubes')                                          #custom name

    ##### Loading pipettes
    p20 = protocol.load_instrument(
        'p20_single_gen2',                  #instrument definition
        'left',                             #mount position
        tip_racks=[tips_20])                #assigned tiprack
# =============================================================================
    
    p20.starting_tip = tips_20.well('E11')
    p20.pick_up_tip()
    p20.aspirate(10, sample_tubes['D1'])
    p20.dispense(10, sample_tubes['D1'])
    p20.blow_out(sample_tubes['D1'])
    p20.drop_tip()
    
    
    