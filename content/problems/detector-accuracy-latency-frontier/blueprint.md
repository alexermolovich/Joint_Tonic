---
{
  "schema_version": 1,
  "problem_id": "detector-accuracy-latency-frontier",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Benchmark Detector Accuracy Against Edge Latency",
  "summary": "Find accuracy/latency Pareto candidates and choose a feasible detector from supplied measurements.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "yolo-v1",
    "detector-accuracy-latency-frontier"
  ],
  "paper_ids": [
    "2016-yolo-v1"
  ],
  "paper_sections": [
    "Unified detection grid and training objective; downstream evaluation teaching protocol explicitly distinguished"
  ],
  "track_ids": [
    "paper-2016-yolo-v1"
  ],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "entrypoint": "solution.detector_frontier",
  "physical_contract": {
    "frames": [
      "Benchmark experiment identity, no geometric frame"
    ],
    "units": {
      "values": "accuracy fraction and milliseconds"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent mechanism checks",
      "Boundary and invalid inputs",
      "Input preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "eb5db866833a5256027ee69a4efdeba022087a7a8372361fcdea8697381abfd4"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1506.02640"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "research_curator"
  ]
}
---

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

## Implementation and verification plan

Compare candidate pairs for dominance, then choose the feasible lexicographic optimum. O(N²) time and temporary memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
