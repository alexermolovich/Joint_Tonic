---
{
  "schema_version": 1,
  "problem_id": "slice-metrics-regressions",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Compare Slice Metrics Without Hiding Regressions",
  "summary": "Compare Slice Metrics Without Hiding Regressions",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-foundations"
  ],
  "topics": [
    "robotics-foundations",
    "numerics-evaluation"
  ],
  "paper_ids": [],
  "paper_sections": [
    "Mechanism described in theory; bounded teaching contract"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; local bubblewrap baseline",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.compare_slice_regressions",
  "physical_contract": {
    "frames": [
      "Caller-aligned robot sensor/controller frames; no implicit transform"
    ],
    "units": {
      "loss/delta/tolerance": "dimensionless comparable normalized loss",
      "counts": "paired episode count"
    },
    "axes": "Input vectors(N,), output slice vectors(S,); supplied episode pairing preserved",
    "timestamp_assumptions": "Episodes and fixed sample ordering supplied; no wall clock or timing inference.",
    "batching": "Input vectors(N,), output slice vectors(S,); supplied episode pairing preserved"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-09,
    "atol": 1e-10,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "independent-oracle",
      "edge-shapes",
      "invalid-contract",
      "preservation",
      "scale"
    ],
    "evaluator_sha256": "f771cb9bce15668abc274bd18149578f17c82f4d85771173b1bf9cae626b8fd2",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original robotics foundation with synthetic fixtures; no paper-derived implementation.",
    "primary_urls": [
      "https://numpy.org/doc/2.2/reference/"
    ]
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root"
  ]
}
---

# Compare Slice Metrics Without Hiding Regressions

Implement compare_slice_regressions(slice_ids, baseline, candidate, slice_count, tolerance) -> dict.

slice_ids NumPy int64(N,), baseline/candidate float64(N,),0<=N<=100000, slice_count built-in non-bool int1..256. IDs in[0,S), losses finite0..1e6; tolerance built-in finite non-bool int/float0..1e6. Each row is a paired evaluation of the same robot episode under baseline and candidate using comparable dimensionless normalized loss; lower is better. Return counts:int64(S,), mean_delta:float64(S,), regressed:bool(S,), overall_delta:Python float or None, complete:bool. Per-row delta=candidate-baseline; mean_delta averages paired deltas within each slice, NaN for unobserved slices. regressed is true iff observed mean_delta>tolerance (strict; equality passes). overall_delta is the mean of ALL paired deltas, None when N=0. complete is true iff every declared slice is observed. Preserve inputs and return independent arrays; noncontiguous valid. Invalid contracts raise ValueError.

This exposes empirical slice regressions even when the pooled result improves. It does not perform significance tests, impute missing evidence, change weights to balance slices, or treat missing slices as passing proof. Caller must align episode identity before this function.
