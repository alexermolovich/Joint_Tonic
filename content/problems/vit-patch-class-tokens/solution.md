# Solution

Validate ranks and all dimensions before broadcasting. Multiply patches by the shared projection, add patch bias, expand the class token across B, concatenate it before the patch rows, and add all N+1 positions. Keep normal PyTorch operations to preserve gradients to every input, including shared parameters. Complexity is O(BNFD) for projection plus O(BND) storage. The class token bypasses the patch affine transform.
