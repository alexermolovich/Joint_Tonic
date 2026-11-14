# Hints

1. Write a tiny example showing that dependencies[model] contains model's parents. Build the opposite adjacency for change propagation.
2. Reachability starts with changed artifacts themselves. Cache membership must not stop traversal.
3. Validate the DAG, then intersect the reached set with cached IDs and sort. Do not delete anything.

Common mistake: copying blast radius's root subtraction. A changed artifact's existing cache entry must be invalidated here.
