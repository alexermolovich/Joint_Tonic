# Apply a Seeded Random-Shift Augmentation

## Intuition

Small translations should not alter which physical transition a stack of camera frames represents. One seeded crop shared across time preserves relative motion while varying image placement.

## Mathematical mechanism

Let X have shape B by T by H by W by C. Edge padding p extends only its spatial axes. Draw one pair $(u_b,v_b)$ uniformly from integer offsets 0 through 2p for each batch row. The result is $$Y_{b,t,h,w,c}=\widetilde X_{b,t,h+u_b,w+v_b,c}.$$ A shared pair across time prevents augmentation-induced apparent motion. PCG64 and draw shape are part of reproducibility, not an inference that arbitrary random-shift implementations generate identical samples.

## Visual computation trace

| Axis | Padding or sampling | Preserved property |
|---|---|---|
| Batch | one offset pair per row | independent views |
| Time | same pair for every frame | relative frame displacement |
| Height/width | edge pad then integer crop | output dimensions |
| Channel | no independent shift | channel alignment |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

An image array of shape (1, 2, 1, 1, 1), with frame values 0.2 and 0.8, remains unchanged after any padding-1 edge crop. Both frames share the same generated offset.

## Why this matters on a robot

Incorrect replay support or inconsistent visual views can teach a robot critic to trust actions that its training data cannot justify. These diagnostics do not establish physical safety.

## Physical contract and limits

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

Source: [primary paper](https://arxiv.org/abs/2004.13649). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
