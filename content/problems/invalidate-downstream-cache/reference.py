import re


def invalidated_artifacts(dependencies: dict[str, list[str]],
                          changed: list[str], cached: list[str]) -> list[str]:
    def valid_id(value):
        return isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", value) is not None

    if not isinstance(dependencies, dict) or not isinstance(changed, list) or not isinstance(cached, list):
        raise ValueError("Expected dependency dictionary and ID lists")
    if len(dependencies) > 10000 or len(changed) > 10000 or len(cached) > 10000:
        raise ValueError("Input limit exceeded")
    if not all(valid_id(node) for node in dependencies):
        raise ValueError("Invalid artifact ID")
    if not all(isinstance(parents, list) for parents in dependencies.values()):
        raise ValueError("Expected parent lists")
    if sum(map(len, dependencies.values())) > 50000:
        raise ValueError("Parent entry limit exceeded")
    children = {node: set() for node in dependencies}
    indegree = {}
    for node, parents in dependencies.items():
        if any(not valid_id(parent) or parent not in dependencies for parent in parents):
            raise ValueError("Undeclared parent")
        distinct = set(parents)
        indegree[node] = len(distinct)
        for parent in distinct:
            children[parent].add(node)
    for collection in (changed, cached):
        if any(not valid_id(node) or node not in dependencies for node in collection):
            raise ValueError("Undeclared artifact")
    ready = [node for node, count in indegree.items() if count == 0]
    processed = 0
    while ready:
        node = ready.pop()
        processed += 1
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    if processed != len(dependencies):
        raise ValueError("Dependency graph contains a cycle")
    affected = set(changed)
    pending = list(affected)
    while pending:
        for child in children[pending.pop()]:
            if child not in affected:
                affected.add(child)
                pending.append(child)
    return sorted(affected.intersection(cached))
