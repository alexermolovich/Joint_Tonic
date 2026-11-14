"""Compute Dependency-Graph Blast Radius."""


def blast_radius(nodes: list[str], edges: list[tuple[str, str]],
                 changed: list[str]) -> list[str]:
    """Return sorted downstream consumers, excluding all changed roots."""
    raise NotImplementedError("Implement blast_radius")
