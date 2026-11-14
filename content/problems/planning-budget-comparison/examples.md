# Worked examples

1. Budgets `[10,20]`, costs `[[5.,3.],[0.,4.]]`, all observed, solved `[[True,True],[False,True]]` yield counts `[2,2]`, success rate `[0.5,1.]`, median solved cost `[5.,3.5]`, paired counts `[1]`, paired improvement `[2.]`.
2. Budgets `[10,20]`, one row of zero placeholder costs, both masks all False yield counts `[0,0]`, NaN rates/medians, paired count `[0]` and NaN improvement.
