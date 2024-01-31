#### Import math module to allow rounding up
import math

tube_type = '5mL_screwcap_tubes'
total_volume = 250000



#### How much volume can a tube hold?
tube_dict = {'tubes_1.5mL'          : 1400,
             '5mL_screwcap_tubes'    : 4800,
             '15mL_tubes'           : 15000,
             '50mL_tubes'           : 50000
             }    

if not tube_type:
    for key, value in tube_dict.items():
        if value >= total_volume:
            tube_type = key
            break
        tube_type = '50mL_tubes'


number_of_tubes = math.ceil((total_volume)/tube_dict[tube_type])

                
