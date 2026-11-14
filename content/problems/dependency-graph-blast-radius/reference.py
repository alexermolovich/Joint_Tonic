import re


def blast_radius(nodes: list[str], edges: list[tuple[str, str]],
                 changed: list[str]) -> list[str]:
    def valid_id(value):
        return isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", value) is not None

    if not all(isinstance(value, list) for value in (nodes, edges, changed)):
        raise ValueError("Expected lists")
    if len(nodes) > 10000 or len(edges) > 50000 or len(changed) > 10000:
        raise ValueError("Input limit exceeded")
    if not all(valid_id(node) for node in nodes) or len(set(nodes)) != len(nodes):
        raise ValueError("Invalid or duplicate node")
    children = {node: set() for node in nodes}
    for edge in edges:
        if not isinstance(edge, tuple) or len(edge) != 2:
            raise ValueError("Expected a producer-consumer tuple")
        if any(not valid_id(node) or node not in children for node in edge):
            raise ValueError("Undeclared endpoint")
        children[edge[0]].add(edge[1])
    if any(not valid_id(node) or node not in children for node in changed):
        raise ValueError("Undeclared changed node")
    roots = set(changed)
    visited = set(roots)
    pending = list(roots)
    while pending:
        node = pending.pop()
        for consumer in children[node]:
            if consumer not in visited:
                visited.add(consumer)
                pending.append(consumer)
    return sorted(visited - roots)
