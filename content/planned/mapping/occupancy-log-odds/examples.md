# Hand-verified worked examples

**Planning examples, not executable tests.** Values below define the intended contract and must be reproduced by the future reference implementation.

## Example 1: two consistent obstacle observations

Inputs: current log odds = 0, inverse probability = 0.8, prior = 0.5, limits = (-10,10).

After one update: log odds = $\log4\approx1.3862943611$; probability = 0.8.

Apply the same evidence again: log odds = $\log16\approx2.7725887222$; probability = $16/17\approx0.9411764706$.

## Example 2: explicit prior correction

Inputs: current log odds = 0, inverse probability = 0.8, prior = 0.6, limits = (-10,10).

Expected log odds: $\log4-\log1.5=\log(8/3)\approx0.9808292530$.

Expected probability: $(8/3)/(1+8/3)=8/11\approx0.7272727273$.

The result is not 0.8 because the inverse model's prior was not neutral.

## Boundary

An inverse probability of exactly 0 or 1 is invalid. It represents infinite log odds and must be rejected by the planned contract.

