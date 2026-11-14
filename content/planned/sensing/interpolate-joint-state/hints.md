# Progressive hints

## Hint 1

Locate the source samples on either side of each camera timestamp. Received-message order does not define the correct pair.

## Hint 2

Handle exact source timestamps before rejecting a long interpolation gap. Then apply one time fraction to all joint channels.

## Hint 3

A query outside the measured range is not an interpolation. Preserve its row with NaNs and false validity, and apply the same policy to excessive internal gaps.
