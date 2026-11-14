# Compare Activation-Weighted Quantization Error

## Intuition

The best quantized weights in weight space need not preserve a robot model's outputs. Calibration activations determine which weight errors are amplified and which correlated errors cancel.

## Mathematics and conventions

For candidate $\widehat W^{(k)}\in\mathbb R^{C\times D}$, set $\Delta W^{(k)}=\widehat W^{(k)}-W$ and calibration $X\in\mathbb R^{N\times C}$.
$$e_k^W=\frac{\|\Delta W^{(k)}\|_F^2}{CD},\qquad e_k^Y=\frac{\|X\Delta W^{(k)}\|_F^2}{ND}.$$
Both are dimensionless squared feature/weight quantities in this teaching layer. Select the smallest index minimizing $e_k^Y$. The full output metric includes cross-channel correlations; replacing it with independent per-channel weighted squares is a different contract. AWQ motivates activation-sensitive quantization, while the supplied-candidate comparison here omits its search and clipping recipe.

## Shape and numerical trace

```text
Candidate0 changes the channel activated by10: outputerror10, squared100. Candidate1 changes channel activated by1 by2: outputerror2, squared4. Choose candidate1 despite larger weightMSE.
```

The trace is also the text alternative: each arrow is the ordered operation described above; no animation is required.

## Why this matters on a robot

An edge VLM can suffer task errors when compression targets only small weight MSE. Calibration drift can still invalidate this ranking on new robot scenes.

## Source and prerequisites

Original bounded component inspired by [2023-awq](https://arxiv.org/abs/2306.00978). No pretrained model, paper benchmark result, retraining or hardware latency claim is included. Familiarity with a linear layer and the stated channel convention is assumed.
