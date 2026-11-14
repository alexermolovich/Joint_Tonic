# Preintegrate Bias-Corrected IMU Velocity and Position

## Intuition

Each accelerometer sample is measured in a moving body frame. Rotate it into the fixed keyframe frame, then integrate velocity and position with a consistent interval-start convention.

## Mathematics and conventions

With interval-start rotation $\Delta R_k$, specific force $a_k$, bias $b_a$ and duration $h_k$, define $f_k=\Delta R_k(a_k-b_a)$ in the initial body frame.

$$\Delta p_{k+1}=\Delta p_k+\Delta v_kh_k+\tfrac12f_kh_k^2,\qquad\Delta v_{k+1}=\Delta v_k+f_kh_k.$$

Initialize both increments to zero. Force is m/s², velocity m/s and position meters. The position formula uses the old velocity, not the just-updated one. These local preintegrated increments exclude world gravity and initial world velocity by construction.

## Visual computation trace

| Interval | Starting velocity | Position increment | Ending velocity |
| --- | --- | --- | --- |
| 0, force 2 m/s², dt .1 | 0 | .01 m | .2 m/s |
| 1, same force/dt | .2 m/s | .03 m | .4 m/s |
| Total | initial 0 | .04 m | .4 m/s |

## Worked examples

1. One specific-force sample `[[2.,0.,0.]]`, zero bias, identity interval-start rotation, duration `[0.1]` produce final velocity `[0.2,0.,0.]` m/s and position `[0.01,0.,0.]` meters.
2. Two identical samples and durations give final velocity `[0.4,0.,0.]` m/s and position `[0.04,0.,0.]` meters. Both output traces include their initial zero row.

## Why this matters on a robot

Adding gravity here and again in the keyframe factor double-counts it. Using interval-end rotations or updated velocity changes the discretization and produces a systematic position error.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1512.02363). [integrate-imu-rotation](/problems/integrate-imu-rotation)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
