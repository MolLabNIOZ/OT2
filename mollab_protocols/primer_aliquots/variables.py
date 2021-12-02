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

no = 300

plate_1 = "plate_1"
plate_2 = "plate_2"
plate_3 = "plate_3"

if no <= 96:
    print(plate_1)
if no >= 97:
    print(plate_1 + " " + plate_2)
if no >= 193:
    print(plate_1 + " " + plate_2 + " " + plate_3)
if no >=289:
    print("TOO HIGH")
    
    
#%%

sample_plate_1 = [1,2,3,4,5,6,7,8]
sample_plate_2 = [9,10,11,12,13,14,15,16]
sample_plate_3 = [17,18,19,20,21,22,23,24]

sample_wells = []

for well in sample_plate_1:
    sample_wells.append(well)
for well in sample_plate_2:
    sample_wells.append(well)
    
print(sample_wells)


#%%
import math

primer_tubes = ['A1', 'B1', 'C1', 'D1', 'A2', 'B2', 'C2', 'D2',
          'A3', 'B3', 'C3', 'D3', 'A4', 'B4', 'C4', 'D4',
          'A5', 'B5', 'C5', 'D5', 'A6', 'B6', 'C6', 'D6']
primer_strips = ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
               'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
               'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11']

total_primer_combinations = 6

number_full_racks = math.floor(primer_combinations/24)

source = []
destination = []

if total_primer_combinations <= 24:
    source = primer_tubes[:total_primer_combinations]
    destination = primer_strips[:total_primer_combinations]
if total_primer_combinations >= 25:
    repeats = math.floor(total_primer_combinations/24)

for primer in range(24):
    if primer % 2 == 0 and primer <= 2:
        for primer_tube, PCR_strip_tube in zip(source, destination):
            print(primer_tube + '    ' + PCR_strip_tube)
        

# for primer in range(total_primer_combinations):
#     if primer % 2 == 0 and primer <= 2:
#         for primer_tube, PCR_strip_tube in zip(source, destination):
#             print(primer_tube + '    ' + PCR_strip_tube)
                

#%%
import math

a = 60
b = a/24
c = math.floor(b)
d = b - math.floor(b)
e = round(d*24)



print(a)
print(b)
print(c)
print(d)
print(e)