import re


def feedback_groups(nodes, edges):
    def identifier(value):
        return isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", value) is not None
    if not isinstance(nodes, list) or not isinstance(edges, list) or len(nodes) > 10000 or len(edges) > 50000:
        raise ValueError("Invalid graph containers or size")
    if any(not identifier(node) for node in nodes) or len(set(nodes)) != len(nodes):
        raise ValueError("Invalid or duplicate node IDs")
    outgoing = {node: set() for node in nodes}
    incoming = {node: set() for node in nodes}
    for edge in edges:
        if not isinstance(edge, tuple) or len(edge) != 2 or any(not identifier(v) or v not in outgoing for v in edge):
            raise ValueError("Invalid edge")
        source, target = edge
        outgoing[source].add(target)
        incoming[target].add(source)
    seen, finished = set(), []
    for root in nodes:
        if root in seen:
            continue
        seen.add(root)
        stack = [(root, iter(outgoing[root]))]
        while stack:
            node, children = stack[-1]
            child = next(children, None)
            if child is None:
                finished.append(node)
                stack.pop()
            elif child not in seen:
                seen.add(child)
                stack.append((child, iter(outgoing[child])))
    assigned, groups = set(), []
    for root in reversed(finished):
        if root in assigned:
            continue
        assigned.add(root)
        stack, component = [root], []
        while stack:
            node = stack.pop()
            component.append(node)
            for parent in incoming[node]:
                if parent not in assigned:
                    assigned.add(parent)
                    stack.append(parent)
        if len(component) > 1 or root in outgoing[root]:
            groups.append(sorted(component))
    return sorted(groups, key=lambda group: group[0])
