# Compute a Conservative Q Penalty

Conservative Q-learning compares values across the entire finite action set against values of actions that actually appear in the dataset. The gradient raises logged-action support relative to the soft maximum over alternatives.

## Contract

`q_values` is a real array of shape `(B, A)`, where `1 <= B <= 128`, `1 <= A <= 256` and every magnitude is at most `10_000`. `logged_actions` is an integer array `(B, K)`, with `1 <= K <= 128` and indices in `[0, A)`. Duplicate logged indices are allowed. `valid` is a Boolean array `(B,)`; `alpha` is a scalar in `[0, 100]`.

For each row, compute the raw penalty as log-sum-exp over **all A actions**, minus the mean Q value at its K logged indices. Return a dictionary with:

- `loss`: Python float, alpha times the mean raw penalty over valid rows; zero if none are valid.
- `per_state`: float64 `(B,)`, raw penalties, with exact zero in invalid rows.
- `gradient`: float64 `(B, A)`, alpha divided by the valid-row count, times the difference between the Q softmax and empirical logged-action frequencies. Invalid rows have zero gradient.

Use stable log-sum-exp. This is an exact finite-discrete-action CQL regularizer; arbitrary continuous proposals do not satisfy this contract. No TD loss or optimizer step runs.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Example 1

With Q = [[0, 0]], logged indices = [[0]], valid = [True] and alpha = 1, the loss and raw penalty are log(2), and the gradient is [[-0.5, 0.5]].

## Example 2

A single action with Q = [[9]], logged indices = [[0, 0]] and alpha = 2 has zero loss and gradient. Repeated observations do not invent extra actions.
