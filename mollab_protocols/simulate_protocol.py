#SV200907 - module for simulating opentrons protocols

# Import statements
from opentrons.simulate import simulate, format_runlog

# Read file
protocol_file = open("mollab_protocols/project_related/210608_eDNA_fish_test_PCR_Wall-E.py")

# Simulate protocol
runlog, _bundle = simulate(protocol_file)

# Print runlog
print(format_runlog(runlog)) 

