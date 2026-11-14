# Batch Independent Simulator States

## Intuition

Simulator state is often exposed as a flattened buffer. Environment boundaries are an indexing contract, not something to guess by reshaping. Gather each environment's selected joints explicitly and reject shared indices that would couple supposedly independent robots.

## Mathematics and physical contract

Let $S\in\mathbb R^{A\times2}$ contain $A$ revolute-joint records: column zero is position in radians, column one angular velocity in radians per second. Index map $I\in\{0,\ldots,A-1\}^{B\times J}$ names $J$ joints in each of $B$ environments. The output is
$$Y_{bjc}=S_{I_{bj},c},\qquad Y\in\mathbb R^{B\times J\times2}.$$
All selected indices must be globally unique. The map preserves caller-defined actuator ordering and joint axes. Unselected buffer entries can belong to other actors. This simplified layout excludes prismatic joints and root or rigid-body state formats.

## Worked pipeline and shape trace

```text
flat row:  0       1       2       3
state:   [1,10]  [2,20]  [3,30]  [4,40]
env0 indices[2,0] -> [[3,30],[1,10]]
env1 indices[3,1] -> [[4,40],[2,20]]
(A,2) + (B,J) map -> (B,J,2)
```

The text trace is the visual and accessible alternative; no animation is required.

## Why this matters on a robot

A reshaped buffer can assign a neighboring robot's velocity to the current policy. A correct gather still requires the real simulator adapter to acquire and refresh the right buffer at the right time.

## Prerequisites and source

The problem statement supplies the exact array, unit and boundary conventions. [Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for preserving episode boundaries.

Original bounded component associated with [2021-isaac-gym](https://arxiv.org/abs/2108.10470). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
