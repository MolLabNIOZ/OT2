# SV201209
# I want to write a protocol to transfer liquid from eppendorfs to PCR strips.
# Aliquoting primers for Illumina sequencing.

#import statements
from opentrons import protocol_api

metadata = {
    'protocolName': 'primer_aliquot',
    'author': 'SV <sanne.vreugdenhil@nioz.nl>',
    'description': 'Protocol for aliquoting Illumina primer dilutions.',
    'apiLevel': '2.6'}
    #apiLevel is the only required argument here, rest of the metadata is
    # also shown in the Opentrons app so it is usefull to put this in

def run(protocol: protocol_api.ProtocolContext):
    """Function to handle the aliquoting of Illumina primers."""

# Loading labware
    strips = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 3, 
                                  '96plate')
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 9, 
                                      '300tips_1')
    f_primers_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 1,
        'Fprimers_1')
    f_primers_2 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 4,
        'Fprimers_2')
    r_primers_1 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 7,
        'Rprimers_1')
    r_primers_2 = protocol.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 10,
        'Rprimers_2')
    
# Load pipette 
    p300 = protocol.load_instrument('p300_single_gen2', 'right', 
        tip_racks=[tiprack_1])
    
# Define functions for transferring.
    def transfer_f():
        "Transfer the forward primers to the strips."
        # Strip 1 F
        p300.transfer(20, [f_primers_1.columns_by_name()[column_name] 
                           for column_name in ['1', '2']], 
                      strips.columns_by_name()['1'], new_tip='always')
        # Strip 2 F
        p300.transfer(20, [f_primers_1.columns_by_name()[column_name] 
                           for column_name in ['3', '4']], 
                      strips.columns_by_name()['4'], new_tip='always')
        # Strip 3 F
        p300.transfer(20, [f_primers_1.columns_by_name()[column_name] 
                           for column_name in ['5', '6']], 
                      strips.columns_by_name()['7'], new_tip='always')
        # Strip 4 F
        p300.transfer(20, [f_primers_2.columns_by_name()[column_name] 
                           for column_name in ['1', '2']], 
                      strips.columns_by_name()['10'], new_tip='always')
    

    def transfer_r():
        "Transfer the reverse primers to the strips."
        # Strip 1 R
        p300.transfer(20, [r_primers_1.columns_by_name()[column_name] 
                            for column_name in ['1', '2']], 
                      strips.columns_by_name()['1'], new_tip='always')
        # Strip 2 R
        p300.transfer(20, [r_primers_1.columns_by_name()[column_name] 
                            for column_name in ['3', '4']], 
                      strips.columns_by_name()['4'], new_tip='always')
        # Strip 3 R
        p300.transfer(20, [r_primers_1.columns_by_name()[column_name] 
                            for column_name in ['5', '6']], 
                      strips.columns_by_name()['7'], new_tip='always')
        # Strip 4 R
        p300.transfer(20, [r_primers_2.columns_by_name()[column_name] 
                            for column_name in ['1', '2']], 
                      strips.columns_by_name()['10'], new_tip='always')
        
    # Numbers of forward primers are used because reverse primers differ per
    # aliquot.
    
    # 1 to 63
    transfer_f()
    transfer_r()
    protocol.pause('Change the tubes and strips.')
    
    # 65 to 127
    transfer_f()
    transfer_r()
    protocol.pause('Change the tubes and strips.')
    
    # 129 to 191
    transfer_f()
    transfer_r()
    protocol.pause('Change the tubes and strips.')
    
    # 193 to 255
    transfer_f()
    transfer_r()
    protocol.pause('Change the tubes and strips.')
    

    
    