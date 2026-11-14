# Worked examples

1. Descriptor map `[[[1.,0.],[0.,1.]]]`, keypoint `[[0.5,0.]]`, stride `[1.,1.]`, offset `[0.,0.]`: the sampled vector `[0.5,0.5]` becomes `[1/sqrt(2),1/sqrt(2)]`, valid True.
2. Keypoint `[[-1.,0.]]` with that map and mapping is outside the descriptor grid, so the result is `[0.,0.]`, valid False. A valid zero-valued map also returns zero, but valid True.
