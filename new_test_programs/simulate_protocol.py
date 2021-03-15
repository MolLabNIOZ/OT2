#SV200907 - module for simulating opentrons protocols

#import statements
from opentrons.simulate import simulate, format_runlog

    #read file
protocol_file = open("new_test_programs/test_volume_tracking.py")
    #simulate protocol
runlog, _bundle = simulate(protocol_file)
    #print runlog
print(format_runlog(runlog))