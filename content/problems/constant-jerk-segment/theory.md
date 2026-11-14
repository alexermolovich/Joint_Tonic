# Integrate a Constant-Jerk Motion Segment

## Intuition

Constant jerk means acceleration changes linearly. Integrating that line produces a quadratic velocity and cubic position; each term must carry the same units as the quantity it contributes to.

## Mathematics and conventions

For joint index $d$, duration $t$ in seconds, initial position $q_d$, velocity $v_d$, acceleration $a_d$, and constant jerk $j_d$,

$$a_d(t)=a_d+j_dt,\quad v_d(t)=v_d+a_dt+\frac12j_dt^2,\quad q_d(t)=q_d+v_dt+\frac12a_dt^2+\frac16j_dt^3.$$

The four input vectors have shape $D$ and units rad, rad/s, rad/s², rad/s³ respectively. These equations are exact under constant jerk; a piecewise profile must restart from each segment's end state.

## Visual computation trace

| Quantity | At t=0 | At t=0.5 s, jerk=2 rad/s³ |
| --- | --- | --- |
| Acceleration | 0 | 1 rad/s² |
| Velocity | 0 | 0.25 rad/s |
| Position | 0 | 1/24 rad |

## Worked examples

1. Initial `q=v=a=[0.]`, jerk `[2.]`, duration `0.5` gives position `[1/24]`, velocity `[0.25]`, acceleration `[1.]` in the stated units.
2. Initial `q=[1.]`, `v=[2.]`, `a=[3.]`, jerk `[4.]`, duration `0` returns `[1.]`, `[2.]`, `[3.]` in fresh arrays.

## Why this matters on a robot

Dropping the cubic coefficient can give a plausible velocity but the wrong endpoint. This is only kinematic integration: a trajectory can satisfy these equations and still violate torque, collision, or joint-position constraints.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2105.04830). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
