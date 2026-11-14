# Implement a Functional Physics Step Contract

## Intuition

A functional step receives every state variable explicitly and returns a new state. For a small damped particle model, update velocity from force first, then position using that new velocity. The order is the distinction between semi-implicit and explicit Euler.

## Mathematics and physical contract

For $B$ independent systems and $D$ Cartesian axes, $q,v,f\in\mathbb R^{B\times D}$ denote position (m), velocity (m/s) and force (N) in a fixed common frame. Per-axis mass $m_d$ is in kg and damping $c_d$ in kg/s. For step size $h$ seconds,
$$a_{bd}=\frac{f_{bd}-c_dv_{bd}}{m_d},\qquad v'_{bd}=v_{bd}+ha_{bd},\qquad q'_{bd}=q_{bd}+hv'_{bd}.$$
Mass and damping broadcast across the environment axis only. Gravity is included only if the caller supplied it in force. There are no contacts, rotations or constraints. This original toy model illustrates explicit state flow; it is not a Brax engine implementation or a stability guarantee.

## Worked pipeline and shape trace

```text
q=0m, v=1m/s, f=3N, mass2kg, damping1kg/s, h=.1s
net force3-1*1=2N -> acceleration1m/s^2
v_next=1.1m/s -> q_next=0.11m
(B,D) state + (D,) parameters -> fresh (B,D) state
```

The text trace is the visual and accessible alternative; no animation is required.

## Why this matters on a robot

Hidden mutation makes replay and batched simulation harder to reason about. Even an exactly implemented update can be unstable for overly large time steps or stiff damping, and this toy model omits real robot constraints.

## Prerequisites and source

The problem statement supplies the exact array, unit and boundary conventions. [Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for preserving episode boundaries.

Original bounded component associated with [2021-brax](https://arxiv.org/abs/2106.13281). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
