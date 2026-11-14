# Validate Layer Output Error After Smoothing

## Goal and contract

Implement `layer_error_report(reference, candidate, absolute_tolerance) -> dict`. Both arrays shape(N,D),1<=N,D<=2048; tolerance real in[0,1e6]. Return float64 row_rmse(N,), row_max_abs(N,), bool failed_rows(N,), Python float relative_l2, and Python bool passed. Let error=candidate-reference; row_rmse=sqrt(mean(error^2,axis=1)); failed_rows=row_max_abs>tolerance. relative_l2=norm(error)/max(norm(reference),1e-12), with Frobenius norms over all entries. passed means no failed row. Equality to tolerance passes. This gate has absolute per-output units; relative_l2 is a diagnostic only. Work O(ND).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

reference=[[3,4],[0,0]], candidate=[[3,5],[0,0]], tolerance=1 gives row_rmse=[sqrt(0.5),0], row_max_abs=[1,0], failed_rows=[False,False], relative_l2=0.2, passed=True.

reference=[[0]], candidate=[[2]], tolerance=1 gives row_rmse=[2], row_max_abs=[2], failed_rows=[True], relative_l2=2e12, passed=False.

## Source and scope

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
