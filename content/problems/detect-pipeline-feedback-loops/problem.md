# Detect Feedback Loops in an ML Pipeline

Implement:

~~~python
def feedback_groups(nodes: list[str],
                    edges: list[tuple[str, str]]) -> list[list[str]]:
    ...
~~~

An edge (u,v) means that u influences v. Return every maximal strongly connected group that contains a directed cycle: either two or more nodes, or one node with an explicit self-loop. Sort names inside each group; sort groups by their first name. Do not return acyclic downstream nodes. Overlapping cycles belong to one group.

Both inputs must be Python lists. Nodes are unique strings matching ASCII [a-z][a-z0-9_-]{0,63}. Each edge is a tuple of exactly two declared IDs. Duplicate edges have no extra effect. At most 10,000 nodes and 50,000 supplied edges; an empty graph returns []. Self-loops and disconnected components are allowed. All malformed inputs, unknown IDs, duplicate node IDs and exceeded bounds raise ValueError. Validate the whole graph. Return fresh lists and preserve inputs.

This is a directed logical influence graph, not a physical robot frame or a legal training execution DAG. It has no numeric timestamps, tensor/device rules, or internal random sampling.

## Worked examples

### Feedback with an acyclic consumer

~~~python
nodes = ["dataset","train","policy","logger","dashboard"]
edges = [("dataset","train"),("train","policy"),("policy","logger"),
         ("logger","dataset"),("logger","dashboard")]
feedback_groups(nodes, edges)
# [["dataset","logger","policy","train"]]
~~~

The dashboard is reachable from the cycle but cannot return to it, so it is excluded.

### Separate loops, deterministic output

~~~python
nodes = ["monitor","b","a","isolated"]
edges = [("b","a"),("a","b"),("monitor","monitor"),("a","b")]
feedback_groups(nodes, edges)
# [["a","b"],["monitor"]]
~~~

The repeated edge changes nothing. The isolated node has no cycle.

## Source and scope

The paper motivates inspecting direct and indirect feedback. Strongly connected components are an original finite-graph teaching tool; declared graph cycles do not prove a harmful statistical feedback effect, and absent edges can hide real loops. [Primary source](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html).
