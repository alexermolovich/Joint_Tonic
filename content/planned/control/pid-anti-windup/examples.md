# Hand-verified worked examples

**Planning examples, not executable tests.** Values below define the intended contract and must be reproduced by the future reference implementation.

## Example 1: prevent positive windup

Inputs: error=1 rad, previous_error=1 rad, integral=0, dt=0.1 s, gains=(2,1,0), limits=(-1,1).

Candidate integral=0.1 rad·s; candidate command=2.1. It saturates upward while error is positive.

Expected: command=1; next integral=0; derivative=0.

## Example 2: integrate a feasible command

Inputs: error=0.2 rad, previous_error=0.2 rad, integral=0, dt=0.1 s, gains=(2,1,0), limits=(-1,1).

Candidate integral=0.02 rad·s; command=$2(0.2)+0.02=0.42$.

Expected: command=0.42; next integral=0.02; derivative=0.

## Boundary

dt=0 is invalid. A saturated command does not justify silently dividing by zero or skipping derivative validation.

