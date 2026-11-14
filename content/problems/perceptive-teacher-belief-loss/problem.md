# Compute Belief Reconstruction and Teacher-Action Losses

A student can imitate a teacher action even when some environmental labels are unavailable. Keep action supervision and belief reconstruction separate, normalize each by its own physical scale, and expose both counts so missing labels cannot silently change the objective.

## Contract

Implement `teacher_belief_loss(student_actions, teacher_actions, reconstruction, privileged_target, action_valid, reconstruction_valid, action_scale, feature_scale, weights)`.

`student_actions` and `teacher_actions` have shape `(B,T,A)`, where `0 <= B <= 64`, `1 <= T <= 128`, and `1 <= A <= 32`. They are joint-position targets in radians, in identical robot joint order, with absolute values at most 10. `reconstruction` and `privileged_target` have shape `(B,T,D)`, where `1 <= D <= 64`; their normalized environmental coordinates have absolute values at most 100.

`action_valid` is a Boolean `(B,T)` mask selecting whole action vectors. `reconstruction_valid` is a Boolean `(B,T,D)` mask selecting individual feature labels. `action_scale` has shape `(A,)`, with values in `[1e-3,10]` radians. `feature_scale` has shape `(D,)`, with values in `[1e-3,100]` in the corresponding normalized feature units. `weights` has shape `(2,)`, with nonnegative values at most 100.

Let `na = A * sum(action_valid)` and `nf = sum(reconstruction_valid)`. The action component is the sum of eligible squared `(student_actions - teacher_actions) / action_scale` residuals divided by `na`. The reconstruction component uses squared `(reconstruction - privileged_target) / feature_scale` residuals divided by `nf`. Each absent component is zero. Total loss is `weights[0] * action_component + weights[1] * reconstruction_component`.

Return a dictionary with `components` (float64 `(2,)`), `counts` (int64 `(2,)`), `loss` (Python float), `action_gradient` (float64 `(B,T,A)`), and `reconstruction_gradient` (float64 `(B,T,D)`). Gradients are analytical derivatives of the total loss with respect to student predictions only; teacher targets, scales, and weights are fixed. Eligible action derivatives are `2 * weights[0] * (student_actions - teacher_actions) / (na * action_scale**2)`, with the analogous reconstruction derivative. Masked entries and absent-component gradients are zero.

This is an original scale-normalized teaching objective. It does not specify the paper's exact network, loss weights, or a hardware controller.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Example 1

Use `B=T=A=D=1`: student action `[[[1.]]]`, teacher action `[[[0.]]]`, reconstruction `[[[2.]]]`, target `[[[0.]]]`, both masks true, `action_scale=[2.]`, `feature_scale=[1.]`, and `weights=[2.,0.5]`.

The action error is `(1/2)^2 = 0.25`; the reconstruction error is `2^2 = 4`. Return `components=[0.25,4.]`, `counts=[1,1]`, `loss=2.5`, `action_gradient=[[[1.]]]`, and `reconstruction_gradient=[[[2.]]]`.

## Example 2

Use the same values with both masks false. Both component losses, both counts, the total loss, and every gradient are zero. Replacing even a masked teacher target with NaN must raise `ValueError`.
