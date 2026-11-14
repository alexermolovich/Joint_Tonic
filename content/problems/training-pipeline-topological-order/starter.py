"""Topologically Schedule a Training Pipeline DAG."""


def schedule_pipeline(nodes: list[str],
                      edges: list[tuple[str, str]]) -> list[str]:
    """Return the smallest-ready-first full order, or reject cycles."""
    raise NotImplementedError("Implement schedule_pipeline")
