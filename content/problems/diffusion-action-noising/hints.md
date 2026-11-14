# Progressive hints

## Hint 1

The evaluator supplies the particular noise tensor. Your function constructs one forward sample and returns that noise as the target; it should not call a random generator or run reverse denoising.

## Hint 2

Gather one cumulative schedule value for each batch item. A gathered `(B,)` vector needs two singleton axes to broadcast across `(B,H,D)` actions.

## Hint 3

Use square roots for both coefficients. If a mask exists, expand `(B,H)` along the final dimension and zero both returned tensors at padded positions. Validate the original tensors before masking and preserve their gradients.
