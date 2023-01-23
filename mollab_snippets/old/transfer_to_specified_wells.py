# =============================================================================
# How to transfer samples.
# =============================================================================

#from 1 specified well to multiple specified wells:
p20.transfer(1, 
                  sample_tubes['A1'], 
                  [plate_96.wells_by_name()[well_name] for well_name in 
                  ['A2', 'D4', 'B5', 'F5', 'D6', 'B7', 'F7', 'D8', 'B9', 'F9',
                    'A11']], 
                  new_tip='always',
                  blow_out=True,
                  blowout_location='destination well',
                  mix_after=(3, 5),
                  air_gap=1
                  )
              
#from multiple specified wells to other specified wells:
p20.transfer(1, 
                  [sample_tubes.wells_by_name()[well_name] for well_name in 
                  ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']], 
                  [plate_96.wells_by_name()[well_name] for well_name in 
                  ['B2', 'C2', 'D2', 'E2', 'F2', 'G2']], 
                  new_tip='always',
                  blow_out=True,
                  blowout_location='destination well',
                  mix_after=(3, 5),
                  air_gap=1
                  )
