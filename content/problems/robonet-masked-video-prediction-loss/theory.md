# Compute a Masked Video-Prediction Loss

## Intuition

A padded video frame is not a black target. Exclude it before subtracting pixels, then report error both overall and by prediction horizon. Horizons with fewer valid examples should not receive accidental extra weight in the overall loss.

## Mathematics and physical contract

Predictions $\widehat I$ and targets $I$ have shape $(B,T,H,W,C)$, and $m_{bt}$ marks a valid frame. Pixels are normalized dimensionless intensities. Define a valid frame error
$$E_{bt}=\frac{1}{HWC}\sum_{h,w,c}(\widehat I_{bthwc}-I_{bthwc})^2.$$
For horizon support $n_t=\sum_bm_{bt}$,
$$L=\frac{\sum_{b,t}m_{bt}E_{bt}}{\sum_tn_t},\qquad L_t=\frac{\sum_bm_{bt}E_{bt}}{n_t}.$$
Unobserved pixels may contain NaN or infinity, so select valid frames before arithmetic; multiplication by zero does not remove NaN. Missing horizon means are NaN. No data produces loss zero plus has_data=False, explicitly distinguishing absence from perfect prediction. This pixel regression does not measure semantic or perceptual image quality.

## Worked pipeline and shape trace

```text
one-pixel errors by batch/horizon: [[0,1],[1,padded]]
counts per horizon[2,1] -> means[.5,1]
overall(0+1+1)/3=2/3, not mean(.5,1)=.75
valid mask(B,T) selects complete(H,W,C) frames
```

This text trace is both the visual and its accessible alternative; no animation is used.

## Why this matters on a robot

Future frames near an episode boundary are often missing. Averaging horizon means equally can overemphasize a poorly supported horizon and change training behavior. Pixel accuracy alone does not establish contact or geometry correctness.

## Prerequisites and primary source

[Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for excluding unavailable observations. The Problem tab defines this task's precise indexing, unit and missing-evidence conventions.

Original bounded component associated with [2019-robonet](https://arxiv.org/abs/1910.11215). The task pins its own explicit finite-data protocol; it does not reproduce the complete paper system or benchmark results.
