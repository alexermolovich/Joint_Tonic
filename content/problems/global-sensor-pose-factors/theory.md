# Assemble Sensor-Specific Pose Factors

## Intuition

Global sensors constrain different parts of a pose. GPS measures a position, a magnetometer measures field direction, and a barometer supplies height after conversion. Their residuals must retain those distinct meanings.

## Mathematics and conventions

For body-to-world pose $T_{WB}$ and calibrated sensor-to-body extrinsic $T_{BS}$, compute $T_{WS}=T_{WB}T_{BS}$ with rotation $R_{WS}$ and position $p_{WS}$. World axes use east, north, up. GPS $g\in\mathbb R^3$ and converted height $h$ are meters; magnetic vectors $m\in\mathbb R^3$ in sensor coordinates and $f\in\mathbb R^3$ in world coordinates share microtesla units. Define
$$r_g=g-p_{WS},\qquad r_m=\frac m{\|m\|_2}-R_{WS}^\top\frac f{\|f\|_2},\qquad r_h=h-p_{WS,z}.$$
The three GPS entries and height residual have meter units; magnetic direction residuals are dimensionless. For per-coordinate standard deviations $\sigma\in\mathbb R^7_{>0}$ in matching units and sensor availability flags, set unavailable blocks to zero, then
$$\widetilde r_k=r_k/\sigma_k,\qquad E=\tfrac12\sum_{n,k}\widetilde r_{nk}^2.$$
This diagonal-noise, collocated-sensor exercise uses measured-minus-predicted signs. It does not estimate calibration, field bias, or uncertainty from field magnitude.

## Visual computation trace

| Stage | Output | Meaning |
|---|---|---|
| Body pose × sensor extrinsic | sensor world pose | Includes lever arm |
| GPS / field / height models | 3 + 3 + 1 residuals | Separate measurement units |
| Availability then whitening | (N,7) | Missing evidence contributes zero |
| Half squared norm | scalar | Dimensionless objective |

## Worked examples

1. Body and sensor transforms are identity. GPS [1,2,3], magnetic [1,0,0], world field [1,0,0], height 4, all standard deviations 1 and all sensors available give raw [1,2,3,0,0,0,4] and cost 15.
2. The body is identity; the sensor has translation [1,0,0] and a 90-degree z rotation. GPS [1,0,0], sensor magnetic [0,-2,0], world field [5,0,0], and height 0 give zero residuals.

## Why this matters on a robot

Ignoring the GPS lever arm converts rotations into apparent position errors. Treating magnetic vectors as positions is dimensionally wrong. Zero cost with every sensor unavailable is absence of evidence, not a verified pose.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1901.03642). [compose-frame-transforms](/problems/compose-frame-transforms)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
