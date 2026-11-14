# Evaluate Chunk Length Against Compounding Error

Open-loop action errors accumulate until feedback corrects them. A small reset-and-integrate model makes the effect of different feedback intervals visible without pretending to simulate a full robot.

## Contract

`chunk_error_scores(action_error, chunk_lengths)` receives real error(T,D), 1<=T<=4096, 1<=D<=64, abs entries<=100, and integer lengths(K,), 1<=K<=128, each1..T (duplicates permitted, preserve order). Treat error as position-increment error and restart accumulated position error at each nonoverlapping chunk boundary 0,L,2L,... . Within a chunk, position error is the inclusive cumulative sum of action_error. For each length return mean squared position error across all T*D entries, float64(K,). Include the final partial chunk with its actual length.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Error channels are normalized dimensionless position increments; all channels are equally weighted, not mixed raw meters and radians. Rows are equally spaced control steps. The toy reset represents perfect feedback at each chunk boundary. Original diagnostic inspired by ACT compounding-error motivation. It evaluates supplied residuals in a unit-gain integrator; it does not predict ACT rollout performance or claim an optimal chunk length.


## Example 1

action_error=[[1],[1],[1]], chunk_lengths=[1,2,3] returns [1,2,14/3]. The last length2 chunk contains only the final sample.

## Example 2

action_error=[[1],[-1]], chunk_lengths=[2,1] returns [0.5,1]. Cancellation can make a longer chunk score lower in this toy diagnostic.
