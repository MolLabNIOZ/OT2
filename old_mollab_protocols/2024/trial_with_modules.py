#### Import opentrons protocol API v2
from opentrons import protocol_api
                                      
#### Import protocol module
from mollab_modules import MolLab_pipetting_modules as ML
from mollab_modules import Opentrons_LabWare as LW

metadata = {'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):

   tips_200 = protocol.load_labware(
       'opentrons_96_filtertiprack_200ul', 
       10,                                  
       'opentrons_200tips')
   p300 = protocol.load_instrument(
       'p300_single_gen2',             
       'right',                        
       tip_racks=[tips_200])
   
   source = protocol.load_labware(
       'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
       9,
       'source_tube') 
   
   destination = protocol.load_labware(
       'biorad_96_wellplate_200ul_pcr',    
       6,                                  
       'destination_plate').wells()
   
   ML.trial(p300, 20, source, destination)

   

