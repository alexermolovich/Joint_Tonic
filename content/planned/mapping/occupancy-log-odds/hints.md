# Progressive hints

## Hint 1

Convert probabilities to odds before taking a logarithm. A 0.5 probability contributes zero log odds.

## Hint 2

The inverse model already contains its assumed prior. Remove that prior before adding evidence to the existing cell belief.

## Hint 3

Clamp the log-odds state after accumulation, then convert to probability. Do not clamp probabilities to exact zero or one before applying the logarithm.

