import pandas as pd

volume_data = pd.read_excel("LAB_TABLE.xlsx")

dna = volume_data['PCR1_DNA_VOL'].to_list()

print (dna)
