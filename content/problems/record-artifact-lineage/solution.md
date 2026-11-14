# Solution approach

Validate the DAG using a Kahn queue, then traverse target parents iteratively. O(V+E+V log V) time including output sort; O(V+E) memory. No filesystem or artifact loader.

Validate documented types and bounds before the core operation. Preserve supplied metadata, use deterministic output ordering, and keep unknown evidence distinct from a passing result. The cases exercise the worked examples, meaningful boundary/error behavior, input preservation and a bounded realistic workload.
