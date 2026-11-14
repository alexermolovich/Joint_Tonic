# Solution

Validate both tensors and compute validation norms in float64, as the contract requires. Divide each original tensor by its own last-axis norm with keepdim=True. The denominator has shape (B,1), so each sample is normalized independently. These ordinary differentiable operations preserve autograd and allocate new outputs. Cost is O(BD) time and output storage. Avoid detach, normalization across B, or adding an undocumented epsilon.
