#SV200907 - module for simulating opentrons protocols

# Import statements
from opentrons.simulate import simulate, format_runlog

# Read file
<<<<<<< Updated upstream
protocol_file = open("OT2/mollab_protocols/PCR/qPCRre-do.py")

=======
protocol_file = open("C:/Users/svreugdenhil/Documents/GitHub/OT2/mollab_protocols/tests_and_tryouts/calibration_check.py")
>>>>>>> Stashed changes

# Simulate protocol
runlog, _bundle = simulate(protocol_file)

# Print runlog
print(format_runlog(runlog)) 

