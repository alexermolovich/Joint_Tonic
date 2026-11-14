# Deskew a Lidar Scan with Motion Estimates

## Intuition

A scanning lidar observes different parts of a scene while the sensor moves. First locate each point in the common world, then express it relative to one chosen lidar pose so motion does not bend static geometry.

## Mathematics and conventions

Let $T_{WL_i}$ map the capture-time lidar frame of point i into world, and $T_{WL_r}$ map the reference lidar frame into world. With homogeneous point $p_i$,

$$p_i^{L_r}=T_{WL_r}^{-1}T_{WL_i}p_i^{L_i}.$$

Equivalently, using rotations/translations,

$$p_i^{L_r}=R_r^T(R_ip_i^{L_i}+t_i-t_r).$$

Rotations are dimensionless and all translations/point coordinates are meters. Every point has its own supplied capture pose; a single global cloud transform cannot represent this correction during motion.

## Visual computation trace

| Capture point x | Capture world x | Reference world x | Corrected x |
| --- | --- | --- | --- |
| 2 m | 1 m | 0 m | 3 m |
| 2 m | 1 m | 2 m | 1 m |

## Worked examples

1. One captured point `[[2.,0.,0.]]`, capture pose with identity rotation and world translation `[1.,0.,0.]`, and identity reference pose yield `[[3.,0.,0.]]` in the reference lidar frame.
2. Change the reference pose's world translation to `[2.,0.,0.]`. The same capture and point now yield `[[1.,0.,0.]]` in the reference lidar frame.

## Why this matters on a robot

Using poses at the wrong capture times leaves motion distortion even when the transform algebra is correct. Deskew accuracy depends on time synchronization, motion estimates and lidar extrinsic calibration.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2007.00258). [se3-transform-points](/problems/se3-transform-points) · [compose-frame-transforms](/problems/compose-frame-transforms)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
