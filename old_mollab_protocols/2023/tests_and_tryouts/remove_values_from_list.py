# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 13:09:42 2023

@author: mbrouwer
"""

# Make a list with 96 indexes
to_skip = []
for i in range(96):
    to_skip.append(i)

# list with the samples that 
to_do = [3,5,6,7,8,9,13,19,20,22,29,30,35,38,39,41,42,43,44,45,47,48,60,62,65,68,73,75,82,86,88]

# Remove the to_do from the to_skip
for do in to_do:
    to_skip.remove(do)

print(to_skip)
print(len(to_skip))
