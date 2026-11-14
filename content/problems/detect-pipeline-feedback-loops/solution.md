# Solution approach

Validate the snapshot; run iterative Kosaraju traversal, retaining cyclic components. O(V+E+V log V) time including deterministic sorting, O(V+E) storage. No recursion dependency.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep unknown evidence distinct from a passing result. The cases exercise the worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
