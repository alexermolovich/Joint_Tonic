# Compute a Differential-Drive Rollout

## Intuition

Equal wheel speeds move straight; unequal speeds trace a circle. Integrating only the initial heading is inaccurate during turns. The exact arc uses the heading halfway through the interval and a distance correction.

## Mathematics and physical meaning

For left/right wheel rates $\omega_l,\omega_r$ in rad/s, radius $r$ metres and track width $b$ metres,
$$v=\frac r2(\omega_l+\omega_r),\qquad \omega=\frac r b(\omega_r-\omega_l).$$
Let $h=\omega\Delta t/2$ and define $\operatorname{sinc}_0(h)=\sin(h)/h$ with value 1 at zero. From pose $(x,y,\theta)$, use
$$d=v\Delta t\operatorname{sinc}_0(h),\quad x'=x+d\cos(\theta+h),\quad y'=y+d\sin(\theta+h),\quad \theta'=\operatorname{wrap}(\theta+2h).$$
Position is in metres; angles are radians. NumPy sinc uses $\sin(\pi z)/(\pi z)$, so pass $h/\pi$. This is a no-slip kinematic model.

## Visual trace

| Wheel rates, radius=1, track=2 | v | yaw rate | Motion |
|---|---|---|---|
| [1,1] | 1 m/s | 0 | straight |
| [-1,1] | 0 | 1 rad/s | rotate in place |
| [0,2] | 1 m/s | 1 rad/s | unit-radius arc |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `initial_pose=[0,0,0], wheel_rates=[[1,1],[1,1]], dt=1, radius=1, track=2` → `[[0,0,0],[1,0,0],[2,0,0]]`.
2. Same parameters with one rate row `[[0,2]]` → final `[sin(1),1-cos(1),1]`, approximately `[0.84147098,0.45969769,1]`.

## Why this matters on a robot

Wheel slip, unequal radii, and an incorrect track width create odometry drift. This deterministic rollout checks the kinematic component; it does not estimate those parameters or model wheel-ground forces.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.

dt, radius and track must each be at least 1e-9 in their declared units; smaller values raise ValueError.
