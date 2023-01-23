#SV200907 - module for simulating opentrons protocols

# Import statements
from opentrons.simulate import simulate, format_runlog

# Read file
protocol_file = open("C:/Users/svreugdenhil/OneDrive - NIOZ/Documenten/GitHub/OT2/mollab_protocols/lab_general/tapestation_reagents.py")


# Simulate protocol
runlog, _bundle = simulate(protocol_file)

# Print runlog
print(format_runlog(runlog)) 

