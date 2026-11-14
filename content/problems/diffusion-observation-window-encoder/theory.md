# Encode Synchronized Observations for an Action Denoiser

## Intuition

A policy needs an observation context with a fixed temporal layout. This original small encoder makes that contract visible: pool an image, project it alongside proprioception, and preserve time order. A missing sensor is not equivalent to a valid zero measurement.

## Mathematics and physical meaning

Images have shape $(B,T,C,H,W)$ and normalized intensities in $[0,1]$. Proprioception $q$ has shape $(B,T,P)$ in supplied dimensionless normalized channels. Frames are already synchronized, chronological, and from one episode per batch row. Mean-pool only the spatial axes:
$$r_{btc}=\frac1{HW}\sum_{h,w}I_{btchw}.$$
With supplied projections $W_v\in\mathbb R^{C\times D}$, $W_p\in\mathbb R^{P\times D}$ and bias $a\in\mathbb R^D$,
$$z_{bt}=r_{bt}W_v+q_{bt}W_p+a.$$
Keep $z_{bt}$ only when both modality masks are true; otherwise return a zero vector and `used=False`. Tokens have shape $(B,T,D)$; the flat context $(B,TD)$ stores all channels of time zero, then all channels of time one, and so on. These two arrays must have independent storage. This linear fixture replaces a trained visual backbone and is not Diffusion Policy's CNN architecture.

## Visual trace

| One synchronized slot | Contribution |
|---|---:|
| Image mean `.5` × vision weight `3` | 1.5 |
| Proprioception `2` × weight `4` | 8 |
| Bias | 1 |
| Both sensors valid | context 10.5 |
| Proprioception missing | context 0, unused |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** With every dimension equal to 1, image `.5`, proprioception `2`, vision weight `3`, proprioception weight `4`, bias `1` and both masks true, return tokens `[[[10.5]]]`, flat `[[10.5]]` and used `[[True]]`.

**Example 2.** Keep the same data but mark proprioception invalid. Return tokens `[[[0]]]`, flat `[[0]]` and used `[[False]]`. A valid zero pixel would not itself invalidate the slot.

## Why this matters on a robot

A robot policy can react incorrectly when image and joint-state features are out of sync or reordered. This task assumes alignment is already done; zeroing unavailable observations prevents fabricated context but is not a replacement for a fallback controller.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2303.04137). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
