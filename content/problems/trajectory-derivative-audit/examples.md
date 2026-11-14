# Worked examples

1. One joint sample with velocity `2`, acceleration `-3`, jerk `4`, limits `[[2.],[3.],[4.]]` yields violations `[[[False,False,False]]]`, max ratios `[[1.],[1.],[1.]]`, passed True.
2. Change velocity to `2.2`: only its velocity flag is True, maximum velocity ratio is `1.1`, and passed is False.
