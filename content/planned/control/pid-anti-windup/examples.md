# Worked examples

## Prevent outward windup

Input: error=1, previous_error=1, integral=0, dt=0.1, gains=(2,1,0), output_limits=(-1,1).

Candidate integral 0.1 produces command 2.1. Error pushes farther upward into saturation: reject integration and return (1.0,0.0,0.0).

## Accept feasible integration

Input: error=0.2, previous_error=0.2, integral=0, dt=0.1, gains=(2,1,0), output_limits=(-1,1).

Candidate integral 0.02 gives command 0.42. Return (0.42,0.02,0.0).

## Allow unwinding while still saturated

Input: error=-0.5, previous_error=-0.5, integral=3, dt=1, gains=(0,1,0), output_limits=(-1,1).

Accept integral 2.5 because the error reduces the accumulated state. Return (1.0,2.5,0.0).
