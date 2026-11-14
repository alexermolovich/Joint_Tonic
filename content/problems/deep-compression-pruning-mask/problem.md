# Apply a Weight-Pruning Mask

## Goal and contract

Implement `prune_weights(weights, threshold) -> (mask, pruned)`. Weights shape(R,C),1<=R,C<=2048, threshold real[0,1e6]. mask=abs(weights)>=threshold, Boolean; pruned=float64 weights where mask is true and zero otherwise. Equality is retained. At threshold zero even exact zero weights have mask=True. This computes a fixed magnitude mask; no retraining occurs. Work O(RC).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

weights=[[-0.5,0.2],[0,1]], threshold=0.5 returns mask=[[True,False],[False,True]], pruned=[[-0.5,0],[0,1]].

weights=[[0,-1]], threshold=0 returns mask=[[True,True]], pruned=[[0,-1]].

## Source and scope

Original bounded component inspired by [2015-deep-compression](https://arxiv.org/abs/1510.00149). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
