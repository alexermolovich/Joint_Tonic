# Quantify Calibration Sensitivity

## Intuition

A one-degree calibration error and a one-kilogram mass error cannot be compared directly. First estimate local score changes, then multiply each derivative by a meaningful uncertainty scale in the same physical unit.

## Matched perturbations

For parameter j and score m, let f_m be the nominal score, f^+_(jm) and f^-_(jm) matched perturbed scores, and delta_j the positive physical perturbation. Central differences give

$$J_{jm}=\frac{f^+_{jm}-f^-_{jm}}{2\delta_j},\qquad H_{jm}=\frac{f^+_{jm}-2f_m+f^-_{jm}}{\delta_j^2}.$$

J has inverse parameter units; H has inverse squared units because scores are dimensionless. For uncertainty scale s_j in parameter units,

$$S_{jm}=|J_{jm}|s_j,\qquad r_j=\max_m S_{jm}.$$

Rank r descending with input-index ties. H is a diagonal local curvature estimate, not the complete Hessian.

## Visual matched-evaluation trace

| Parameter | minus score | nominal | plus score | delta | scale |
|---|---|---|---|---|---|
| yaw, radians | 0.4 | 0.5 | 0.8 | 0.1 | 0.02 |

J=2/rad, H=20/rad², S=0.04. This table is the static visual and text alternative.

## Why this matters on a robot

Use the same scenarios and stochastic seeds for plus/minus runs; otherwise rollout variance masquerades as calibration sensitivity. A zero slope with large curvature can still be fragile. Local finite differences do not expose joint perturbation interactions or contacts beyond the tested neighborhood.

Prerequisite: [Aggregate Mean and Worst-Case Policy Returns](/problems/aggregate-policy-returns).

## Source and scope

This original bounded component is motivated by [2018-dynamics-randomization](https://arxiv.org/abs/1710.06537). It does not reproduce the full paper, trained model or benchmark protocol.
