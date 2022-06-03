import pandas as pd

volume_data = pd.read_excel(
    "C:/Users/mbrouwer/OneDrive - NIOZ/Documenten/GitHub/OT2/mollab_protocols/lab_general/Workflow for an Illumina lane planning example v2.xlsx",
    sheet_name='pooling without dilutions')

dna = volume_data['µl to add'].to_list()

print (dna)
