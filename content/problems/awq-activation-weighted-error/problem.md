# Compare Activation-Weighted Quantization Error

## Goal and contract

Implement `compare_quantized_candidates(activations, weights, candidates) -> (weight_mse, output_mse, best_index)`. X(N,C), W(C,D), candidates(K,C,D), 1<=N,C,D<=256,1<=K<=32, K*N*C*D<=10^7. Compute float64 mean((candidate-W)^2) over C,D for each candidate, and mean((X@(candidate-W))^2) over N,D. Return both float64(K,) and Python int index of minimum output_mse; exact ties choose smallest candidate index. Use full calibration activations, including channel correlations. No mean-absolute activation proxy, scale search or weight retraining is implemented. Work O(KNCD).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

X=[[10,1]], W=[[0],[0]], candidates=[[[1],[0]],[[0],[2]]] gives weight_mse=[0.5,2], output_mse=[100,4], best_index=1.

X=[[1,1]], W=[[0],[0]], candidates=[[[1],[-1]],[[0],[0]]] gives weight_mse=[1,0], output_mse=[0,0], best_index=0.

## Source and scope

Original bounded component inspired by [2023-awq](https://arxiv.org/abs/2306.00978). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
