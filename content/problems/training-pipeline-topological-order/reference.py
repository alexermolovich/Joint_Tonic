import heapq
import re


def schedule_pipeline(nodes: list[str],
                      edges: list[tuple[str, str]]) -> list[str]:
    def valid_id(value):
        return isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", value) is not None

    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("Expected lists")
    if len(nodes) > 10000 or len(edges) > 50000:
        raise ValueError("Input limit exceeded")
    if not all(valid_id(node) for node in nodes) or len(set(nodes)) != len(nodes):
        raise ValueError("Invalid or duplicate node")
    children = {node: set() for node in nodes}
    indegree = {node: 0 for node in nodes}
    for edge in edges:
        if not isinstance(edge, tuple) or len(edge) != 2:
            raise ValueError("Expected a producer-consumer tuple")
        if any(not valid_id(node) or node not in children for node in edge):
            raise ValueError("Undeclared endpoint")
        producer, consumer = edge
        if consumer not in children[producer]:
            children[producer].add(consumer)
            indegree[consumer] += 1
    ready = [node for node in nodes if indegree[node] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for consumer in children[node]:
            indegree[consumer] -= 1
            if indegree[consumer] == 0:
                heapq.heappush(ready, consumer)
    if len(order) != len(nodes):
        raise ValueError("Pipeline contains a cycle")
    return order
