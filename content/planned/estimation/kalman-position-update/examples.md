# Hand-verified worked examples

**Planning examples, not executable tests.** Values below define the intended contract and must be reproduced by the future reference implementation.

## Example 1: a precise beacon corrects uncertain odometry

Inputs: mean = 2 m, variance = 4 m², measurement = 5 m, measurement variance = 1 m².

Expected: innovation = 3 m; gain = 0.8; posterior mean = 4.4 m; posterior variance = 0.8 m².

Calculation: $K=4/(4+1)$ and $P^+=0.2^2(4)+0.8^2(1)$.

## Example 2: the same reading with more noise

Inputs: mean = 2 m, variance = 4 m², measurement = 5 m, measurement variance = 16 m².

Expected: innovation = 3 m; gain = 0.2; posterior mean = 2.6 m; posterior variance = 3.2 m².

Calculation: $K=4/20$; $P^+=0.8^2(4)+0.2^2(16)=3.2$.

## Boundary

A prior variance of zero gives gain zero and preserves the prior mean and variance. A measurement variance of zero is outside this lesson's contract.

