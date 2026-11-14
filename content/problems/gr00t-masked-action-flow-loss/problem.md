# Compute a Masked Action Flow-Matching Loss

A flow model learns how to move a noisy action toward a demonstration. Under the declared noise-to-data path its target is the clean action minus noise; unsupported embodiment channels must contribute neither loss nor gradient.

## Contract

prediction,clean_actions,noise real(B,H,D),common1<=B<=32,1<=H<=64,1<=D<=32; valid bool(B,H,D), true for supported supervised action entries. Prediction is velocity of the explicit noise-to-data path X(t)=(1-t)*noise+t*clean_actions; target=clean_actions-noise. Return dict loss Pythonfloat mean squared error over ALL valid scalar entries across the batch, per_example float64(B,) per-row valid-element mean (0forzero support), gradient float64(B,H,D)=analytic d(global loss)/d(prediction), exact0masked. If no valid entries, loss/per_example/gradient all0. Masked numeric inputs still must be finite/bounded. No DDPM noise target, time sampling or gradient through targets.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized sensor features/actions are dimensionless; embodiment IDs are schema indices, not physical coordinates. Observations are synchronized by the caller; flow time is dimensionless and differs from physical sampling time. Noise-to-data flow matching with an explicit support mask; this captures the GR00T action objective family, not DDPM noise prediction or the complete published training recipe.

## Source convention

[GR00T N1 v1, Section 2.1](https://arxiv.org/html/2503.14734v1#S2.SS1) prints the target noise-minus-action alongside a noise-to-data interpolation. This exercise explicitly chooses the derivative of its stated path, action-minus-noise. It therefore teaches a self-consistent flow objective and does not claim numeric compatibility with that printed target or with released weights.


## Example 1

prediction=[[[0,9]]],clean=[[[3,7]]],noise=[[[1,2]]],valid=[[[True,False]]] gives target[2,5], loss4,per_example[4],gradient[[[-4,0]]].

## Example 2

With all-False mask, even nonzero prediction errors produce loss0,per_example[0],gradient all0; they are unsupported labels, not negative examples.
