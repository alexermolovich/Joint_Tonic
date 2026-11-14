# Hints

1. Validate artifacts, matching parent keys and all declared references.

2. Check the entire graph for cycles before traversing the target ancestry.

3. Use an iterative parent traversal with a visited-ID set, then emit sorted rows.
