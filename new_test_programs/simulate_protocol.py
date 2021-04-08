#SV200907 - module for simulating opentrons protocols

# Import statements
from opentrons.simulate import simulate, format_runlog

# Read file
protocol_file = open("new_test_programs/test_volume_tracking_internal_module_old.py")

# Simulate protocol
runlog, _bundle = simulate(protocol_file)

# Print runlog
print(format_runlog(runlog))