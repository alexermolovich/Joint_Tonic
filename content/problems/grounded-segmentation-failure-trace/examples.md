# Worked examples

1. One query scores `[0.9,0.2]`, quality0.8, mask `[[True,True],[False,False]]`, thresholds(0.5,0.5): accepted, phrase0, area2, centroid `[1,0.5]` pixels.
2. Two empty masks, best scores `[0.2,0.9]`, qualities `[0.1,0.1]`, thresholds(0.5,0.5) report `["low_grounding","low_mask_quality"]`. Earlier failures take precedence over emptiness.
