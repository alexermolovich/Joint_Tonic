# A reproducible layer compression workflow

Start with the atomic channel-range, equivalent-scaling, integer-simulation and error-reporting exercises. Then implement one function that consumes calibration observations, separate validation observations, linear weights, candidate exponents and an explicit absolute tolerance.

```text
calibration + original weights -> per-channel maxima
  + candidate smoothing exponents -> guarded equivalent scales
validation features -> scaled layer -> simulated int8 output
  -> fixed float64 reference comparison -> MSE choice + per-row gate
```

Each arrow is a data dependency; this textual pipeline is also the accessible diagram alternative. For $X\in\mathbb R^{N\times C}$, $W\in\mathbb R^{C\times D}$ and positive diagonal $S$, the starting identity is
$$XW=(XS^{-1})(SW).$$
Rounding makes the quantized output different. This project measures that difference using a precisely declared per-token/per-output symmetric recipe. It is original executable numerical work inspired by [SmoothQuant](https://arxiv.org/abs/2211.10438), with synthetic arrays and no pretrained checkpoint.

Out of scope: full transformer conversion, production packing and integer kernels, model training, task-accuracy reproduction, device latency, closed-loop robot safety and headline paper speedups. Calibration-derived scales and validation-based configuration selection are implemented; an untouched final test set is still needed after selecting a configuration.
