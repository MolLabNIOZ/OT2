#SV200907 - module for simulating opentrons protocols

#import statements
from opentrons.simulate import simulate, format_runlog

    #read file
protocol_file = open('cross_contamination_test.py')
    #simulate protocol
runlog, _bundle = simulate(protocol_file)
    #print runlog
print(format_runlog(runlog))
