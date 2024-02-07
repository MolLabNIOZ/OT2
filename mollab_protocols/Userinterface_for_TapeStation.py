# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 14:41:22 2024
@author: rdebeer
"""
# Import the modules you need
from data.user_storage.mollab_modules import MO_protocols as MO
from opentrons import protocol_api

# How many samples do you want to check on the TapeStation
number_of_reactions = 96

# Wich kit are you going to use?
tapestation_kit = 'D1000'
    # Options are:
    # 'D1000', 'D5000', 'gDNA', 'RNA'

# What is the starting tip of the p20?    
starting_tip = 'A1'

# What are the sample indexen you want to skip?
skipped_wells = []

# Do you simulate the protocol on the PC?
simulate = True

metadata = {'protocolName': 'TapeStation_run', 'apiLevel': '2.13'}

def run(protocol: protocol_api.ProtocolContext):
    """
    Adding reagents and sample to a TapeStation-plate.
    """
    
    MO.tapestation(tapestation_kit,
                starting_tip,
                number_of_reactions,
                skipped_wells,
                simulate,
                protocol)
    