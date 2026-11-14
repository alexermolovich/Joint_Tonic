# Assemble an IMU-Lidar Pose Constraint

## Intuition

A rotating IMU can move an offset lidar even when the IMU origin stays still. Convert both endpoint poses through the mounting transform before comparing their relative motion to lidar registration.

## Mathematics and conventions

Let $T_{WI_i},T_{WI_j}\in SE(3)$ be IMU-to-world poses and $T_{IL}$ the shared lidar-to-IMU extrinsic. Compute
$$\widehat T_{L_iL_j}=(T_{WI_i}T_{IL})^{-1}(T_{WI_j}T_{IL}),\qquad E=Z^{-1}\widehat T_{L_iL_j},$$
where $Z$ is the measured lidar-j-to-lidar-i transform. For $E=[R_E,p_E;0,1]$, define $r_p=p_E$ in meters and $r_R=\operatorname{Log}(R_E)\in\mathbb R^3$ in radians, with the principal rotation angle bounded by $\pi-10^{-4}$. Then
$$r=[r_p,r_R]\in\mathbb R^6,\qquad \widetilde r=r/\sigma,\qquad E_{\rm cost}=\tfrac12\widetilde r^\top\widetilde r.$$
The positive six standard deviations match translation then rotation units. This is a split residual: its translation is the transform translation, not the left-Jacobian-corrected translation of a full SE(3) logarithm. The full inertial velocity/bias factor is outside this exercise.

## Visual computation trace

```text
IMU-i ---- known mounting ----> lidar-i
  | world poses                   | predicted relative transform
IMU-j ---- known mounting ----> lidar-j
measured inverse × predicted -> split translation / SO3-log -> whitening
```

## Worked examples

1. Identity extrinsic, IMU world poses at x=0 and x=2, measured lidar relative translation x=1, and all standard deviations 1 give translation residual [1,0,0], zero rotation residual, and cost 0.5.
2. The IMU rotates 90 degrees about z at a fixed origin. A lidar mounted one meter along IMU x has relative rotation Rz90 and relative translation [-1,1,0]. Supplying exactly that measurement gives zero cost.

## Why this matters on a robot

Ignoring the mounting offset makes pure rotations look inconsistent with measured lidar motion. Reversing the measurement multiplies transforms in the wrong frame. A small six-coordinate residual does not certify correct bias estimation or scan correspondence.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2007.00258). [compose-frame-transforms](/problems/compose-frame-transforms) · [se3-exponential-logarithm](/problems/se3-exponential-logarithm)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
