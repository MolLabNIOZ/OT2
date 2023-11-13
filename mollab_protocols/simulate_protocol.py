#SV200907 - module for simulating opentrons protocols

# Import statements
from opentrons.simulate import simulate, format_runlog

# Read file
<<<<<<< HEAD
protocol_file = open("molecular_tools/transfering of volume/from epje to PCR-plate.py")
=======
protocol_file = open("C:/Users/mbrouwer/OneDrive - NIOZ/Documenten/GitHub/OT2/mollab_protocols/lab_general/row_fill_plate.py")
>>>>>>> d534a77c9a327838e41bd4addd877047fef5421a


# Simulate protocol
runlog, _bundle = simulate(protocol_file)

# Print runlog
print(format_runlog(runlog)) 

