# Integrate appearance and report what the depth means

## Intuition

Ray weights describe how much visible mass each sample contributes. Color blends those contributions with a background. A depth estimate needs an additional convention: this task reports the expected sample depth **conditioned on a foreground hit**, rather than pretending the background is a surface at a chosen distance.

## Two different sums

Let $w_{ri}\ge0$ be sample weights, $b_r$ the remaining background mass, $\mathbf c_{ri}\in[0,1]^3$ linear RGB, and $z_{ri}$ depth in meters. With background color $\mathbf c_{\mathrm{bg}}$,

$$
\mathbf C_r=\sum_iw_{ri}\mathbf c_{ri}+b_r\mathbf c_{\mathrm{bg}},
\qquad A_r=\sum_iw_{ri}.
$$

Color already includes the full mass. Conditional foreground depth is

$$
D_r=\frac{\sum_iw_{ri}z_{ri}}{A_r}\quad\text{when }A_r>10^{-8}.
$$

For insufficient foreground mass, depth is NaN and validity false. The unnormalized numerator is a depth moment, not this task's conditional expected depth.

## Visual: trace mass and its outputs

| Contributor | Mass | Color | Depth contribution |
|---|---:|---|---:|
| Sample0 | 0.5 | red | 0.5×2=1m |
| Sample1 | 0.25 | green | 0.25×4=1m |
| Background | 0.25 | blue | No foreground depth |
| Combined | 1 | [0.5,0.25,0.25] | 2/0.75=8/3m |

This static table is the text alternative. If both sample weights are zero, RGB is still the background color but no surface depth is available.

## Units and assumptions

Depths are distances along normalized rays, not necessarily optical-axis z. RGB is linear; applying the same weighted average directly to gamma-encoded camera pixels changes the physical interpretation. The caller provides one consistent scene snapshot, ordered samples, and weights from a compositor such as [alpha compositing](/problems/nerf-alpha-compositing).

## Why this matters on a robot

A mostly transparent ray can have a plausible conditional depth backed by very little foreground mass. Downstream mapping should inspect opacity as well as depth validity, and should not convert NaN into a free-space endpoint. This exercise's threshold is an explicit numerical convention, not a robot safety margin.

## Questions and source

Why not divide RGB by A? Background mass already completes the color mixture. Why not assign background depth zero? That would make a different expected-depth convention.

Source: [NeRF volume rendering](https://arxiv.org/abs/2003.08934). Conditional depth and its validity threshold are explicitly defined teaching choices; this is not a trained radiance field.
