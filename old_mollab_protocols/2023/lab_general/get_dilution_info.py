import pandas as pd


## Import excel sheet
volume_data = pd.read_excel(
    "C:/Users/mbrouwer/OneDrive - NIOZ/Documenten/GitHub/OT2/mollab_protocols/lab_general/Workflow for an Illumina lane planning example v2.xlsx",
    sheet_name='pooling with dilutions')

# Make list of volumes (rounded to 2 decimals)
EB = round(volume_data['EB'],2).to_list()

# remove NaNs
EB_noNaNs = [x for x in EB if pd.isnull(x) == False and x != 'nan']

print(EB_noNaNs)

print("\nIs it correct that you have ",len(EB_noNaNs), " samples?")

print("\nCopy_Paste the list with volumes to your OT2 protocol")