#SV200907 - module for simulating opentrons protocols

#import statements
from opentrons.simulate import simulate, format_runlog

    #read file
protocol_file = open("C:/Users/dnalab/Desktop/OT2/repository/new_test_programs/implementation_volume_tracking_module.py")
    #simulate protocol
runlog, _bundle = simulate(protocol_file)
    #print runlog
print(format_runlog(runlog))


