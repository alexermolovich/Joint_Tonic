# Hints

1. Count distinct unfinished parents for every node, including isolated nodes.
2. Keep all ready IDs in a min-heap. Insert newly ready consumers after each removal.
3. Compare the emitted count with the declared node count. Fewer emitted nodes means a cycle; raise instead of returning a prefix.

Avoid repeatedly scanning all edges for every stage; the maximum-size fixture rewards adjacency and indegree bookkeeping without a hardware-dependent timing score.
