"""Original sequential edge-inference teaching gate."""
import numbers
import numpy as np


def _finite(value):
    return isinstance(value, numbers.Real) and not isinstance(value, (bool, np.bool_)) and np.isfinite(value)


def release_gate(samples, thresholds):
    if not isinstance(samples, list) or not isinstance(thresholds, dict):
        raise ValueError("samples must be a list and thresholds a dictionary")
    if type(thresholds.get("min_samples")) is not int or thresholds["min_samples"] < 1:
        raise ValueError("min_samples must be a positive integer")
    for key in ("min_accuracy", "max_p99_ms", "min_throughput_qps", "max_memory_mb"):
        if key not in thresholds or not _finite(thresholds[key]) or thresholds[key] < 0:
            raise ValueError(f"invalid {key}")
    if thresholds["min_accuracy"] > 1:
        raise ValueError("min_accuracy must be in [0,1]")
    drop = thresholds.get("max_slice_drop", 1)
    baseline = thresholds.get("baseline_accuracy", {})
    if not _finite(drop) or not 0 <= drop <= 1 or not isinstance(baseline, dict):
        raise ValueError("invalid baseline policy")
    if any(not isinstance(k, str) or not _finite(v) or not 0 <= v <= 1 for k, v in baseline.items()):
        raise ValueError("invalid baseline accuracy")
    groups = {}
    for sample in samples:
        if not isinstance(sample, dict):
            raise ValueError("sample must be a dictionary")
        if type(sample.get("valid", True)) is not bool or type(sample.get("warmup", False)) is not bool:
            raise ValueError("sample flags must be bool")
        if not sample.get("valid", True) or sample.get("warmup", False):
            continue
        if not isinstance(sample.get("hardware"), str) or not sample["hardware"]:
            raise ValueError("hardware must be a nonempty string")
        if (not _finite(sample.get("latency_ms")) or sample["latency_ms"] <= 0
                or not _finite(sample.get("memory_mb")) or sample["memory_mb"] < 0
                or type(sample.get("correct")) is not bool
                or not isinstance(sample.get("slice", "all"), str)):
            raise ValueError("invalid measured sample")
        groups.setdefault(sample["hardware"], []).append(sample)
    metrics, reasons = {}, []
    for hardware, rows in sorted(groups.items()):
        latency = np.array([r["latency_ms"] for r in rows], dtype=np.float64)
        accuracy = sum(r["correct"] for r in rows) / len(rows)
        p50, p90, p99 = np.quantile(latency, [0.5, 0.9, 0.99], method="linear")
        slices = {}
        for name in sorted({r.get("slice", "all") for r in rows}):
            subset = [r for r in rows if r.get("slice", "all") == name]
            slices[name] = sum(r["correct"] for r in subset) / len(subset)
        result = {"count": len(rows), "accuracy": accuracy, "p50_ms": float(p50),
                  "p90_ms": float(p90), "p99_ms": float(p99),
                  "throughput_qps": float(1000 * len(rows) / latency.sum()),
                  "peak_memory_mb": float(max(r["memory_mb"] for r in rows)), "slices": slices}
        metrics[hardware] = result
        rules = (("sample_count", len(rows) < thresholds["min_samples"]),
                 ("accuracy", accuracy < thresholds["min_accuracy"]),
                 ("p99_ms", p99 > thresholds["max_p99_ms"]),
                 ("throughput_qps", result["throughput_qps"] < thresholds["min_throughput_qps"]),
                 ("memory_mb", result["peak_memory_mb"] > thresholds["max_memory_mb"]))
        reasons.extend(f"{hardware}:{name}" for name, failed in rules if failed)
        for name, previous in sorted(baseline.items()):
            if name not in slices:
                reasons.append(f"{hardware}:slice_missing:{name}")
            elif previous - slices[name] > drop + 1e-12:
                reasons.append(f"{hardware}:slice_regression:{name}")
    if not groups:
        reasons = ["no_samples"]
    return {"passed": not reasons, "metrics": metrics, "reasons": reasons}
