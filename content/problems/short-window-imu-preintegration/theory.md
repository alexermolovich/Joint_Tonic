# Preintegrate a Short IMU Window

## Intuition

Preintegration summarizes the effect of many IMU samples relative to the first body frame. Orientation, velocity and position evolve together, but each interval uses the old orientation and velocity in this declared discretization.

## Mathematics and conventions

Let corrected angular rate $\omega_k-b_g$ have rad/s units, corrected specific force $a_k-b_a$ have m/s squared units, and interval $h_k$ have seconds. Relative $R_k$ maps body-k vectors to the initial body frame. Then

$$R_{k+1}=R_k\operatorname{Exp}((\omega_k-b_g)h_k),$$
$$v_{k+1}=v_k+R_k(a_k-b_a)h_k,\qquad p_{k+1}=p_k+v_kh_k+\tfrac12R_k(a_k-b_a)h_k^2.$$

R is dimensionless, v is m/s, and p is m. The exponential uses Rodrigues coefficients with their continuous limits at zero angle. All initial increments are zero except $R_0=I$. Gravity is introduced later when comparing the increments with world-frame state changes, not added inside this body-frame summary.

## Visual computation trace

| Interval | Starting body x direction in initial frame | Force contribution |
| --- | --- | --- |
| 0 | initial x | velocity +x; position +.5x |
| 1 after quarter turn | initial y | velocity +y; old velocity adds +x, acceleration +.5y |
| Final | half turn orientation | v=(1,1,0), p=(1.5,.5,0) |

## Worked examples

1. One zero-angular-rate sample with specific force `[2.,0.,0.]`, zero biases and duration 0.1 s gives final velocity `[0.2,0.,0.]` m/s, position `[0.01,0.,0.]` m and identity rotation.
2. Two one-second intervals with body angular rate `[0.,0.,pi/2]` and body specific force `[1.,0.,0.]` each give final rotation Rz(pi), velocity `[1.,1.,0.]` m/s and position `[1.5,0.5,0.]` m. The second force is rotated by the interval's starting orientation.

## Why this matters on a robot

Rotating force with the end-of-interval orientation changes the integration scheme and introduces motion-dependent errors. A stationary accelerometer generally measures nonzero specific force; omitting gravity here is a preintegration convention, not a claim that stationary readings vanish.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1708.03852). [integrate-imu-rotation](/problems/integrate-imu-rotation) · [preintegrate-imu-translation](/problems/preintegrate-imu-translation)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
