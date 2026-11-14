# Measure Per-Channel Activation and Weight Ranges

## Intuition

A rare camera or language token can make one input channel much larger than its neighbors. Measure both sides of the linear layer before deciding where that range can be moved.

## Mathematics and conventions

For calibration tokens $X\in\mathbb R^{N\times C}$ and weights $W\in\mathbb R^{C\times D}$, define $a_j=\max_{0\le i<N}|X_{ij}|$ and $w_j=\max_{0\le k<D}|W_{jk}|$.
$$a,w\in\mathbb R_{\ge0}^{C}.$$
The two reductions use different axes because input channels are columns of $X$ and rows of $W$. These are maxima, not means or percentiles. The later SmoothQuant scale uses channel statistics; this problem only measures them, and does not select a smoothing exponent.

## Shape and numerical trace

```text
X(2,2) -> abs -> reduce token axis -> a(2,)=[3,4]; W(2,2) -> abs -> reduce output axis -> w(2,)=[2,5].
```

The trace is also the text alternative: each arrow is the ordered operation described above; no animation is required.

## Why this matters on a robot

Calibration without rare visual/language contexts can underestimate deployment outliers. Zero maxima are useful evidence and must not be silently replaced here.

## Source and prerequisites

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included. Familiarity with a linear layer and the stated channel convention is assumed.
