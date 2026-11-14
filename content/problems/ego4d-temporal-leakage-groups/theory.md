# Build Leakage-Safe Temporal Splits

## Intuition

Adjacent clips can share nearly identical context even when they do not overlap. A declared guard band connects nearby clips from the same source video. Split whole connected groups so indirect chains cannot leak held-out context into training.

## Mathematics and physical contract

For intervals $A=[a_0,a_1)$ and $B=[b_0,b_1)$ from the same video, define integer-time gap
$$g(A,B)=\max(0,\max(a_0,b_0)-\min(a_1,b_1)).$$
Connect them when $g(A,B)\le\delta$, where guard $\delta\ge0$ is in nanoseconds. This policy intentionally connects touching intervals at $\delta=0$. Transitive connected components determine the split: a component is test when any member was held out. Sweep intervals by start time while retaining the greatest end reached by the current component. Source-video IDs define separate namespaces.

## Worked pipeline and shape trace

```text
same video: a[0,10), b[15,20), c[25,30), guard5ns
a --gap5--> b --gap5--> c
held out c -> connected group[a,b,c] entirely test, group ID a
clips in another video cannot connect through timestamps alone
```

This text trace is both the visual and its accessible alternative; no animation is used.

## Why this matters on a robot

Random clip-level splitting can put neighboring views of the same event on both sides of an evaluation. This policy addresses within-video temporal proximity; it does not prevent the same person, room or object appearing across different videos.

## Prerequisites and primary source

[Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for excluding unavailable observations. The Problem tab defines this task's precise indexing, unit and missing-evidence conventions.

Original bounded component associated with [2021-ego4d](https://arxiv.org/abs/2110.07058). The task pins its own explicit finite-data protocol; it does not reproduce the complete paper system or benchmark results.
