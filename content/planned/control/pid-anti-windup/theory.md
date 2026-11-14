# Take a PID Step with Conditional Anti-Windup: theory

## Intuition

An integral term remembers persistent tracking error. That memory helps overcome a steady load or bias, but it can become harmful when the actuator is already at its limit. The controller keeps demanding more than the motor can deliver, the integral grows, and the joint may overshoot after the constraint disappears. Anti-windup limits this artificial memory growth.

## The discrete controller state

At control step $k$, error $e_k$ is desired minus measured joint angle in radians. The interval $\Delta t>0$ is seconds. Let $I_{k-1}$ be accumulated error in radian-seconds. The previous error is measured at the preceding control instant.

$$
D_k=\frac{e_k-e_{k-1}}{\Delta t},\qquad
I^*=I_{k-1}+e_k\Delta t.
$$

The proportional gain converts radians to command units. Integral and derivative gains provide corresponding conversions from radian-seconds and radians per second. No term should be added unless its resulting physical unit agrees with the others.

$$
u^*=K_pe_k+K_iI^*+K_dD_k.
$$

This lesson uses conditional integration. If $u^*>u_{\max}$ with $e_k>0$, or $u^*<u_{\min}$ with $e_k<0$, retain the old integral. Otherwise accept the candidate. Recompute the command with the accepted state and clamp it to the actuator range. An error that drives the command back toward its feasible range may still reduce the integral.

## Worked joint example

Use $K_p=2$, $K_i=1$, $K_d=0$, limits $[-1,1]$, old integral 0, error 1 rad, and interval 0.1 s. The candidate integral is 0.1 and candidate command 2.1. Positive error pushes beyond the upper limit, so the integral stays zero. The final command is clamped from 2 to 1.

With error 0.2 rad and the same initial state, the candidate command is 0.42. It is feasible, so the integral becomes 0.02 and the output remains 0.42.

## Visual explanation

Plot desired/measured angle, actuator command with limit lines, and integral state on aligned time axes. A saturation marker explains why an integration step was accepted or rejected. A numerical state table provides the same information without animation.

## Robot relevance and failure modes

Using milliseconds as seconds changes both integral and derivative behavior. Applying anti-windup only after storing the enlarged integral defeats the rule. Noise can make a raw derivative unstable, and joint-angle wrapping requires a separate error convention. This deterministic component prepares a low-level control loop that can execute higher-level learned action chunks; it does not replace actuator modeling or safety limits.

