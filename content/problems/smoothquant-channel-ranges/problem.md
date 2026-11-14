# Measure Per-Channel Activation and Weight Ranges

## Goal and contract

Implement `calibration_channel_ranges(activations, weights) -> (activation_max, weight_max)`. Activations have shape (N,C), weights (C,D), with 1<=N,C,D<=2048. Return two float64 arrays (C,): maximum absolute calibration activation over N, and maximum absolute weight over D. A completely zero channel has maximum zero. Empty axes are invalid. Work O(NC+CD).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

X=[[1,-4],[3,2]], W=[[2,-1],[0,-5]] gives activation_max=[3,4], weight_max=[2,5].

X=[[0,2]], W=[[0],[3]] gives activation_max=[0,2], weight_max=[0,3].

## Source and scope

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
