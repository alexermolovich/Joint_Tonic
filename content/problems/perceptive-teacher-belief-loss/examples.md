## Example 1

Use `B=T=A=D=1`: student action `[[[1.]]]`, teacher action `[[[0.]]]`, reconstruction `[[[2.]]]`, target `[[[0.]]]`, both masks true, `action_scale=[2.]`, `feature_scale=[1.]`, and `weights=[2.,0.5]`.

The action error is `(1/2)^2 = 0.25`; the reconstruction error is `2^2 = 4`. Return `components=[0.25,4.]`, `counts=[1,1]`, `loss=2.5`, `action_gradient=[[[1.]]]`, and `reconstruction_gradient=[[[2.]]]`.

## Example 2

Use the same values with both masks false. Both component losses, both counts, the total loss, and every gradient are zero. Replacing even a masked teacher target with NaN must raise `ValueError`.
