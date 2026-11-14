# Worked examples

1. reference=`[[0],[2]]`, current=`[[1],[3]]`: z=`[1/√1.000001]` and score=1/√1.000001. The reference mean is 1 and current mean is 2.
2. Identical constant clouds `[[4,4]]` have zero shift and score 0. Changing one current channel to 4.001 gives z≈`[1,0]`, score≈1/√2 because the variance floor is 1e-6.
