# =============================================================================
# Author(s): Maartje Brouwer & Sanne Vreugdenhil
# Creation date: 210510
# Description: protocol for aliquoting 12S illumina primers, 1 eppendorf rack
#   at a time, 6 aliquots in total.
# =============================================================================

##### Import statements
from opentrons import protocol_api
  ## Import opentrons protocol API v2.                                      ##
  
import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
  
# =============================================================================

##### Metadata
metadata = {
    'protocolName': 'Aliquoting 12S Illumina primers, 1 rack at a time, 6x',
    'author': 'SV <sanne.vreugdenhil@nioz.nl> & MB <maartje.brouwer@nioz.nl>',
    'description': ('Protocol for aliquoting 42 illumina primer pairs, '
                    '1 eppendorf rack at a time - 6 aliquots'
                    'Pausing after every rack so that you can put the next '
                    'rack in. \n '
                    'NOTE: Start with '),
    'apiLevel': '2.9'}

##### Define function
def run(protocol: protocol_api.ProtocolContext):
    """
    Aliquoting Illumina primers from 1 tube rack filled with 1.5 mL tubes,
    to 3 PCR strips in a BioRad 96-well plate, calibrated with Westburg
    PCR strips.
    """
      
# =============================================================================