# Diagnose Camera Dropout and Calibration Drift in BEV

## Intuition

Absent images and geometrically wrong images require different responses. A health report should retain both failure channels and avoid calling an unmeasured camera well calibrated.

## Math and evidence flow

For camera $c$ across $T$ expected instants, let $r_{ct}$ mark reception and $v_{ct}$ mark a usable landmark residual $e_{ct}\in\mathbb R^2$ pixels. Require $v_{ct}\Rightarrow r_{ct}$.
$$d_c=\frac1T\sum_t(1-r_{ct}),\qquad n_c=\sum_t v_{ct},\qquad E_c=\sqrt{\frac{\sum_t v_{ct}\|e_{ct}\|_2^2}{n_c}}.$$
Use a zero placeholder and observed=false when $n_c=0$. Thresholds are dimensionless for dropout and pixels for reprojection RMSE.

| Evidence | Count or value | Interpretation |
|---|---|---|
| 1 missing of 2 expected frames | dropout=0.5 | Transport/acquisition issue |
| Residual (3,4) on received frame | RMSE=5 pixels | Geometry issue worth investigating |
| No valid residuals | observed=false | No calibration conclusion |

## Why this matters on a robot

A dropped camera removes spatial coverage; a miscalibrated camera can actively inject wrong BEV features. Dynamic landmarks, synchronization error or incorrect detections can also increase reprojection residuals. Inspect those causes before recalibrating. This windowed diagnostic is a teaching system component, not a detector learned by BEVFormer.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2203.17270). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
