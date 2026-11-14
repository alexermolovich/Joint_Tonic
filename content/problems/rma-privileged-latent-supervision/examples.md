## Example 1

One factor 0, weight 1, bias 0, prediction 2 and a valid row yield teacher target 0, per-state and total loss 4, and prediction gradient 4.

## Example 2

Two target channels [0, 0] and prediction [1, -1] yield loss 1 and gradient [1, -1]. An entirely invalid batch has zero loss, targets and gradients, with NaN per-state losses.
