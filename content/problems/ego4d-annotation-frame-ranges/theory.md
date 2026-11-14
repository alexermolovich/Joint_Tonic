# Align Egocentric Video Annotations

## Intuition

Variable-frame-rate video cannot be aligned reliably with a nominal FPS multiplication. Use the actual timestamp table to find which frames fall inside an annotation interval. Empty matches still have a meaningful insertion position.

## Mathematics and physical contract

Strictly increasing frame timestamps $t_0,\ldots,t_{T-1}$ and annotation endpoints $a<z$ are exact integer nanoseconds on one source-video clock. For the half-open interval $[a,z)$, return
$$\ell=|\{i:t_i<a\}|,\qquad h=|\{i:t_i<z\}|.$$
The selected frame-index range is $[\ell,h)$. A frame exactly at $a$ is included, while one exactly at $z$ is excluded. Binary search implements both left insertion positions without converting large timestamps to floating point. These are instantaneous timestamp memberships, not exposure-overlap integrals.

## Worked pipeline and shape trace

```text
frame times: 0 10 25 40 ns
interval[10,40) -> indices[1,3), frames10 and25
interval[11,24) -> indices[2,2), no frame
interval[50,60) -> indices[4,4), after coverage
```

This text trace is both the visual and its accessible alternative; no animation is used.

## Why this matters on a robot

Mistimed human activity annotations can assign the wrong action context to a robot representation learner. A correct single-video index map still needs source identity, camera calibration and any cross-device clock alignment upstream.

## Prerequisites and primary source

[Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for excluding unavailable observations. The Problem tab defines this task's precise indexing, unit and missing-evidence conventions.

Original bounded component associated with [2021-ego4d](https://arxiv.org/abs/2110.07058). The task pins its own explicit finite-data protocol; it does not reproduce the complete paper system or benchmark results.
