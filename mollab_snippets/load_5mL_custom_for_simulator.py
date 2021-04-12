## The 5mL tubes are custom labware, because the protocol simulator     ##
    ## handles the import of custom labware different than the robot does,  ##
    ## we have 2 options for handling this. Comment out the option that you ##
    ## are not using (in spyder: select + ctrl-1).                          ##

import json 
  ## Import json to import custom labware with labware_from_definition,     ##
  ## so that we can use the simulate_protocol with custom labware.          ##
  

##### !!! OPTION 1: ROBOT                                               ###
    tubes_5mL = protocol.load_labware(
        'eppendorf_15_tuberack_5000ul',     #labware definition
        8,                                  #deck position
        '5mL_tubes')                        #custom name
   
#### !!! OPTION 2: SIMULATOR
    with open("labware/eppendorf_15_tuberack_5000ul/"
              "eppendorf_15_tuberack_5000ul.json") as labware_file: 
        labware_def_5mL = json.load(labware_file)
      ## Import the file that contains all the information about the custom ##
      ## labware. Load the file using json, store it in a variable.         ##
        tubes_5mL = protocol.load_labware_from_definition( 
            labware_def_5mL,                    #labware definition
            3,                                  #deck position
            '5mL_tubes')                        #custom name
        ##Load the labware using load_labware_from_definition() instead of   ##
        ##load_labware(). Then use the variable you just set with the opened ##
        ##json file to define which labware to use.                          ##
        
