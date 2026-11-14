# Solution

Compute A @ A.transpose(-1,-2), subtract a D×D identity, square and sum over both matrix axes, then average over B. The reduction order defines the loss scale. Keep autograd connected. Reflections have zero penalty too, so this is feature orthogonality regularization rather than a constraint to proper spatial rotations. Time is O(BD³), temporary storage O(BD²).
