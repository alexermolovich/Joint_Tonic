# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
