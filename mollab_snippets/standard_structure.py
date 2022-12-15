"""
A file with the standard structure of a robot protocol.
"""

# Docstring with file info
"""
Version: V_Aug22

filename.py is a protocol written to short discription

You have to provide:
    list of variables that the user has to provide
    
Extra information about features that are only for certain parts of the 
protocol (e.g. what is different when doing a qPCR )
    
The reagent tube should always be put in A1

Updates: 
(INITIALS) date:
    -
    -
"""


# VARIABLES TO SET#!!!=========================================================
# =============================================================================

# =============================================================================


# IMPORT STATEMENTS============================================================
# =============================================================================
#### Import opentrons protocol API v2
from opentrons import protocol_api
                                      
if simulate: #Simulator
    from mollab_modules import volume_tracking_v1 as vt
    import json 
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.     
else: #Robot
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
                                          
# Import other modules
import math
  ## math to do some calculations (rounding up)  
# =============================================================================


# CALCULATED VARIABLES=========================================================
# =============================================================================

# =============================================================================


# METADATA=====================================================================
# =============================================================================
metadata = {
    'protocolName': 'filename.py',
    'author': 'MB <maartje.brouwer@nioz.nl>, SV <sanne.vreugdenhil@nioz.nl>',
    'description': ('short discription'),
    'apiLevel': '2.12'}

def run(protocol: protocol_api.ProtocolContext):
    """
    another short discription  
    """
# =============================================================================

# LOADING LABWARE AND PIPETTES=================================================
# =============================================================================

# =============================================================================


# SETTING LOCATIONS============================================================
# =============================================================================

# =============================================================================   


# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.comment("your message")              
# =============================================================================


## PIPETTING===================================================================
## ============================================================================

## ============================================================================
 