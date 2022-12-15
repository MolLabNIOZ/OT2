"""
A file with snippets of code
"""

# IMPORT STATEMENTS AND FILES==================================================
# =============================================================================
from opentrons import protocol_api
  ## Import opentrons protocol API v2.
import math
  ## To do some calculations 

# If not simulated, import the .csv from the robot with robot_specific 
# labware off_set values
if simulate: #Simulator
    from mollab_modules import volume_tracking_v1 as vt
      ## Volume_tracking module for robot
    import json
      ## Import json to import custom labware with labware_from_definition,
      ## so that we can use the simulate_protocol with custom labware.  

else: #Robot
    from data.user_storage.mollab_modules import volume_tracking_v1 as vt
      ## Volume_tracking module for simulator
# =============================================================================
