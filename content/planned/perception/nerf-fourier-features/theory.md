# Expose position at several spatial frequencies

## Intuition

A small neural field can struggle to represent rapidly changing color or density directly from a smooth coordinate input. Sinusoids expose multiple spatial scales before the MLP. This changes the input representation; it does not itself learn geometry.

## Define the frequency bands

For normalized scene position $p=(x,y,z)\in\mathbb R^3$, level $\ell$ uses angular frequency $\omega_\ell=2^\ell\pi$. Coordinates are dimensionless, so each phase is dimensionless. With L levels, define

$$
\gamma(p)=
[\sin(\omega_0p),\cos(\omega_0p),\ldots,
\sin(\omega_{L-1}p),\cos(\omega_{L-1}p)]
\in\mathbb R^{6L}.
$$

Sine and cosine act independently on x,y,z. Within a level, all three sine values precede all three cosine values. The raw position is excluded in this contract; some implementations concatenate it as an additional input.

## Visual: one position, two bands

| Level | Phase for x=0.25 | sin(x phase) | cos(x phase) | y,z contributions |
|---|---|---|---|---|
| 0 | π/4 | √2/2 | √2/2 | sine 0, cosine 1 |
| 1 | π/2 | 1 | 0 | sine 0, cosine 1 |

The table traces p=(0.25,0,0). Concatenating its six entries per level produces twelve channels. It is also a text alternative to a frequency plot.

Higher levels oscillate faster: moving x by $2^{1-\ell}$ completes one cycle at level $\ell$. A coordinate-scale error therefore changes the spatial meaning of every feature.

## Numerical and layout choices

Float64 trigonometry can produce tiny nonzero values at theoretical zeros; grade with a tolerance rather than exact equality. Empty inputs retain their feature dimension, and L=0 has no encoded channels. No random seed is needed because all frequencies are fixed.

A sequence ordered coordinate-by-coordinate may contain the same numbers but connect them to different learned weights. Channel order is part of a checkpoint interface, just like image channel order.

## Why this matters on a robot

Neural maps can use positional features to model fine scene structure. If a deployment changes meters-to-scene normalization, the model receives a different pattern even at the same physical point. Record that transform with camera poses and model weights. High-frequency features alone do not fix pose drift or inadequate observations.

## Questions and source

Does this encoding preserve a unique position over all space? No: sinusoids are periodic. Does doubling L double output width? Yes, each new level adds six channels.

Source: [NeRF §5.1 positional encoding](https://arxiv.org/abs/2003.08934). This exercise isolates deterministic input encoding, separate from [ray compositing](/problems/nerf-alpha-compositing).
