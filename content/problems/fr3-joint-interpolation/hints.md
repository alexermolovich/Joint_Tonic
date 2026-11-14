## Hint 1

Validate the sample count and both seven-element input vectors before creating the output. The FR3's fourth and sixth joints cannot be zero in this model.

## Hint 2

There are `num_steps - 1` intervals. Build fractions from zero to one, including both endpoints.

## Hint 3

A fraction array shaped `(N,1)` broadcasts against a joint vector shaped `(7,)`, giving an `(N,7)` trajectory. Allocate an independent result.
