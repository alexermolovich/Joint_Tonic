# Evaluate Trajectory Error After Alignment

## Intuition

Two trajectories can describe the same camera path in different coordinate frames or monocular scales. Remove only the allowed global transformation before measuring per-position discrepancies.

## Mathematics and conventions

Let centered estimated positions $X_i$ and reference positions $Y_i$ each have three coordinates. For N paired positions, define

$$C=\frac1N\sum_iY_iX_i^\top=U\operatorname{diag}(\sigma)V^\top,\qquad D=\operatorname{diag}(1,1,\operatorname{sign}\det(UV^\top)).$$

The proper rotation is $R=UDV^\top$. With estimated variance $v_X=N^{-1}\sum_i\|X_i\|^2$, optional similarity scale and translation are

$$s=\frac{\operatorname{tr}(\operatorname{diag}(\sigma)D)}{v_X},\qquad t=\bar y-sR\bar x.$$

Rigid alignment fixes s=1. Reference units are meters; fitted scale converts estimated units to meters. Aligned error and aggregate RMSE are

$$e_i=\|sR x_i+t-y_i\|_2,\qquad E_{RMSE}=\sqrt{\frac1N\sum_i e_i^2}.$$

The determinant correction forbids mirror reflections. Degenerate paired support is rejected instead of reporting an arbitrary rotation. Global alignment does not repair time-varying scale or drift.

## Visual computation trace

| Transformation component | Known synthetic example |
| --- | --- |
| Rotation | quarter turn about z |
| Scale | 2 estimated units to reference meters |
| Translation | (1,2,3) meters |
| Similarity-aligned RMSE | 0 |
| Rigid-only RMSE | positive: scale mismatch remains |

## Worked examples

1. Estimated tetrahedron points `[[0,0,0],[1,0,0],[0,1,0],[0,0,1]]` as float64, reference `2*Rz(90deg)*point+[1,2,3]`, fit_scale=True: recovered scale 2, rotation Rz(90deg), translation `[1,2,3]`, RMSE zero up to floating error.
2. Use the same reference but fit_scale=False: scale remains exactly 1. The best rigid alignment still has nonzero error because translation and rotation cannot absorb the factor-of-two scale difference.

## Why this matters on a robot

Reporting only aligned RMSE can hide a global scale error if the application requires metric accuracy. Reflections must never be accepted as physical camera-frame rotations, even if they reduce point-cloud error.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2007.11898). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
