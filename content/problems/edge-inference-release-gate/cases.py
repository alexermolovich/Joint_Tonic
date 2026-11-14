"""Synthetic sequential benchmark fixtures; CC0-1.0."""
import copy
import numpy as np


def _policy(**overrides):
    result = {"min_samples": 2, "min_accuracy": 0.9, "max_p99_ms": 20.,
              "min_throughput_qps": 60., "max_memory_mb": 128.}
    result.update(overrides)
    return result


def _samples():
    return [{"hardware": "cpu", "latency_ms": 10., "correct": True, "memory_mb": 100.},
            {"hardware": "cpu", "latency_ms": 20., "correct": True, "memory_mb": 120.}]


def passing(m):
    result = m.release_gate(_samples(), _policy())
    assert result["passed"] is True and result["reasons"] == []
    metrics = result["metrics"]["cpu"]
    assert metrics["count"] == 2 and metrics["accuracy"] == 1.
    np.testing.assert_allclose([metrics["p50_ms"], metrics["p90_ms"], metrics["p99_ms"]],
                               [15., 19., 19.9])
    np.testing.assert_allclose(metrics["throughput_qps"], 2000 / 30)
    assert metrics["peak_memory_mb"] == 120. and metrics["slices"] == {"all": 1.}


def tail_failure(m):
    result = m.release_gate(_samples(), _policy(max_p99_ms=19))
    assert result["passed"] is False and result["reasons"] == ["cpu:p99_ms"]


def quality_failure(m):
    samples = _samples()
    samples[0]["correct"] = False
    result = m.release_gate(samples, _policy())
    assert result["metrics"]["cpu"]["accuracy"] == 0.5
    assert result["reasons"] == ["cpu:accuracy"]


def sample_count(m):
    result = m.release_gate(_samples()[:1], _policy())
    assert result["reasons"] == ["cpu:sample_count"]


def exclusions(m):
    result = m.release_gate(_samples() + [{"warmup": True}, {"valid": False}], _policy())
    assert result["passed"] and result["metrics"]["cpu"]["count"] == 2


def no_samples(m):
    assert m.release_gate([], _policy()) == {"passed": False, "metrics": {}, "reasons": ["no_samples"]}
    assert m.release_gate([{"valid": False}], _policy())["reasons"] == ["no_samples"]


def hardware_groups(m):
    samples = _samples()
    slow = [dict(row, hardware="arm", latency_ms=40.) for row in _samples()]
    result = m.release_gate(samples + slow, _policy())
    assert list(result["metrics"]) == ["arm", "cpu"]
    assert result["reasons"] == ["arm:p99_ms", "arm:throughput_qps"]


def all_failures_in_order(m):
    policy = _policy(min_samples=4, min_accuracy=1., max_p99_ms=1.,
                     min_throughput_qps=1000., max_memory_mb=10.)
    samples = _samples()
    samples[0]["correct"] = False
    assert m.release_gate(samples, policy)["reasons"] == [
        "cpu:sample_count", "cpu:accuracy", "cpu:p99_ms", "cpu:throughput_qps", "cpu:memory_mb"]


def slices(m):
    samples = _samples()
    samples[0].update(slice="night", correct=False)
    samples[1].update(slice="day")
    policy = _policy(min_accuracy=0., baseline_accuracy={"night": 0.9, "fog": 1.}, max_slice_drop=0.1)
    result = m.release_gate(samples, policy)
    assert result["reasons"] == ["cpu:slice_missing:fog", "cpu:slice_regression:night"]


def equality(m):
    samples = [{"hardware": "x", "latency_ms": 10., "correct": True, "memory_mb": 5.}]
    result = m.release_gate(samples, _policy(min_samples=1, min_accuracy=1.,
                              max_p99_ms=10., min_throughput_qps=100., max_memory_mb=5.,
                              baseline_accuracy={"all": 1.}, max_slice_drop=0.))
    assert result["passed"]


def immutable(m):
    samples, policy = _samples(), _policy()
    before = copy.deepcopy((samples, policy))
    m.release_gate(samples, policy)
    assert (samples, policy) == before


def invalid(m):
    for bad in (dict(_samples()[0], latency_ms=0), dict(_samples()[0], correct=1),
                dict(_samples()[0], memory_mb=float("nan")), {"warmup": "yes"}):
        try:
            m.release_gate([bad], _policy())
        except ValueError:
            continue
        raise AssertionError("invalid sample must raise")
    for policy in (_policy(min_samples=True), _policy(min_accuracy=1.1), _policy(max_p99_ms=-1)):
        try:
            m.release_gate([], policy)
        except ValueError:
            continue
        raise AssertionError("invalid policy must raise")


TESTS = [
    ("Passing quality and performance", "public", passing),
    ("Tail-latency failure", "public", tail_failure),
    ("Quality failure", "public", quality_failure),
    ("Insufficient measurement count", "hidden", sample_count),
    ("Exclude warmup and invalid measurements", "hidden", exclusions),
    ("Empty measurement evidence", "hidden", no_samples),
    ("Independent hardware classes", "hidden", hardware_groups),
    ("Report every failed rule deterministically", "hidden", all_failures_in_order),
    ("Missing and regressed scenario slices", "hidden", slices),
    ("Threshold equality passes", "hidden", equality),
    ("Input evidence remains unchanged", "hidden", immutable),
    ("Reject invalid measurements and policies", "hidden", invalid),
]
