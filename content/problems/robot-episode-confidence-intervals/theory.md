# Compute Confidence Intervals Across Robot Episodes

## Intuition

A policy's average tracking error can vary across complete trials. Estimate that variation at the episode level instead of treating thousands of correlated control timesteps as thousands of independent tests.

## Between-episode uncertainty

Let X in R^(E×M) contain episode summaries. For metric j in its declared unit,

$$\bar x_j=\frac1E\sum_e X_{ej},\quad s_j^2=\frac1{E-1}\sum_e(X_{ej}-\bar x_j)^2,\quad SE_j=\frac{s_j}{\sqrt E}.$$

A supplied critical multiplier $c$ yields endpoints

$$I_j=[\bar x_j-c SE_j,\bar x_j+c SE_j].$$

Mean, standard error and bounds retain metric units; $c$ is dimensionless. The $E-1$ variance estimates between-episode variation. A matching Student-t multiplier has a conventional confidence interpretation under independent normal summaries; this task intentionally accepts $c$ rather than pretending one fixed constant fits every sample count and distribution.

## Visual worked trace

| Episode | Position-error summary,m |
|---|---|
| 0 | 1 |
| 1 | 3 |
| 2 | 5 |

Mean3m, variance4m², SE=2/sqrt(3)m. With c=2, bounds approximately[0.690599,5.309401]m. This static table is the visual and text alternative.

## Why this matters on a robot

Selecting only successful episodes biases the estimate. Contact failures may also produce heavy tails for which a small-sample normal model is poor. Record the episode selection protocol and interval assumptions; a narrow interval is not a safety guarantee.

Prerequisite: [Aggregate Mean and Worst-Case Policy Returns](/problems/aggregate-policy-returns).

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
