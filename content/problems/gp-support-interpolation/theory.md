# Interpolate a Trajectory Between Support States

## Intuition

Endpoint velocities determine how the path enters and leaves an interval. Matching only positions loses that information and can create a discontinuous commanded velocity at support states.

## Mathematics and conventions

For elapsed time $s=ut$, let $q_0,v_0,q_1,v_1\in\mathbb R^D$ be endpoint joint states. Define

$$h_{00}=2u^3-3u^2+1,\ h_{10}=u^3-2u^2+u,\ h_{01}=-2u^3+3u^2,\ h_{11}=u^3-u^2.$$

Then $q(u)=h_{00}q_0+h_{10}tv_0+h_{01}q_1+h_{11}tv_1$ and

$$v(u)=\frac{1}{t}\frac{dq}{du}.$$

Positions use radians, velocities rad/s, duration seconds, and u is dimensionless. The four boundary conditions determine this cubic uniquely. For the specified constant-velocity GP it is also the conditional mean; the calculation here is the explicit endpoint-constrained cubic, with no learned kernel or covariance output.

## Visual computation trace

| Fraction | Position for q0=0,q1=1,v0=v1=0,t=2 | Velocity |
| --- | --- | --- |
| 0 | 0 rad | 0 rad/s |
| 0.5 | 0.5 rad | 0.75 rad/s |
| 1 | 1 rad | 0 rad/s |

## Worked examples

1. Start `[[0.,0.]]`, end `[[1.,0.]]`, duration `2`, fractions `[0.5]` give position `[[0.5]]` and velocity `[[0.75]]`.
2. Start `[[0.,2.]]`, end `[[4.,2.]]`, duration `2`, fractions `[0.,0.5,1.]` give positions `[[0.],[2.],[4.]]` and velocities `[[2.],[2.],[2.]]`.

## Why this matters on a robot

A smooth interpolant can overshoot joint bounds or cross an obstacle. Forgetting to divide the derivative by duration yields a fraction derivative with the wrong physical units.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1707.07383). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
