# Hints

1. Write the edge direction in words before constructing adjacency.
2. Seed a visited set with all changed IDs and expand newly reached consumers.
3. Subtract the original root set and sort the final IDs. Validate undeclared references first.

Common mistake: rejecting cycles. They are valid here; the later pipeline scheduler has a different contract.
