# Quantize Shared Weight Centroids

## Goal and contract

Implement `assign_weight_centroids(weights, active, centroids) -> (indices, reconstructed)`. weights(N,),active Boolean(N,),0<=N<=100000; centroids(K,),1<=K<=256; N*K<=10^7. All weights, including inactive entries, must satisfy numeric validation. For each active entry choose the centroid minimizing absolute distance; ties choose the smallest supplied centroid index, even if centroids are unsorted or duplicated. Inactive indices=-1 and reconstructed=0. Return int64 indices(N,) and float64 reconstructed(N,). No codebook learning or centroid update occurs. Work O(NK).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

weights=[-1,0,3], active=[True,True,False], centroids=[-2,2] gives indices=[0,0,-1], reconstructed=[-2,-2,0]. Zero is tied and chooses index0.

weights=[1,4], active=[True,True], centroids=[3,1,1] gives indices=[1,0], reconstructed=[1,3].

## Source and scope

Original bounded component inspired by [2015-deep-compression](https://arxiv.org/abs/1510.00149). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
