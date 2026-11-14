# Progressive hints

## Hint 1

Reshape tau to(B,1,1). Compute the interpolant and target separately; the target does not depend on tau.

## Hint 2

Use linear tau and1-tau coefficients. Square roots belong to a different noising parameterization.

## Hint 3

Broadcast valid with a final axis and zero both outputs. Keep all arithmetic on tensors so gradients through tau and the two endpoint tensors survive.
