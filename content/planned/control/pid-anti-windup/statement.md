# Take a PID Step with Conditional Anti-Windup

**Status: planned; no runnable implementation yet.**

A robot joint cannot execute commands beyond its actuator limits. Compute a discrete PID command without allowing the integral state to keep accumulating error that pushes farther into saturation.

## Contract

Planned function: pid_step(error, previous_error, integral, dt, gains, output_limits).

Errors are radians at consecutive control instants. The integral stores accumulated error in radian-seconds; dt is positive seconds. Gains (kp,ki,kd) are finite nonnegative scalars with units that make every term an actuator command. Limits are finite and increasing.

Compute derivative = (error-previous_error)/dt and candidate integral = integral + error*dt. Form the candidate command with that integral. Reject the candidate integral when the command exceeds the upper limit and error is positive, or falls below the lower limit and error is negative. Otherwise accept it. Recompute using the accepted integral, then clamp the output. Return command, next integral, and derivative.

## Scope and assessment

Use the caller-supplied previous error; derivative-on-measurement and filtering are later extensions. Reject nonfinite inputs and nonpositive time. Grade the exact conditional integration rule, saturation direction, and unsaturated recovery. See [examples.md](examples.md). This is a planned component.

