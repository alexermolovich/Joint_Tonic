# Solution explanation

Compute activation maxima from calibration only and weight maxima from the original weights. Guard those vectors before exponentiation and clamp each candidate scale. Reuse the fixed unquantized validation output for every comparison. Each candidate then composes equivalent scaling, the explicit symmetric quantizer, int64 matrix accumulation and float64 dequantization.

Record MSE and per-token maximum errors separately. Retain a candidate output only when its MSE is strictly smaller than the best so far, preserving first-index ties without storing every candidate output. Acceptance follows the maximum-error tolerance and does not alter selection. Return the selected quantized output with its acceptance Boolean. Work O(MC+CD+KNCD); storage follows the returned diagnostics and one candidate layer representation.
