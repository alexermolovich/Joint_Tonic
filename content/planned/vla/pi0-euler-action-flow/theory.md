# Integrate an Action Flow with Euler Steps

## Intuition

A flow policy learns how an action chunk should change along a generative path. Sampling applies that learned velocity repeatedly. Even if the velocity model is fixed, integration accuracy depends on how the path is discretized.

## One explicit step

Let $X_k\in\mathbb R^{B\times H\times D}$ be normalized action chunks at dimensionless flow time $\tau_k$. B is batch size, H future control ticks and D Euclidean action channels. For a supplied vector field $v$ and increasing grid from0 to1,

$$
\Delta\tau_k=\tau_{k+1}-\tau_k,\qquad
X_{k+1}=X_k+\Delta\tau_k\,v(X_k,\tau_k).
$$

Evaluate the velocity at the current state and left endpoint. This is explicit Euler, not a midpoint or endpoint update. The field has units normalized action per unit flow time. Physical action timestamps are a separate axis inside H.

## Visual: state-dependent updates

| Step | Flow time | State | Velocity v(X)=X | Step size | Next state |
|---|---:|---:|---:|---:|---:|
| 0 | 0 | 1 | 1 | 0.5 | 1.5 |
| 1 | 0.5 | 1.5 | 1.5 | 0.5 | 2.25 |

The trace records [1,1.5,2.25]. It is a static numerical diagram and text alternative. Calling the field again on the updated state is essential.

## Approximation and conditioning

For sufficiently smooth fields, Euler's global discretization error is first order in the largest step size:

$$
\|X_K-X(1)\|=O\!\left(\max_k\Delta\tau_k\right).
$$

This statement needs regularity and stability assumptions; it is not a universal guarantee for arbitrary learned fields. More steps also mean more model calls. The supplied callback can close over fixed observation context, but this exercise neither changes that context nor models inference latency.

The noise-at0 to action-at1 direction matches the corrected pi0v4 training path. Reversing the grid without changing the field convention changes the sampler.

## Why this matters on a robot

Increasing solver steps may reduce numerical error while missing the control deadline. A stale observation can dominate any integration improvement. Return a separate trace for diagnosis, and keep final output storage independent so plotting or logging cannot alter the command buffer.

## Questions

Why does v(X)=X require reevaluation each step? The field depends on the updated state. Should a constant field need a final evaluation at time1? No; all intervals already have their left-endpoint evaluations.


## Sources and prerequisites

[Primary paper](https://arxiv.org/pdf/2410.24164v4), SectionIV and AppendixA-D: forward Euler inference. Prerequisites: [pi0-flow-action-interpolants](/problems/pi0-flow-action-interpolants).
