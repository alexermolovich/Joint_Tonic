# PID with Integral Anti-Windup

Implement **pid_step(error, previous_error, integral, dt, gains, output_limits)**.

The first four inputs are finite Python or NumPy real scalars excluding bool; 0<dt<=1e6. Other scalar magnitudes are <=1e6. gains=(kp,ki,kd) contains three finite nonnegative values <=1e6. output_limits=(lower,upper) contains two finite values of magnitude <=1e6, lower<upper. Reject numeric strings, booleans, complex data, malformed shapes, nonfinite inputs and nonfinite intermediate calculations with ValueError.

Errors refer to consecutive samples of one joint in radians on one clock; integral is radian-seconds and dt seconds. Gain units are command/rad, command/(rad*s), command*s/rad. Return three Python floats (command,next_integral,derivative).

Compute derivative=(error-previous_error)/dt, candidate integral Ic=integral+error*dt, and candidate command uc=kp*error+ki*Ic+kd*derivative. Reject Ic exactly when (uc>upper and error>0) or (uc<lower and error<0). Otherwise accept it, including exact equality. Recompute effort using the accepted integral, then clip to the limits. Inputs remain unchanged.

No derivative filtering, simulator integration or motor safety guarantee.

NumPy CPU; numerical tolerance rtol=1e-7, atol=1e-9. Masks, shapes and errors are exact.

## Worked examples

### Prevent outward windup

Input: error=1, previous_error=1, integral=0, dt=0.1, gains=(2,1,0), output_limits=(-1,1).

Candidate integral 0.1 produces command 2.1. Error pushes farther upward into saturation: reject integration and return (1.0,0.0,0.0).

### Accept feasible integration

Input: error=0.2, previous_error=0.2, integral=0, dt=0.1, gains=(2,1,0), output_limits=(-1,1).

Candidate integral 0.02 gives command 0.42. Return (0.42,0.02,0.0).

### Allow unwinding while still saturated

Input: error=-0.5, previous_error=-0.5, integral=3, dt=1, gains=(0,1,0), output_limits=(-1,1).

Accept integral 2.5 because the error reduces the accumulated state. Return (1.0,2.5,0.0).

## Hints

1. Compute the candidate integral first.

2. Check whether the error pushes outward, not just whether output saturates.

3. Recompute effort from the accepted integral before clipping.
