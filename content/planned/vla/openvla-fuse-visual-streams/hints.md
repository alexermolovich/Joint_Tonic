# Hints

1. Check equal batch and token dimensions before concatenating along the final axis.
2. Combine both Boolean masks, and apply the result after the affine projection.
3. Keep floating operations in PyTorch so all required gradients survive.
