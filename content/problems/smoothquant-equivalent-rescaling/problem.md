# Apply an Equivalent Channel Rescaling

## Goal and contract

Implement `rescale_linear_channels(activations, weights, scales) -> (scaled_activations, scaled_weights)`. X has shape (N,C), W (C,D), scales (C,), 1<=N,C,D<=2048. Require 1e-6<=scales[j]<=1e6. Return float64 X/scales and scales[:,None]*W; output magnitudes may exceed the input bound. No quantization or calibration search occurs. Work O(NC+CD).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

X=[[2,8]], W=[[3],[4]], scales=[2,4] returns [[1,2]], [[6],[16]]. Both products equal [[38]].

X=[[0,-3]], W=[[5,1],[2,-1]], scales=[1,0.5] returns [[0,-6]], [[5,1],[1,-0.5]]. Both products equal [[-6,3]].

## Source and scope

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
