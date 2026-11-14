# Quantize Actions from Training-Set Quantiles

Rare training outliers should not consume most action-bin resolution. Fit robust bounds from training data, then divide that interval into equal-width bins; changing the evaluation actions must never change those bounds.

## Contract

Training real(N,D),2<=N<=10000,1<=D<=32; actions real(M,D),0<=M<=10000; bins integer scalar2..256. Fit per-channel1st and99th percentiles using NumPy linear quantile interpolation on TRAINING only. Reject any upper<=lower. Uniform bins BETWEEN those bounds, not equal-probability quantile bins. Quantize actions with floor(bins*clip((a-lower)/(upper-lower),0,1)) clipped0..bins-1. Return lower/upper float64(D,), codes int64(M,D), decoded float64(M,D) at bin CENTERS lower+(code+.5)*(upper-lower)/bins. This explicit K-bin teaching codec does not bind IDs to the released OpenVLA tokenizer.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized actions and token features are dimensionless; physical calibration is supplied upstream. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.


## Example 1

Training=[[0],[100]], actions=[[0],[50],[100]], bins2 returns lower[1], upper[99], codes[[0],[1],[1]], decoded[[25.5],[74.5],[74.5]].

## Example 2

The same training with actions=empty((0,1)) still returns fitted bounds and empty(0,1) codes/decoded; evaluation actions never affect fitting.
