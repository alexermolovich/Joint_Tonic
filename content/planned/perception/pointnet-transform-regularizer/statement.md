# Regularize a Learned Feature Transform

Implement feature_transform_penalty(transforms). Input is a finite CPU PyTorch tensor float32 or float64, shape (B,D,D), 1<=B<=256, 1<=D<=64, at most1,000,000 elements, abs values<=10. Return a scalar tensor of the same dtype/device equal to the batch mean of squared Frobenius norms ||A A.T-I||_F^2. Sum over both matrix axes and average only over B. Preserve gradients, inputs and new output storage. TypeError for non-tensor; ValueError for other violations. Empty batches rejected. This penalizes deviation from orthogonality; it does not enforce determinant+1. Feature coordinates are dimensionless, not necessarily a physical rotation. No T-Net, optimizer, classifier, or full PointNet training.

## Worked examples

## Unequal scaling

transforms=[[[2,0],[0,1]]], float64. A A.T-I=diag(3,0), so loss=9.

## Average over clouds only

transforms=[[[1,0],[0,1]],[[2,0],[0,1]]], float32. Per-cloud penalties0 and9 give loss4.5. Do not divide by the four matrix entries.
