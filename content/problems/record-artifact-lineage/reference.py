from collections import deque
import re


def lineage_record(artifacts, parents, target):
    def identifier(value):
        return isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", value) is not None
    if not isinstance(artifacts, dict) or not 1 <= len(artifacts) <= 10000 or not isinstance(parents, dict):
        raise ValueError("Invalid artifact mappings")
    for name, record in artifacts.items():
        if not identifier(name) or not isinstance(record, tuple) or len(record) != 2:
            raise ValueError("Invalid artifact record")
        kind, digest = record
        if not isinstance(kind, str) or kind not in ("dataset", "transform", "model", "evaluator") or not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            raise ValueError("Invalid kind or digest")
    if set(parents) != set(artifacts) or not identifier(target) or target not in artifacts:
        raise ValueError("Parent keys or target invalid")
    dependencies, outgoing, indegree = {}, {name: [] for name in artifacts}, {}
    total = 0
    for name, inputs in parents.items():
        if not isinstance(inputs, list) or any(not identifier(v) or v not in artifacts for v in inputs):
            raise ValueError("Invalid parent references")
        total += len(inputs)
        if total > 50000:
            raise ValueError("Too many references")
        dependencies[name] = set(inputs)
        indegree[name] = len(dependencies[name])
        for parent in dependencies[name]:
            outgoing[parent].append(name)
    ready = deque(name for name in artifacts if indegree[name] == 0)
    completed = 0
    while ready:
        node = ready.popleft()
        completed += 1
        for child in outgoing[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    if completed != len(artifacts):
        raise ValueError("Lineage must be acyclic")
    visited, stack = {target}, [target]
    while stack:
        for parent in dependencies[stack.pop()]:
            if parent not in visited:
                visited.add(parent)
                stack.append(parent)
    return [(name, *artifacts[name]) for name in sorted(visited)]
