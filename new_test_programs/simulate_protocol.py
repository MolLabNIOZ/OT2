#SV200907 - module for simulating opentrons protocols

#import statements
from opentrons.simulate import simulate, format_runlog

    #read file
protocol_file = open("C:/Users/svreugdenhil/Documents/GitHub/OT2/new_test_programs/volume_tracking.py")
    #simulate protocol
runlog, _bundle = simulate(protocol_file)
    #print runlog
print(format_runlog(runlog))


