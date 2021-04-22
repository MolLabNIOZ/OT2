# =============================================================================
# How to mix during dispension
# =============================================================================

    mix_vol = sample_vol + 3
      ## Set volume for mixing up and down.                                 ##
    for i in range (3):
        p20.aspirate(mix_vol, well)
        p20.dispense(mix_vol, well)
          ## Mix 3 times up and down with sample volume +3.                 ##
    p20.aspirate(sample_vol, well)
      ## aspirate sample_vol_mix = volume for in mastermix from dill_well   ##
    p20.dispense(sample_vol, well)
      ## dispense sample_vol_mix = volume for in mastermix into mix_well    ##