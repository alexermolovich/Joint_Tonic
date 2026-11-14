"""Invalidate Cached Artifacts After an Upstream Change."""


def invalidated_artifacts(dependencies: dict[str, list[str]],
                          changed: list[str], cached: list[str]) -> list[str]:
    """Return stale cached IDs; dependencies maps consumers to their parents."""
    raise NotImplementedError("Implement invalidated_artifacts")
