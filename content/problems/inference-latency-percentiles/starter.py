"""Compute p50, p90, and p99 Inference Latency."""


def latency_percentiles(start_ns: list[int], end_ns: list[int]) -> dict[str, float | None]:
    """Return nearest-rank latency values in milliseconds."""
    raise NotImplementedError("Implement latency_percentiles")
