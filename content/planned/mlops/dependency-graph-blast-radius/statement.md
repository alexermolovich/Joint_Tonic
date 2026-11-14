# Compute Dependency-Graph Blast Radius

**Draft 0.1.0 — not runnable yet.**

A calibration change can affect features, a policy, and monitoring reports. Return the declared consumers needing impact review.

## Function contract

~~~python
def blast_radius(nodes: list[str], edges: list[tuple[str, str]],
                 changed: list[str]) -> list[str]:
    ...
~~~

An edge (producer, consumer) means the consumer uses the producer's output. IDs match the case-sensitive ASCII pattern [a-z][a-z0-9_-]{0,63}. The nodes list is unique. All edge endpoints and changed IDs must be declared. Repeated edges or changed IDs count once. Self-loops and feedback cycles are valid.

Return a new list of all nodes reachable through one or more directed edges from any changed node, **excluding every changed node**, sorted by Python's ascending string order. Preserve inputs. Structural impact does not mean each numerical output necessarily changes.

Maximum sizes: 10,000 nodes, 50,000 edges, 10,000 changed entries. This is one metadata graph snapshot, with no physical frame, time-series interpretation, or units. CPU Python objects only.

## Errors and empty inputs

Raise ValueError for invalid container types, malformed/duplicate node IDs, an edge that is not a two-item tuple, undeclared IDs, or exceeded limits. All outer containers must be lists. Validate the complete graph even for an empty changed list. Error messages are not graded. Three empty lists return []; an empty changed list on any valid graph also returns [].

## Worked example 1 — calibration fan-out

~~~python
nodes = ["calib", "images", "features", "policy", "monitor"]
edges = [("calib", "features"), ("images", "features"),
         ("features", "policy"), ("policy", "monitor")]
changed = ["calib"]
# Output: ["features", "monitor", "policy"]
~~~

Images feed features but are not downstream of calibration. Return lexical order, not traversal order.

## Worked example 2 — feedback

~~~python
nodes = ["data", "policy", "log", "dashboard"]
edges = [("data", "policy"), ("policy", "log"),
         ("log", "data"), ("log", "dashboard")]
changed = ["policy", "policy"]
# Output: ["dashboard", "data", "log"]
~~~

The loop reaches policy again. Mark it visited but exclude it from the output because it is a changed root.
