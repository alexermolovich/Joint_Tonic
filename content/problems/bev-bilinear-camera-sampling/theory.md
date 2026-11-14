# Sample Calibrated Multi-Camera Feature Maps

## Intuition

A projected location usually lies between feature-map cells. Bilinear sampling blends nearby cells while preserving a camera-specific validity decision. Projection and calibration are supplied by the caller; this function only gathers aligned visual evidence.

## Mathematics and physical meaning

For a camera feature grid $F\in\mathbb R^{H\times W\times D}$ and feature-pixel coordinates $(u,v)$, let $x=\lfloor u\rfloor$, $y=\lfloor v\rfloor$, $a=u-x$ and $b=v-y$. Clip upper neighbors to the last grid index. The sampled vector is
$$s=(1-b)((1-a)F_{y,x}+aF_{y,x+1})+b((1-a)F_{y+1,x}+aF_{y+1,x+1}).$$
Indices $x+1,y+1$ in this equation mean the clipped upper neighbors. It remains valid at the final row/column and for a one-cell grid. Use the sample only when the caller mask is true and $0\le u\le W-1$, $0\le v\le H-1$; otherwise return zero and `used=False`.

Full inputs are features $(C,H,W,D)$ and coordinates $(C,N,2)$ for $C$ synchronized cameras and $N$ query locations. Output samples are $(C,N,D)$. Coordinates are feature-map pixel centers, not original image pixels or meters; $u$ points right, $v$ down.

## Visual trace

| Neighbor | Value | Weight at `(0.5,0.5)` |
|---|---:|---:|
| Top-left | 0 | .25 |
| Top-right | 2 | .25 |
| Bottom-left | 4 | .25 |
| Bottom-right | 6 | .25 |
| Sum | 3 | 1 |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** One camera has a single-channel map `[[0, 2],[4, 6]]`. A valid point `(u=.5, v=.5)` samples value `3`, with `used=True`.

**Example 2.** For the same map, points `(1, 1)` and `(1.1, 1)` produce samples `6` and `0`. The returned used mask is `[True, False]`; the second point is outside.

## Why this matters on a robot

BEV perception combines evidence from calibrated cameras. Using original image coordinates directly on a downsampled feature map selects the wrong evidence. An out-of-view point must not be clipped into a plausible border observation.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2203.17270). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
