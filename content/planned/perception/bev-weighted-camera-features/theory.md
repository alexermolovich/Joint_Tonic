# Fuse only camera evidence that exists

## Intuition

A BEV location can be visible in several cameras and invisible in others. Its feature should combine valid observations without letting padding or a failed projection dilute the result. The visibility mask must affect both the weighted sum and its normalization.

## Masked weighted reduction

Let $F\in\mathbb R^{B\times Q\times C\times S\times D}$ contain sampled features for B batches, Q BEV queries, C cameras, S sample locations and D feature channels. Let weights $a$ and Boolean validity $v$ have shape $(B,Q,C,S)$. Define

$$
\widetilde a_{bqcs}=a_{bqcs}v_{bqcs},\qquad
Z_{bq}=\sum_{c,s}\widetilde a_{bqcs},
$$

$$
O_{bq:}=\frac{\sum_{c,s}\widetilde a_{bqcs}F_{bqcs:}}{Z_{bq}}
\quad\text{if }Z_{bq}>0.
$$

All learned features and weights are dimensionless. Zero total mass produces zero output with observed=false. That flag distinguishes absence of evidence from a measured zero feature.

## Visual: numerator and denominator share a mask

| Camera | Feature | Weight | Valid? | Used mass |
|---|---|---:|---|---:|
| 0 | [2,4] | 1 | Yes | 1 |
| 1 | [10,20] | 3 | No | 0 |
| Result | [2,4] | Total1 | Observed | |

If camera1 becomes valid, total mass is4 and the result becomes [8,16]. This static table is the accessible alternative to a camera-ray diagram.

## Scope and upstream geometry

Features are already sampled from synchronized camera maps. This task does not project points, interpolate pixels, learn offsets or compensate ego motion. It deliberately defines one global weighted mean. BEVFormer's complete spatial attention includes additional per-camera, head and sampling structure, so this reduction is a prerequisite mechanism rather than a faithful full block.

## Why this matters on a robot

A missing camera must not look like a confident zero-valued measurement. Dividing by all original weights after masking only the numerator systematically shrinks features during dropout. Conversely, a true validity flag cannot repair stale calibration or timestamps; geometrically wrong evidence can still receive a large weight.

## Questions and source

Does multiplying every valid weight by the same positive constant change output? No; numerator and denominator scale together. Does a valid sample with zero weight establish observation? Under this contract, no positive evidence mass remains.

Source: [BEVFormer spatial cross-attention](https://arxiv.org/abs/2203.17270). Use [camera projection](/problems/project-camera-points) to understand the upstream visibility contract. This task is a simplified, explicitly scoped aggregation primitive.
