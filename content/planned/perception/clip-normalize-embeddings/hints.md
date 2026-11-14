# Hints

## Hint 1

Compute one norm per row, not one norm for the entire tensor and not one per feature column.

## Hint 2

Retain the feature dimension as length one in the norm tensor so division broadcasts over the intended row.

## Hint 3

Use differentiable tensor operations for the returned value. Input validation may inspect values, but the output must still connect to the original tensor.
