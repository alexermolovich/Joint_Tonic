# Detect Bad Poses with Reprojection and Render Residuals

Implement `pose_diagnostics(pixel_residuals: np.ndarray, color_residuals: np.ndarray, valid: np.ndarray, pixel_limit: float, color_limit: float) -> dict`.

Compute separate per-view geometric and photometric residual summaries with explicit missing-data flags.
`pixel_residuals` is float64 (V,N,2) measured-minus-predicted image coordinates in pixels; `color_residuals` (V,N,3) is measured-minus-rendered linear RGB in [-1,1]. `valid` is bool (V,N), same validity for both. 1<=V<=32,0<=N<=4096. Limits are built-in int/float non-bool, finite, pixel_limit in [0,1e6], color_limit in [0,1]. Return dict with float64(V,) "pixel_rmse" = sqrt(mean over valid samples of squared 2D norm), "color_rmse" = sqrt(mean over valid samples AND RGB channels of squared entries), bool(V,) "observed", and bool(V,) "flagged". Missing views have both metrics 0, observed=False, flagged=False. Flag an observed view iff either metric strictly exceeds its limit. Validate even masked residual entries. This diagnoses suspicious views; residuals cannot establish that pose, rather than motion/lighting/calibration, caused the failure.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One valid sample with pixel residual `[3,4]`, RGB residual `[1,0,0]` gives pixel_rmse=5 pixels and color_rmse=1/√3. Limits (5,0.6) do not flag it; equality passes.
2. A view with no valid samples reports metrics 0 and observed=False, flagged=False, even at zero limits. Missing evidence is not perfect rendering.

## Source and scope

[Primary source](https://arxiv.org/abs/2003.08934). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
