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

# Tip starting position -- standard variables
  
# Number of samples -- standard variables

# Volumes -- standard variables

# Labware types -- standard variables
    
# Locations (columns, first sample) -- standard variables

# Other variables

# Simulate -- standard variables

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


# CALCULATED AND SET VARIABLES=================================================
# =============================================================================

# Calculated or set volumes

# Number of racks needed

# Container for volume tracking

# Others

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

# Pipette tips

# Pipettes

# Sources (in order of pipetting)

# Destinations

# =============================================================================


# SETTING LOCATIONS============================================================
# =============================================================================

# Starting tips

# Source wells (in order of labware)

# Destination wells 

# =============================================================================   


# MESSAGE AT THE START=========================================================
# =============================================================================
    protocol.comment("your message")              
# =============================================================================


## PIPETTING===================================================================
## ============================================================================

## ============================================================================
 