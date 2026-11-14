# Sample a Balanced Multi-Dataset Mixture

Large datasets should not automatically dominate every mixed batch. Separate the probability of choosing a dataset from the probability of choosing an example within it.

## Contract

`sample_dataset_mixture(sizes,weights,uniforms)` takes positive integer sizes(G,),1<=G<=128, sizes<=1e6; nonnegative real weights(G,) with positive sum; real uniforms(N,2),0<=N<=10000, entries[0,1). Normalize weights to probabilities and form cumulative sums in input dataset order. For each(u,v), choose the first dataset whose cumulative probability is strictly greater than u (searchsorted side=right); choose local index floor(v*sizes[g]). Zero-weight datasets must never be selected. Return (dataset_ids:int64(N,), local_indices:int64(N,)). Set final CDF entry to1 to avoid cumulative roundoff; no RNG calls.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Counts, weights and fractions are dimensionless; dataset action interfaces remain distinct. Independent draws with replacement; selected local indices are not time coordinates. Original weighted mixture sampler motivated by OXE. Weights are explicit caller policy, not inferred from dataset size or asserted as the paper’s exact proportions.

Build the cumulative distribution over positive-weight datasets only, keeping their original indices; force its last value to exactly 1. This prevents floating-point roundoff from selecting a trailing zero-weight source.


## Example 1

sizes=[2,4], weights=[1,3], uniforms=[[0,0.9],[0.25,0.5]] returns dataset_ids=[0,1], local_indices=[1,2]. The CDF boundary belongs to the next dataset.

## Example 2

sizes=[3,2,5], weights=[0,1,0], uniforms=[[0,0],[0.99,0.99]] returns dataset_ids=[1,1], local_indices=[0,1]. Zero-weight datasets remain unselected.
