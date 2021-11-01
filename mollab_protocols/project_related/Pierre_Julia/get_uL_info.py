import pandas as pd

volume_data = pd.read_excel("mollab_protocols/project_related/Pierre_Julia/TEST_RUN1.xlsx")

dna = volume_data['PCR1_DNA_VOL'].to_list()

print (dna)
