# Sample a Progressive-Shrinking Curriculum

Implement sample_progressive_subnets(depths, widths, kernels, phase, count, seed) -> np.ndarray.

Each choice input is a Python list of1–16 strictly decreasing unique built-in non-bool positive ints: depths<=16, widths<=256, odd kernels<=9. phase is a built-in int in[0,3], count in[0,10000], seed in[0,2**32-1]. Phase0 allows only the largest choice for all axes. Phase1 enables every kernel, phase2 additionally every width, phase3 additionally every depth. Choices retain their provided decreasing order.

Construct an independent np.random.Generator(np.random.PCG64(seed)). Draw one array U=rng.random((count,3)), including all three coordinates even when an axis has one legal choice. Columns are depth,width,kernel. Choose index floor(U[:,axis]*len(allowed_axis)) independently. Return fresh int64(count,3), no input mutation or global RNG changes. Empty count yields shape(0,3). Invalid types/order/bounds raise ValueError.

This fixed phase order is an original teaching schedule. It encodes progressive eligibility, not OFA's exact optimizer/distillation/sandwich sampling or performance. Widths are channel counts; all choices are dimensionless architecture integers.

## Worked examples

### Largest network only
`sample_progressive_subnets([4,2],[16,8],[5,3],0,2,0)` returns `[[4,16,5],[4,16,5]]` as int64.

### An empty requested batch
With those same choices, phase3,count0,seed0 returns a new int64 array of shape(0,3). All choice lists must still be valid.

## Source and scope

This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.
