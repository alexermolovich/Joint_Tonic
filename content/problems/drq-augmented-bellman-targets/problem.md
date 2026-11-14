# Average Augmented Bellman Targets

Several augmentations of one next observation estimate the same transition value. Average those estimates before bootstrapping, while keeping true termination separate from missing imagery.

## Contract

`rewards` is real `(B,)`; `next_values` is real `(B, K)`, with `1 <= B <= 128` and `1 <= K <= 64`. `terminated` is Boolean `(B,)`; `view_valid` is Boolean `(B, K)`; `gamma` is a scalar in `[0, 1]`.

Average the valid augmented next-state values separately for each transition. Return a dictionary with `targets` and `mean_next` (float64 `(B,)`) and `counts` (int64 `(B,)`). Nonterminal targets equal reward plus gamma times the mean next value. True-terminal targets equal reward. A nonterminal with zero valid views raises ValueError, including when gamma is zero. A terminal may have zero views: report NaN mean, zero count and the finite reward as its target.

All views represent the same physical transition. The supplied values already contain any required SAC entropy adjustment; do not subtract it again or average the reward across views.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Example 1

Reward [1], next values [[2, 4]], both views valid, terminated = [False] and gamma = 0.5 yield mean_next = [3], counts = [2] and targets = [2.5].

## Example 2

A terminal transition with reward 1 and no valid next views yields target 1, mean_next NaN and count 0.
