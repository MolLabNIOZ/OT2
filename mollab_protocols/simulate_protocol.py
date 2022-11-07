#SV200907 - module for simulating opentrons protocols

# Import statements
from opentrons.simulate import simulate, format_runlog

# Read file
protocol_file = open("//zeus.nioz.nl/mmb/molecular_ecology/data_from_lab_instruments/Opentrons_robots/EVE/EVE_protocols_ran_for_labusers/2022_EVE/Eva/3different(q)PCR_EVE_no_mm.py")


# Simulate protocol
runlog, _bundle = simulate(protocol_file)

# Print runlog
print(format_runlog(runlog)) 

