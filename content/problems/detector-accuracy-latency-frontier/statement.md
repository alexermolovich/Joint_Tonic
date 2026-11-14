# Benchmark Detector Accuracy Against Edge Latency

Implement `detector_frontier(accuracy: np.ndarray, latency_ms: np.ndarray, budget_ms: float) -> tuple[np.ndarray, int]`.

Find accuracy/latency Pareto candidates and choose a feasible detector from supplied measurements.
accuracy is float64 (N,) in [0,1], latency_ms float64 (N,) in (0,1e6],0<=N<=2048. All accuracy values use the same dataset/protocol metric; latency values use the same device/workload statistic (e.g. p95). budget_ms is built-in int/float non-bool in (0,1e6]. Candidate j dominates i if accuracy[j]>=accuracy[i] and latency[j]<=latency[i], with at least one strict inequality. Return int64 ascending indices of nondominated candidates (identical candidates both remain) and Python int selected index. Among candidates latency<=budget, choose highest accuracy, then lowest latency, then smallest input index; return -1 if none. Do not run inference or claim these are measured paper results.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. accuracy=`[0.7,0.8,0.75]`, latency=`[10,20,25]` ms, budget=20: frontier `[0,1]`, selected 1. Candidate 2 is both slower and less accurate than 1.
2. accuracy=`[0.8,0.8]`, latency=`[20,20]`, budget=19: frontier `[0,1]`, selected -1. Identical measurements do not dominate each other; both miss the deadline.

## Source and scope

[Primary source](https://arxiv.org/abs/1506.02640). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
