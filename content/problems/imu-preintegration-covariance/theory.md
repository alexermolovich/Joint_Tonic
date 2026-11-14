# Propagate Preintegration Covariance

## Intuition

Independent sensor noise becomes correlated state uncertainty after integration. A velocity error affects later position, while orientation uncertainty rotates the measured force in the wrong direction. Keeping only the diagonal loses that coupling.

## Mathematics and conventions

The nine-dimensional error is $e=[\delta\theta,\delta v,\delta p]$: orientation in radians in the current body tangent frame, velocity in m/s and position in meters in the initial body frame. For one duration $h$ seconds, supplied angular increment $\phi\in\mathbb R^3$ radians, bias-corrected force $f\in\mathbb R^3$ m/s$^2$, and old body-to-initial rotation $R$, let $E=\operatorname{Exp}(\phi)$ and $[x]_\times y=x\times y$. The right Jacobian is
$$J_r(\phi)=I-\frac{1-\cos\theta}{\theta^2}[\phi]_\times+\frac{\theta-\sin\theta}{\theta^3}[\phi]_\times^2,\qquad\theta=\|\phi\|_2.$$
Use continuous series at zero; the coefficients begin $1/2-\theta^2/24$ and $1/6-\theta^2/120$. The error transition and sensor-noise injection are
$$A=\begin{bmatrix}E^\top&0&0\\-R[f]_\times h&I&0\\-\tfrac12R[f]_\times h^2&Ih&I\end{bmatrix},\qquad B=\begin{bmatrix}J_rh&0\\0&Rh\\0&\tfrac12Rh^2\end{bmatrix}.$$
The six noise variances $q$ are discrete per-sample gyro and accelerometer variances, in (rad/s)$^2$ and (m/s$^2$)$^2$. They are not continuous spectral densities. With $P_0=0$,
$$P^+=APA^\top+B\operatorname{diag}(q)B^\top,\qquad R^+=RE.$$
Each covariance entry has the product of its two error-coordinate units. Symmetrize floating roundoff after each step. This fixed-bias, diagonal-sensor-noise recurrence retains cross-covariances in the resulting $9\times9$ matrix.

## Visual computation trace

```text
old orientation error -- force cross-product --> velocity error
old velocity error ------ elapsed seconds ----> position error
gyro and acceleration noise --> B --> new error covariance
(N,6) discrete variances -> covariance trace(N+1,9,9)
```

## Worked examples

1. One sample has zero rotation and force, duration 1 second, gyro variances [1,1,1] and accelerometer variances [4,4,4]. Final orientation-error variances are 1, velocity variances 4, position variances 1, and matching velocity/position cross-covariances 2.
2. Empty sample arrays return covariance shape (1,9,9) containing zeros and final rotation equal to identity.

## Why this matters on a robot

A filter that ignores orientation/force coupling can become overconfident during acceleration. Confusing discrete variance with continuous noise density introduces an extra or missing time-step factor. This covariance excludes bias random walks and is not a full inertial estimator.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1512.02363). [integrate-imu-rotation](/problems/integrate-imu-rotation) · [preintegrate-imu-translation](/problems/preintegrate-imu-translation)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
