
# transfer from entire tube rack to specific columns in a pcr plate with strips
    p300.transfer(
        primer_volume,
        primer_tubes.wells(),
        [pcr_strips.columns_by_name()[column_name] for column_name in 
         ['2', '7', '11']], 
        new_tip='always',
        air_gap=1)
    
# transfer from specific columns in tube rack to specific columns in pcr plate
# with strips
    
    p300.transfer(
        primer_volume,
        [primer_tubes.columns_by_name()[column_name] for column_name in 
         ['1', '2']],
        pcr_strips.columns_by_name()['7'],
        new_tip='always',
        air_gap=1)
     #Reverse:
    p300.transfer(
        primer_volume,
        [primer_tubes.columns_by_name()[column_name] for column_name in 
         ['5', '6']],
        pcr_strips.columns_by_name()['7'],
        new_tip='always',
        air_gap=1)
