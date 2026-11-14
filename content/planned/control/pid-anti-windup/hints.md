# Progressive hints

## Hint 1

Calculate the candidate integral separately from the saved state so it can be rejected.

## Hint 2

Saturation alone is not enough: check whether the error pushes farther into the saturated direction.

## Hint 3

After choosing the next integral, recompute and clamp the command. Do not return the unclamped candidate or keep a rejected integral update.

