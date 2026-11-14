# Calibrate and Evaluate a Smoothed Int8 Layer

## Goal and contract

Implement `evaluate_smoothing_pipeline(calibration, evaluation, weights, alphas, absolute_tolerance) -> dict`. Use calibration observations to choose equivalent channel scales, then compare several quantized configurations on a separate evaluation batch.

All four arrays must be NumPy float32/float64, finite, absolute value at most1000. Calibration has shape(M,C), evaluation(N,C), weights(C,D), alphas(K,). Require1<=M,N<=128,1<=C,D<=64,1<=K<=8 and alphas in[0,1]. Tolerance is a finite built-in int/float (not bool) in[0,1e6]. Invalid inputs raise ValueError. Preserve all inputs and compute in float64; output arrays are independent. All quantities are dimensionless neural-layer coordinates except squared-error diagnostics, which have squared feature units. No physical frame or timestamp inference occurs.

1. From calibration ONLY, compute a_j=max_i abs(calibration[i,j]). Compute w_j=max_d abs(weights[j,d]). For each supplied alpha, s_j=clip(max(a_j,1e-6)**alpha / max(w_j,1e-6)**(1-alpha),1e-6,1e6). This explicit guard and clamp are teaching policy.
2. For that candidate, X=evaluation/s and W=s[:,None]*weights. Quantize X with one scale per token and W with one scale per output column: scale=max(abs(values))/127, replacing a computed zero scale by1 (including division underflow from a nonzero subnormal range); ties-to-even round, clip to[-127,127], store int8. Multiply using int64 accumulation and dequantize using both scales to get Yhat(N,D). No external model or integer kernel is called.
3. Reference Y=evaluation@weights. Report output_mse[k]=mean((Yhat-Y)**2) over every evaluation token/output, row_max_abs[k,i]=max_d abs(Yhat[i,d]-Y[i,d]), and accepted[k]=all(row_max_abs[k]<=tolerance).
4. selected_index is the smallest supplied index minimizing output_mse (exact floating-point ties only). Selection considers ALL candidates; accepted is diagnostic, not a filter. selected_output is that candidate's Yhat and passed=accepted[selected_index].

Return dict scales:float64(K,C), output_mse:float64(K,), row_max_abs:float64(K,N), accepted:bool(K,), selected_index:Python int, selected_output:float64(N,D), passed:Python bool. Work O(MC+CD+KNCD), storage O(KC+KN+ND+NC+CD); no requirement to retain every candidate output.

A held-out evaluation batch here is used to select a configuration, so it is a validation set, not an untouched final test set. A later independent task evaluation remains necessary. This bounded numerical pipeline reproduces selected SmoothQuant mechanisms, not its full model benchmarks, runtime speedups or exact released calibration/packing recipe.

## Worked examples

calibration=[[2]], evaluation=[[4]], weights=[[2]], alphas=[0.5], tolerance=1e-9 gives scales=[[1]], selected_output approximately[[8]], output_mse approximately[0], row_max_abs approximately[[0]], accepted=[True], selected_index0, passed=True.

calibration=[[0,0]], evaluation=[[0,0]], weights=[[0],[0]], alphas=[0,1], tolerance=0 gives scales=[[1e6,1e6],[1e-6,1e-6]], outputs zero, output_mse=[0,0], row_max_abs=[[0],[0]], accepted=[True,True], selected_index0 and passed=True. The two guards/clamps differ while both exact-zero predictions agree.

## Source

[Meaningful calibration and equivalent smoothing in SmoothQuant](https://arxiv.org/abs/2211.10438). All code, data and evaluation cases are original synthetic teaching material.
