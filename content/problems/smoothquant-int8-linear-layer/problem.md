# Quantize Weights and Activations to Int8

## Goal and contract

Implement `quantize_int8_layer(activations, weights) -> (qx, qw, sx, sw, output)`. X(N,C), W(C,D), 1<=N,C,D<=1024, N*C*D<=10^7. Use symmetric integer range [-127,127]. sx(N,1)=max(abs(X),axis=1)/127; sw(1,D)=max(abs(W),axis=0)/127. Replace a zero scale with exactly 1. Quantize with round-to-nearest ties-to-even then clip; qx/qw have dtype int8. Return scales float64 and output(N,D)=(qx.astype(int64) @ qw.astype(int64))*sx*sw in float64. This is a numerical simulation, not an optimized int8 kernel. Work O(NCD).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

X=[[127,0]], W=[[1],[0]] gives qx=[[127,0]], qw=[[127],[0]], sx=[[1]], sw=[[1/127]], output=[[127]].

X=[[0,0]], W=[[0],[0]] gives zero int8 arrays, sx=[[1]], sw=[[1]], output=[[0]].

## Source and scope

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
