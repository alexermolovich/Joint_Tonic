# Quantize Weights and Activations to Int8

## Intuition

An int8 number is an integer plus a scale that gives it meaning. Separate scale selection, rounding and accumulation so an edge deployment can measure the error of each step.

## Mathematics and conventions

For token $i$, $s_i^X=\max_j|X_{ij}|/127$; for output $k$, $s_k^W=\max_j|W_{jk}|/127$. Replace zero scales by one. Define $q_{ij}^X=\operatorname{clip}(\operatorname{rint}(X_{ij}/s_i^X),-127,127)$ and analogously $q^W$.
$$\widehat Y_{ik}=s_i^Xs_k^W\sum_{j=0}^{C-1}q^X_{ij}q^W_{jk}.$$
The integer sum is int64 here to avoid int8 wraparound. Scales and output are float64. This per-token/per-output-channel recipe is explicitly the exercise's bounded simulation, not every kernel or configuration evaluated by SmoothQuant.

## Shape and numerical trace

```text
X(1,2) -> qx(1,2),sx(1,1); W(2,1) -> qw(2,1),sw(1,1); int64 product(1,1)=16129; rescale by 1/127 -> output127.
```

The trace is also the text alternative: each arrow is the ordered operation described above; no animation is required.

## Why this matters on a robot

Wraparound in a low-width accumulator can cause large control-feature errors even when individual quantized weights look plausible. Calibration quality and actual device latency still need separate evaluation.

## Source and prerequisites

Original bounded component inspired by [2022-smoothquant](https://arxiv.org/abs/2211.10438). No pretrained model, paper benchmark result, retraining or hardware latency claim is included. Familiarity with a linear layer and the stated channel convention is assumed.
