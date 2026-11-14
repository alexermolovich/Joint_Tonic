# Worked examples

1. Identity warp, source centers `[[0.,0.],[2.,0.]]`, target centers `[[0.,0.],[1.,0.]]`, all valid, tolerance 1: distances `[[0.,1.],[2.,1.]]`, labels `[[True,True],[False,True]]`.
2. With the first source marked invalid, its entire distance row is NaN and its labels are False. The second row is unchanged.
