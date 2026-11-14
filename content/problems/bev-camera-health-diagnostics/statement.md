# Diagnose Camera Dropout and Calibration Drift in BEV

Implement `camera_health(received: np.ndarray, residuals: np.ndarray, valid: np.ndarray, max_dropout: float, max_rmse: float) -> dict`.

Distinguish missing camera frames from high reprojection residuals in a synchronized window.
`received` is bool (C,T),1<=C<=16,1<=T<=4096; each False is one expected but missing frame. `residuals` float64 (C,T,2) contains one landmark displacement in pixels per frame; `valid` bool (C,T) marks usable landmark residuals and must imply received=True. Limits are built-in int/float non-bool: max_dropout in [0,1], max_rmse in [0,1e6]. Return dict arrays (C,): float64 "dropout_rate", "reprojection_rmse", bool "observed", "dropout_alert", "calibration_alert". Dropout is missing_count/T. RMSE is sqrt(mean squared 2D norm over valid residuals), zero if none; observed means any valid residual. Alerts use strict > thresholds; calibration_alert also requires observed. Validate all residuals even if masked. These are diagnostic flags, not proof of calibration drift or an automatic recalibration command.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. received=`[[True,False]]`, valid=`[[True,False]]`, residuals=`[[[3,4],[0,0]]]`, limits (0.25,4) report dropout 0.5, RMSE 5, both alerts True.
2. An entirely missing two-frame window has dropout 1, RMSE placeholder 0, observed=False, calibration_alert=False. It may trigger dropout_alert, but supplies no calibration evidence.

## Source and scope

[Primary source](https://arxiv.org/abs/2203.17270). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
