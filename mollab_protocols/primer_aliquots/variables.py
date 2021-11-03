# =============================================================================
# Trial for illu primer aliquots
# =============================================================================

# number = 50
# while number >= 24:
#     print(number)
#     number -= 24
#     if number <= 24:
#         print('NOT DIVISIBLE BY 24')

primer_combinations_start = 25

primer_tubes_1 = ['A1', 'B1', 'C1', 'D1', 'A2', 'B2', 'C2', 'D2']   
primer_strips_1 = ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2']
primer_tubes_2 = ['A3', 'B3', 'C3', 'D3', 'A4', 'B4', 'C4', 'D4']   
primer_strips_2 = ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7']
primer_tubes_3 = ['A5', 'B5', 'C5', 'D5', 'A6', 'B6', 'C6', 'D6']   
primer_strips_3 = ['A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11']

source = []
destination = []
primer_combinations = primer_combinations_start

if primer_combinations <= 8:
    for well_s, well_d in zip(primer_tubes_1, primer_strips_1):
        source.append(well_s)
        destination.append(well_d)
    source = source[:primer_combinations]
    destination = destination[:primer_combinations]
elif primer_combinations >= 9 and primer_combinations <= 16:
    for well_s, well_d in zip(primer_tubes_1, primer_strips_1):
        source.append(well_s)
        destination.append(well_d)
    for well_s, well_d in zip(primer_tubes_2, primer_strips_2):
        source.append(well_s)
        destination.append(well_d)
    source = source[:primer_combinations]
    destination = destination[:primer_combinations]
elif primer_combinations >= 24:
    for well_s, well_d in zip(primer_tubes_1, primer_strips_1):
        source.append(well_s)
        destination.append(well_d)
    for well_s, well_d in zip(primer_tubes_2, primer_strips_2):
        source.append(well_s)
        destination.append(well_d)
    for well_s, well_d in zip(primer_tubes_3, primer_strips_3):
        source.append(well_s)
        destination.append(well_d)    
    source = source[:primer_combinations]
    destination = destination[:primer_combinations]    
print(primer_combinations)
print(source)
print(destination)

for primer in range(primer_combinations):  
    if primer % 2 == 0 and primer <= 2:
        for well_s, well_d in zip(source, destination):
            print('source: ' + well_s)
            print('destin: ' + well_d) 
        print('LOOP')
    source = source[:primer_combinations]
    destination = destination[:primer_combinations]
    primer_combinations -= 1
    
    
        
print(primer_combinations)
print(source)
print(destination)

#%%

no = 100

if no <= 96:
    print("no <= 96")
if no >= 97 and no >= 192:
    print("no between 24 and 25")
elif no >= 193:
    print("no = high")