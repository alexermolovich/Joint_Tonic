# Worked examples

1. Features `[[1,0],[2,0]]` are identical directions. Predictions both box `[0,0,0.1,0.1]`; targets that box and `[0.8,0.8,0.9,0.9]`; limits (0.99,0.5,0.02) give similar_pairs=`[[0,1]]`, missed_small_indices=`[1]`.
2. With no queries and targets `[0,0,0.1,0.1]` and `[0,0,1,1]`, small_area=0.02 returns no pairs and missing index `[0]`. Large targets are outside this slice.
