# Separate Task Semantics from Scene Variation

## Intuition

The same manipulation goal can appear in different scenes. Group by explicit action, object and goal annotations, while keeping scene identity as a separate factor. This avoids confusing a changed room with a changed task meaning.

## Mathematics and physical contract

Each task $i$ has annotated semantic tuple $k_i=(v_i,o_i,g_i)$: verb, object and goal identities. Its scene identity is $s_i$. For each distinct semantic key $k$, collect
$$T_k=\{i:k_i=k\},\qquad S_k=\{s_i:i\in T_k\},\qquad V_k=\mathbf1[|S_k|\ge2].$$
The ordered tuple is important: exchanging object and goal changes meaning. All values are categorical identities without physical units. Scene identity is not a geometric transform or a substitute for calibration. The task consumes supplied annotations rather than parsing language.

## Worked pipeline and shape trace

```text
pick/cup/tray in kitchen -> semantic group(pick,cup,tray)
pick/cup/tray in lab     -> same group, scenes[kitchen,lab], variationTrue
place/cup/tray in kitchen -> different semantic group, variationFalse
```

This text trace is both the visual and its accessible alternative; no animation is used.

## Why this matters on a robot

Evaluation that mixes changed goals with changed backgrounds cannot isolate the source of a robot policy failure. Matching annotation keys also does not prove that two physical tasks have identical dynamics or difficulty.

## Prerequisites and primary source

[Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for excluding unavailable observations. The Problem tab defines this task's precise indexing, unit and missing-evidence conventions.

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). The task pins its own explicit finite-data protocol; it does not reproduce the complete paper system or benchmark results.
