# Evaluate Offline Policy Support

## Intuition

Offline action support is local to the state where an action was observed. An identical action at another state provides no evidence under this explicitly finite-state diagnostic.

## Mathematical mechanism

For query state z and normalized action u, restrict reference rows to $I(z)=\{i:s_i=z\}$. Then $$d=\min_{i\in I(z)}\|a_i-u\|_2.$$ Return the first original row attaining that minimum. Empty I means unknown distance and unsupported status. Otherwise unsupported means d exceeds the supplied threshold; equality passes. State identifiers are discrete labels, not geometric positions. All D action channels use the same normalized dimensionless scale.

## Visual computation trace

| Query | Matching rows | Distances | Result |
|---|---|---|---|
| state 0, action 0.5 | 0, 1 | 0.5, 0.5 | row 0 by tie rule |
| state 1, action 0.5 | none | unknown | unsupported |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Logged states [0, 0] with actions [[0], [1]] and query state [0] with action [[0.5]] produce nearest index [0] and distance [0.5]. At threshold 0.5, unsupported is false; equal-distance ties choose the first row.

## Why this matters on a robot

Incorrect replay support or inconsistent visual views can teach a robot critic to trust actions that its training data cannot justify. These diagnostics do not establish physical safety.

## Physical contract and limits

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

Source: [primary paper](https://arxiv.org/abs/2006.04779). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
