import pandas as pd

volume_data = pd.read_excel("LAB_JUNE_16S.xlsx")

dna = volume_data['UMI1_DNA_VOL'].to_list()

print (dna)
