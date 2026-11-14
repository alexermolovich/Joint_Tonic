# Add a Frozen-Backbone Adaptation Module

A small residual adapter can learn a correction while a useful pretrained map stays fixed. Compute the prediction with the original adapter, then update both low-rank matrices from the same loss so the step is mathematically well defined.

## Contract

features X real(B,E),1<=B<=128,1<=E<=64; base_weight W real(E,D),1<=D<=32; down A real(E,R), up C real(R,D),1<=R<=16; targets Y real(B,D); learning_rate real scalar0..1. Each array magnitude<=100. Return dict prediction float64(B,D) BEFORE update, loss Pythonfloat, down/up updated float64 arrays using one simultaneous gradient step on mean squared error over ALL B*D entries. Forward Z=XW+(XA)C. Freeze W and supplied X: update only A,C; use original A,C in both gradients, no sequential update. No nonlinearities, biases or optimizer state.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed. Each batch row is a synchronized caller-supplied policy context; group order is explicit. Original linear residual-adapter training step motivated by adapting generalist policies while freezing pretrained weights; this is not Octo official fine-tuning code or a full parameter-efficient method.


## Example 1

X=[[2]], W=[[3]], A=[[1]], C=[[2]], targets=[[8]], lr=0.1 returns prediction[[10]], loss4, down[[-0.6]], up[[1.2]]. W remains[[3]].

## Example 2

With the same arrays and lr=0, prediction/loss are unchanged and new adapter arrays equal their inputs without sharing storage.
