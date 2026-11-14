# Solution: follow consumers, then remove the roots

Validate every declaration before traversal, including when nothing changed. Build one set of outgoing consumers per node, so repeated edges have no extra effect.

Keep two sets: the original changed roots and all visited nodes. Initialize both from changed. A stack or queue visits each reachable consumer once; marking nodes when they are discovered makes feedback cycles terminate. Finally subtract the complete root set and sort the remaining IDs.

The distinction between these sets handles overlapping changes: if both a dataset and its downstream model changed, the model remains a root and is not reported as another affected consumer.

Building and traversing the graph takes O(V+E) time; final sorting costs at most O(V log V). Memory is O(V+E). Iterative traversal also supports the documented large graphs without relying on Python's recursion limit. The result plans review work; it cannot discover undeclared consumers or prove robot safety.
