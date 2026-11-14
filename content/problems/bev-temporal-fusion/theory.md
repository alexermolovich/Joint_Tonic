# Fuse Temporal BEV State

## Intuition

History can stabilize noisy observations, but only if it belongs to the same sequence and location. A gate controls how much old evidence survives; a validity mask and reset take precedence over that gate.

## Math and state flow

At grid cell $(i,j)$, $x_{ij},h_{ij}\in\mathbb R^D$ are current and already aligned historical features. Let $v_{ij}\in\{0,1\}$ mark valid history, $g_{ij}\in[0,1]$ its weight and $r$ the reset flag.
$$a_{ij}=g_{ij}v_{ij}(1-r),\qquad y_{ij}=(1-a_{ij})x_{ij}+a_{ij}h_{ij}.$$

| History state | Effective gate | Output |
|---|---|---|
| Same sequence, valid cell | supplied g | convex blend |
| Missing/out-of-grid history | 0 | current features |
| New sequence | 0 everywhere | current features |

For $x=[2,4]$, $h=[10,0]$, $g=0.25$, $y=0.75[2,4]+0.25[10,0]=[4,3]$. Gates apply to whole feature vectors, not to geometric positions. The bounded convex combination keeps each output channel between its current/history values.

## Why this matters on a robot

State leakage across episodes can create objects from the preceding scene. Ego alignment does not compensate independently moving objects, so even valid history may be stale. This exercise isolates reset/mask/gate behavior; a trained attention block must learn the actual temporal weighting.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2203.17270). [bev-ego-motion-warp](/problems/bev-ego-motion-warp)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
