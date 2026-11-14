# Compare Logged and Sampled Action Values

## Intuition

A critic can score sampled actions much higher than logged behavior. Report the two sample means separately so that missing observations cannot masquerade as a reassuring zero gap.

## Mathematical mechanism

Let L and S be logged and sampled values with separate Boolean masks. For row b, $$g_b=\frac{\sum_k M^S_{bk}S_{bk}}{n^S_b}-\frac{\sum_j M^L_{bj}L_{bj}}{n^L_b}.$$ Each count is its own mask sum. Means require positive corresponding counts; the gap requires both. Flag only a known gap strictly greater than threshold tau. Values, gap and tau share reward units. This is a diagnostic; sample means do not replace the CQL log-partition penalty.

## Visual computation trace

| Pool | Values | Count | Mean |
|---|---|---|---|
| Logged | 1, 3 | 2 | 2 |
| Sampled | 5 | 1 | 5 |
| Difference | sampled minus logged | known | 3 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Logged values [[1, 3]] and sampled values [[5]], all valid, have means 2 and 5. The gap is 3, counts are [[2, 1]], and threshold 2 produces flagged = [True].

## Why this matters on a robot

Incorrect replay support or inconsistent visual views can teach a robot critic to trust actions that its training data cannot justify. These diagnostics do not establish physical safety.

## Physical contract and limits

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

Source: [primary paper](https://arxiv.org/abs/2006.04779). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
