# Align Actions and Images in a Video Window

## Intuition

An action belongs between two frames. Pairing it with the wrong next frame trains a predictor on the wrong causal transition. Build current/next/action triples, and keep a window tied to the episode in which it began.

## Mathematics and physical contract

Image sequence $I_t\in[0,1]^{H\times W\times C}$ and command $a_t\in\mathbb R^D$ follow the convention that $a_t$ acts from frame $t$ to $t+1$. For start index $s$ and offset $k$, set $t=s+k$. With observed-frame flag $o_t$ and nondecreasing episode ID $e_t$, validity is
$$m_{s,k}=\mathbf1[t+1<T]\,o_t o_{t+1}\,\mathbf1[e_t=e_{t+1}=e_s].$$
Valid triples are $(I_t,I_{t+1},a_t)$; invalid triples are entirely zero and accompanied by a false mask. Pixel values are dimensionless normalized intensities. Commands retain caller-defined actuator units and frames. Nondecreasing IDs prevent a terminated episode from reappearing later. This task does not interpolate asynchronous camera/action clocks.

## Worked pipeline and shape trace

```text
images[0,.2,.4], actions[1,2], same observed episode, start0/horizon3
current[0,.2,0], next[.2,.4,0], actions[1,2,0], valid[T,T,F]
if episode IDs[0,1,1], both available transitions are invalid for start0
images(T,H,W,C) -> paired outputs(S,K,H,W,C)
```

This text trace is both the visual and its accessible alternative; no animation is used.

## Why this matters on a robot

A camera buffer offset can teach a policy that its command caused an earlier image. Zero padding without a validity mask is equally dangerous because a real dark image is a valid observation.

## Prerequisites and primary source

[Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for excluding unavailable observations. The Problem tab defines this task's precise indexing, unit and missing-evidence conventions.

Original bounded component associated with [2019-robonet](https://arxiv.org/abs/1910.11215). The task pins its own explicit finite-data protocol; it does not reproduce the complete paper system or benchmark results.
