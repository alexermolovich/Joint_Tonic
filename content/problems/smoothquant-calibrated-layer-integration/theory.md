# Calibrate and Evaluate a Smoothed Int8 Layer

## Intuition

A useful compression workflow separates observations used to measure ranges from observations used to compare configurations. A smoothing exponent changes which side of a linear layer carries a channel's dynamic range. It preserves the unquantized function, but its rounding error must still be measured.

## Calibration and equivalent transformation

Let calibration $A\in\mathbb R^{M\times C}$, validation features $X\in\mathbb R^{N\times C}$ and weights $W\in\mathbb R^{C\times D}$ be dimensionless. For candidate exponent $\alpha_k\in[0,1]$, define channel maxima $a_j=\max_i|A_{ij}|$, $w_j=\max_d|W_{jd}|$, and guard $\epsilon=10^{-6}$:
$$s_{kj}=\operatorname{clip}\left(\frac{\max(a_j,\epsilon)^{\alpha_k}}{\max(w_j,\epsilon)^{1-\alpha_k}},10^{-6},10^6\right).$$
With $S_k=\operatorname{diag}(s_k)$, use $X_k=XS_k^{-1}$ and $W_k=S_kW$. In real arithmetic $X_kW_k=XW$. The clamp is an explicit numerical teaching choice, while the equivalence holds for every positive scale. Computing $a$ from validation features would leak evaluation distribution into this declared calibration step.

## Quantization and configuration comparison

For each row of $X_k$, use its absolute maximum divided by127; for each output column of $W_k$, use its absolute maximum divided by127. A computed zero scale becomes1, including when dividing a nonzero subnormal maximum by127 underflows to zero. This matches the linked int8 simulation contract; such an extremely small range may reconstruct as zero. The affine groupwise recipe in the separate AWQ exercise has a different explicitly stated positive floor. Round scaled values with ties-to-even and clip to the signed range[-127,127]. Integer accumulation is int64 here; dequantization multiplies the two corresponding float64 scales. Write the resulting layer output as $\widehat Y_k\in\mathbb R^{N\times D}$ and the reference as $Y=XW$.
$$e_k=\frac{1}{ND}\sum_{i,d}(\widehat Y_{kid}-Y_{id})^2,\qquad r_{ki}=\max_d|\widehat Y_{kid}-Y_{id}|.$$
Given absolute tolerance $\tau$ in output-feature units, candidate $k$ passes exactly when every $r_{ki}\le\tau$. Choose the smallest index minimizing $e_k$; do not filter by acceptance. Selection and release diagnostics answer separate questions. The selected validation metric cannot honestly be reported as independent final-test performance.

## Pipeline and worked trace

```text
calibration(M,C) + weights(C,D) -> channel maxima(C,)
  + supplied alphas(K,) -> guarded scales(K,C)
evaluation(N,C) + weights -> K equivalent layer representations
  -> per-token/per-output int8 simulation -> output diagnostics(K,N)
  -> lowest-MSE index + its output(N,D) + explicit absolute gate
```

For the one-channel example, calibration maximum2 and weight maximum2 at exponent0.5 give scale1. The quantized values are both127, their scales are4/127 and2/127, and $127^2(4/127)(2/127)\approx8$, matching the original product. The pipeline above is also a text alternative; no animation is required.

## Why this matters on a robot

A small average layer error can coexist with an unacceptable rare visual token. Keep row diagnostics and validate downstream perception/action behavior on separate robot scenarios. A scalar toy layer gives no evidence about whole-model memory, target-device speed or collision safety. Poorly chosen calibration data can make a seemingly good configuration fail under new lighting or language inputs.

## Prerequisites and source

[Channel ranges](/problems/smoothquant-channel-ranges), [equivalent scaling](/problems/smoothquant-equivalent-rescaling), [int8 layer simulation](/problems/smoothquant-int8-linear-layer), and [row-level error reporting](/problems/smoothquant-layer-error-report) supply the atomic components. [SmoothQuant primary paper](https://arxiv.org/abs/2211.10438) motivates this original integration; no pretrained checkpoint is required.
