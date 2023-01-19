import pandas as pd


## Import excel sheet
volume_data = pd.read_excel(
    "C:/Users/mbrouwer/OneDrive - NIOZ/Documenten/GitHub/OT2/mollab_protocols/project_related/Annalisa/samples.xlsx",
    sheet_name='Sheet1')

# Make list of volumes (rounded to 2 decimals)
dna = round(volume_data['ul DNA'],2).to_list()

# remove NaNs
dna_noNaNs = [x for x in dna if pd.isnull(x) == False and x != 'nan']

print(dna_noNaNs)

print("\nIs it correct that you have ",len(dna_noNaNs), " samples?")

print("\nCopy_Paste the list with volumes to your OT2 protocol")