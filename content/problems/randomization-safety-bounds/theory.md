# Choose Randomization Bounds from Safety Constraints

## Intuition

Randomization must stay inside declared physical limits, and the nominal model should remain represented. An uncertainty margin can consume the entire allowed range; report that failure instead of silently swapping interval endpoints.

## Shrink and intersect

For dimension j, requested endpoints are l^r_j,h^r_j, allowed endpoints l^a_j,h^a_j, margin m_j>=0, and nominal value x_j. Every quantity in that dimension shares a physical unit. Compute

$$l_j=\max(l^r_j,l^a_j+m_j),\qquad h_j=\min(h^r_j,h^a_j-m_j).$$

The independent feasibility flag is

$$v_j=(l_j\le h_j)\land(l_j\le x_j\le h_j).$$

The joint sampling box is the product of feasible intervals only if every dimension is feasible. This box calculation does not account for coupled physical constraints.

## Visual bound trace

| Dimension | Requested | Allowed | Margin | Intersected | Nominal |
|---|---|---|---|---|---|
| mass,kg | [0.5,3] | [1,4] | 0.2 | [1.2,3] | 2: feasible |
| delay,s | [0,0.1] | [0,0.1] | 0.06 | [0.06,0.04] | 0.05: infeasible |

The table is the static visual and text alternative. Report NaN bounds for the delay dimension; do not sample from a reversed interval.

## Why this matters on a robot

Individually valid mass and gain intervals may still form an unstable combination. This operation is a configuration gate before simulation evidence, not a deployment authorization. A nominal point outside the intersection also reveals a mismatch between calibration and the proposed experiment.

Prerequisite: [Version a Simulation Scenario Distribution](/problems/version-simulation-distribution).

## Source and scope

This original bounded component is motivated by [2018-dynamics-randomization](https://arxiv.org/abs/1710.06537). It does not reproduce the full paper, trained model or benchmark protocol.
