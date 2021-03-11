#SV200907 - module for simulating opentrons protocols

#import statements
from opentrons.simulate import simulate, format_runlog

    #read file
protocol_file = open("C:/Users/dnalab/Desktop/OT2/repository/new_test_programs/distribute_test.py")
labware = "C:/Users/dnalab/Desktop/OT2"
    #simulate protocol
runlog, _bundle = simulate(protocol_file, custom_labware_paths = labware)
    #print runlog
print(format_runlog(runlog))


