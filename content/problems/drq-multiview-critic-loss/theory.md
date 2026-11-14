# Compute a Multi-View Critic Regression Loss

## Intuition

Each observed state should contribute equally even when some states have fewer usable augmented views. First reduce within a state, then across states, instead of flattening all available images.

## Mathematical mechanism

For predictions Q of shape B by M, fixed target y of shape B and Boolean validity W, let $n_b=\sum_m W_{bm}$ and $N=\#\{b:n_b>0\}$. Then $$\ell_b=\frac1{n_b}\sum_m W_{bm}(Q_{bm}-y_b)^2,\qquad L=\frac1N\sum_{b:n_b>0}\ell_b.$$ The valid prediction gradient is $2(Q_{bm}-y_b)/(Nn_b)$; invalid entries have zero gradient. Missing-state losses are NaN and an entirely absent batch has total loss zero. Equal counts recover ordinary DrQ view averaging; unequal masks are a declared extension.

## Visual computation trace

| State | Residuals retained | State loss | Gradient entries |
|---|---|---|---|
| 0 | 1, 3 | 5 | 0.5, 1.5 |
| 1 | 2 | 4 | 2, 0 for missing |
| Batch | equal state weights | 4.5 | no target gradient |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Predictions [[1, 3], [4, 99]], targets [0, 2] and mask [[True, True], [True, False]] yield per-state losses [5, 4], total loss 4.5 and gradient [[0.5, 1.5], [2, 0]].

## Why this matters on a robot

Incorrect replay support or inconsistent visual views can teach a robot critic to trust actions that its training data cannot justify. These diagnostics do not establish physical safety.

## Physical contract and limits

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

Source: [primary paper](https://arxiv.org/abs/2004.13649). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
