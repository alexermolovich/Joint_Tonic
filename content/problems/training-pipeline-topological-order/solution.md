# Solution: maintain the ready set after every stage

Deduplicate edges while recording outgoing consumers and their unfinished-parent counts. A node with zero unfinished parents is ready. Put all initially ready IDs into a min-heap.

Remove the smallest ready ID, append it, and decrement each of its consumers' remaining-parent counts. Insert a consumer when its count becomes zero. Because new work enters the heap immediately, the tie-break is applied at every step, not just between initial layers.

If fewer nodes are emitted than declared, some component is cyclic. Raise ValueError rather than returning an apparently successful prefix. A valid component elsewhere does not repair that cycle.

Each distinct edge is processed once, and each node enters and leaves the heap once. Complexity is O(V+E+V log V) time and O(V+E) memory. This is a deterministic precedence schedule, not a resource allocator or evidence that artifact versions are correct.
