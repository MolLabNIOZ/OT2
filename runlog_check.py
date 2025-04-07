'''
Script to create a readable run log from opentrons runlogs
'''
import json
from datetime import datetime

# Define path to raw run log
path_to_raw_runlog = '//lab-mmb.nioz.nl/logs/MolLab_robots/run logs/EVE_Qubit V1.0_2024-11-07T10_40_43.476Z.json'
output_path = path_to_raw_runlog.replace('.json', '.txt')

# Load the raw run log from JSON file
with open(path_to_raw_runlog, encoding='utf-8') as run_log_file:
    raw_run_log = json.load(run_log_file)

# Create a TXT file to append run info
with open(output_path, 'w', encoding='utf-8') as run_log:
    run_log.write('run log for the following protocol:\n')
    run_log.write(f'{path_to_raw_runlog.replace(".json","")}\n\n')

# Append information to the TXT file
with open(output_path, 'a', encoding='utf-8') as run_log:
    

    # Extract run data
    run_data = raw_run_log['data']
    
    # Parse and format run date, start, and end times
    run_date = datetime.strptime(run_data['startedAt'].split('T')[0], '%Y-%m-%d').date()
    run_start = datetime.strptime(run_data['startedAt'].split('T')[1].split('.')[0], '%H:%M:%S')
    run_end = datetime.strptime(run_data['completedAt'].split('T')[1].split('.')[0], '%H:%M:%S')
    run_duration = run_end - run_start
    # Write run date and duration in TXT
    run_log.write(f'Date of the run: {run_date}\n')
    run_log.write(f'Total run time: {run_duration}\n\n')
    
    # Parse run parameters
    run_log.write('Parameters:\n')
    for parameter in run_data.get('runTimeParameters',[]):
        parameter_name = parameter['displayName']
        value = parameter['value']
        suffix = parameter.get('suffix','') #.get to fix that it is not always there
        # Write parameters in TXT
        run_log.write(f'{parameter_name}: {value} {suffix}\n')  
     
    # Parse amd write labware information
    labwares = {}
    run_log.write('\nThe following labware is loaded:\n')
    # Loop through labware
    for labware in run_data.get('labware',[]):
        labwareId = labware['id']
        # Add to dictionary
        labwares[labwareId] = {'labware_name': labware['displayName'], 'deck_slot': labware['location']['slotName']}
        # Write to the TXT
        run_log.write(f'{labware["displayName"]} on deck position {labware["location"]["slotName"]}\n')
    # Loop through pipettes
    for pipette in run_data.get('pipettes',[]):
        pipetteId = pipette['id']
        labwares[pipetteId] = {'pipette_name': pipette['pipetteName'], 'mount': pipette['mount']}

    #Parse all commands
    run_log.write('\nSteps performed in this protocol:\n\n')
    # Dict of all commands it should write down, and their parameters
    possible_commands = {
        'custom': ['legacyCommandText'],
        'setRailLights': ['on'],
        'pickUpTip': ['labwareId', 'pipetteId', 'wellName'],
        'aspirate': ['labwareId', 'pipetteId', 'volume', 'wellName'],
        'dispense': ['labwareId', 'pipetteId', 'volume', 'wellName'],
        'dropTipInPlace': ['pipetteId']       
        }
    
    # Loop through all steps
    for command in raw_run_log['commands']['data']:
        command_type = command['commandType']
        params = command['params']
              
        # Custom = comments
        if command_type == 'custom':
            run_log.write(f'Comment: {params["legacyCommandText"]}\n\n')
        # Raillights
        elif command_type == 'setRailLights':
            state = 'ON' if params['on'] else 'OFF'
            run_log.write(f'Lights are turned {state}\n\n')
        # Aspirate / dispense actions
        elif command_type in {'aspirate', 'dispense'}:
            pipette = labwares[params['pipetteId']]['pipette_name']
            well = params['wellName']
            rack = labwares[params['labwareId']]['labware_name']
            slot = labwares[params['labwareId']]['deck_slot']
            volume = params['volume']
            action = 'aspirated from' if command_type == 'aspirate' else 'dispensed into'
            run_log.write(f'{volume}µL {action} well {well} of {rack} on slot {slot} by {pipette}\n\n')
        # Tip pick up        
        elif command_type == 'pickUpTip':
            pipette = labwares[params['pipetteId']]['pipette_name']
            tip_well = params['wellName']
            tip_box = labwares[params['labwareId']]['labware_name']
            tip_box_slot = labwares[params['labwareId']]['deck_slot']
            run_log.write(f'Tip pickup by {pipette} from {tip_well} of {tip_box} on slot {tip_box_slot}\n\n')
        # Drop tip
        elif command_type == 'dropTipInPlace':
            pipette = labwares[params['pipetteId']]['pipette_name']
            run_log.write(f'Drop tip by {pipette}\n\n')

