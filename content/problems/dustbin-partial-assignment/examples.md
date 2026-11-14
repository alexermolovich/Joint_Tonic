# Worked examples

1. One source and one target feature, real score 0 and dustbin score 0: every entry of the `2x2` assignment is 0.5. Both unmatched flags are False because the real and dustbin values tie.
2. One source and one target, real score -2 and dustbin score 0, 100 iterations: real-real and dustbin-corner values approach `1/(1+e)`; the two off-diagonal values approach `e/(1+e)`. Both feature unmatched flags are True.
