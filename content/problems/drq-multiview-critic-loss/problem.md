# Compute a Multi-View Critic Regression Loss

Each observed state should contribute equally even when some states have fewer usable augmented views. First reduce within a state, then across states, instead of flattening all available images.

## Contract

`predictions` is real `(B, M)`, with `1 <= B <= 128` and `1 <= M <= 64`; `targets` is real `(B,)`; `valid` is Boolean `(B, M)`.

For each state, compute the mean squared prediction-minus-target residual over its valid views. Then average equally over states with at least one valid view. Return a dictionary with:

- `loss`: Python float, the equal-state mean, or zero when no state has a valid view.
- `per_state`: float64 `(B,)`, each state loss, or NaN for a state without views.
- `gradient`: float64 `(B, M)`. Each valid entry is twice its residual divided by both the number of valid views in that state and the number of observed states. Invalid entries are zero.

Targets are fixed; no target gradient is returned. Equal view counts recover ordinary DrQ averaging. The unequal-mask policy is an explicit teaching extension.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Example 1

Predictions [[1, 3], [4, 99]], targets [0, 2] and mask [[True, True], [True, False]] yield per-state losses [5, 4], total loss 4.5 and gradient [[0.5, 1.5], [2, 0]].

## Example 2

If every view is invalid, total loss is zero, every per-state loss is NaN and all gradient entries are zero.
