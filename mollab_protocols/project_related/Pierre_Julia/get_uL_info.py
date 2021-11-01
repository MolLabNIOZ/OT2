import pandas as pd

volume_data = pd.read_excel("\Users\mbrouwer\Documents\GitHub\OT2\mollab_protocols\project_related\Pierre_Julia\LAB_MARCH_16S.xlsx")

dna = volume_data['UMI1_DNA_VOL'].to_list()

print (dna)
