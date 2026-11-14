# Sample Descriptors at Keypoint Coordinates

## Intuition

A coarse descriptor map and a full-resolution image use different coordinate systems. Convert coordinates first, interpolate channel vectors second, and normalize the resulting vector last.

## Mathematics and conventions

Let image keypoint $p_i=(x_i,y_i)$ have pixel units, stride $s=(s_x,s_y)$ have pixels per grid cell, and offset $o=(o_x,o_y)$ have pixels. Grid position is

$$g_i=(p_i-o)\oslash s.$$

The division is elementwise. For an inside-grid position with fractions a,b, combine descriptor vectors $d_{00},d_{10},d_{01},d_{11}\in\mathbb R^D$:

$$z_i=(1-a)(1-b)d_{00}+a(1-b)d_{10}+(1-a)bd_{01}+ab d_{11},\qquad \hat z_i=\frac{z_i}{\|z_i\|_2}.$$

The normalized expression applies only when $\|z_i\|_2>10^{-12}$; otherwise the output is zero. Descriptor channels and norms are dimensionless. Normalizing each neighbor first would change the result when neighbor magnitudes differ.

## Visual computation trace

| Stage | Midpoint between [1,0] and [0,1] |
| --- | --- |
| Image to grid | (.5,0) |
| Bilinear vector | (.5,.5) |
| Norm | sqrt(.5) |
| Final descriptor | (.70710678,.70710678) |

## Worked examples

1. Descriptor map `[[[1.,0.],[0.,1.]]]`, keypoint `[[0.5,0.]]`, stride `[1.,1.]`, offset `[0.,0.]`: the sampled vector `[0.5,0.5]` becomes `[1/sqrt(2),1/sqrt(2)]`, valid True.
2. Keypoint `[[-1.,0.]]` with that map and mapping is outside the descriptor grid, so the result is `[0.,0.]`, valid False. A valid zero-valued map also returns zero, but valid True.

## Why this matters on a robot

Wrong half-pixel offsets can shift descriptor samples away from detected corners. Normalization cannot repair that geometric error, and a zero descriptor must not be mistaken for a confident feature. This exercise uses bilinear sampling as an explicit teaching variant; the paper reports bicubic interpolation, so this component is not an exact reproduction of its descriptor decoder.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1712.07629). [homographic-keypoint-adaptation](/problems/homographic-keypoint-adaptation)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
