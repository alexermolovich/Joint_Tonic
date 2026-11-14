# Calibration quality appears as displaced landmarks

## Intuition

A calibrated camera model predicts where a visible 3D point should land in an image. A measured landmark provides another location. Their difference is a reprojection residual: a small, interpretable diagnostic that connects sensor geometry to calibration and localization.

Assume known correspondences between camera-frame points $p_i=(x_i,y_i,z_i)$ in meters and observed pixels $m_i=(u_i^{obs},v_i^{obs})$. The optical frame uses x right, y down, and z forward. All measurements must refer to the same instant and the same image preprocessing.

## Prediction and error convention

The zero-skew pinhole model uses focal lengths $f_x,f_y$ and principal point $(c_x,c_y)$ in pixels:

$$
\hat u_i=f_x x_i/z_i+c_x,\qquad
\hat v_i=f_y y_i/z_i+c_y.
$$

This lesson defines residual as observation minus prediction:

$$
r_i=m_i-
\begin{bmatrix}\hat u_i\\\hat v_i\end{bmatrix}.
$$

Thus a positive horizontal residual means the measured landmark lies right of the predicted location. Reversing this sign does not change squared error, but it matters when displaying arrows or later deriving parameter updates.

Let V contain rows with $z_i>10^{-8}$. The per-point pixel error is:

$$
\operatorname{RMSE}=\sqrt{\frac{1}{|V|}
\sum_{i\in V}\left(r_{iu}^2+r_{iv}^2\right)}.
$$

This averages squared 2D distances. Averaging over $2|V|$ coordinates instead would produce a different statistic. Invalid depth is excluded rather than replaced by a zero residual, which would misleadingly improve the score.

## Worked camera example

Take $f_x=f_y=100$, principal point $(50,40)$, and point $(0.2,0,2)$. Its prediction is $(60,40)$. If the measured pixel is $(62,37)$, the residual is $(2,-3)$ pixels and its distance is $\sqrt{13}\approx3.606$ pixels.

## Visual interpretation and practical limits

The planned overlay draws predicted and observed landmarks with labeled connecting arrows; a table lists coordinates, residuals, depth validity, and distance. Systematic arrow directions may suggest a principal-point or pose mismatch, while isolated large errors may indicate bad correspondence. These patterns are clues, not unique diagnoses.

On robots, wrong extrinsics, time alignment, lens distortion, rolling shutter, or resize metadata can all increase residuals. A low average can also hide a bad image region. Keep per-point evidence and calibration versions. This exercise measures a declared model's consistency; it neither identifies the cause automatically nor certifies that calibration is correct.
