# Finite-Difference Gradient Check

## Intuition

Before trusting an optimizer to adjust robot calibration, check whether its reported gradient agrees with small controlled changes to the same objective. The loss definition and reduction must match exactly: a summed residual cost and a mean cost have different gradients.

## Perturb one calibration coordinate

Let A in R^(M×D) be a normalized local measurement design, x in R^D calibration offsets, and b in R^M target residuals. All quantities are dimensionless in this teaching model.

$$L(x)=\tfrac12\|Ax-b\|_2^2,\qquad g_j^{FD}=\frac{L(x+h e_j)-L(x-h e_j)}{2h}.$$

Here $h$ is the positive normalized perturbation and $e_j$ the unit vector. The supplied analytic gradient $g$ is assessed with

$$r_j=\frac{|g_j^{FD}-g_j|}{\max(1,|g_j^{FD}|,|g_j|)}.$$

The denominator avoids exaggerating errors near zero. A tolerance is an engineering comparison parameter, not a convergence proof.

## Visual perturbation trace

| A=2, x=1, b=1, h=0.001 | Residual | Loss |
|---|---|---|
| x+h | 1.002 | 0.502002 |
| x-h | 0.998 | 0.498002 |

The numeric gradient is $(0.502002-0.498002)/0.002=2$. This static trace is the visual and text alternative.

## Why this matters on a robot

A transposed Jacobian or wrong reduction can send calibration in the wrong direction. Very small $h$ subtracts nearly equal floating-point losses; very large $h$ can hide local behavior for nonlinear objectives. This problem fixes a linear measurement model to isolate the gradient-checking contract.

Prerequisite: understand the supplied normalized calibration design and objective.

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
