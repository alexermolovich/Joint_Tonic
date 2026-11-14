def latency_percentiles(start_ns: list[int], end_ns: list[int]) -> dict[str, float | None]:
    if not isinstance(start_ns, list) or not isinstance(end_ns, list):
        raise ValueError("Expected paired timestamp lists")
    if len(start_ns) != len(end_ns) or len(start_ns) > 1000000:
        raise ValueError("Invalid paired trace length")
    durations = []
    for start, end in zip(start_ns, end_ns):
        if type(start) is not int or type(end) is not int:
            raise ValueError("Timestamps must be built-in integers")
        if not 0 <= start <= 2**63 - 1 or not 0 <= end <= 2**63 - 1:
            raise ValueError("Timestamp out of range")
        duration = end - start
        if not 0 <= duration <= 10**12:
            raise ValueError("Invalid latency interval")
        durations.append(duration)
    if not durations:
        return {"p50_ms": None, "p90_ms": None, "p99_ms": None}
    durations.sort()
    count = len(durations)
    return {f"p{percent}_ms": durations[(percent * count + 99) // 100 - 1] / 1000000
            for percent in (50, 90, 99)}
