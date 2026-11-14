---
{
  "schema_version": 1,
  "problem_id": "pareto-edge-model-selection",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Select a Pareto Model Under Accuracy and Latency Limits",
  "summary": "Select a Pareto Model Under Accuracy and Latency Limits",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2020-once-for-all"
  ],
  "paper_ids": [
    "2020-once-for-all"
  ],
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
  "entrypoint": "solution.select_pareto_model",
  "physical_contract": {
    "frames": [
      "No spatial transform; preserve caller-supplied scenario/model identities"
    ],
    "units": {
      "accuracy": "dimensionless fraction",
      "latency": "milliseconds"
    },
    "axes": "Independent named model records; output IDs sorted lexicographically",
    "timestamp_assumptions": "No live timestamps; latency metrics are supplied durations only.",
    "batching": "Independent named model records; output IDs sorted lexicographically"
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
    "evaluator_sha256": "03e5be156a7235fd6e6091fcd175cab95b2704f916e5260d1f2a47c4966f2e17",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/1908.09791"
    ],
    "paper_card": "research/papers/mlops-sim2real/2020-once-for-all.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root"
  ]
}
---

# Select a Pareto Model Under Accuracy and Latency Limits

Implement select_pareto_model(records, min_accuracy, max_latency_ms) -> dict.

records is a list of0–1000 tuples(model_id,accuracy,latency_ms), with unique ASCII IDs[a-z][a-z0-9_-]{0,63}. Accuracy and min_accuracy are built-in non-bool int/float finite in[0,1]; latency and max_latency_ms are such numbers in(0,1000000]. All records refer to the same caller-declared workload, quality metric, device and runtime.

A dominates B iff A has accuracy>=B and latency<=B with at least one strict inequality. Return exactly frontier: sorted list of ALL nondominated model IDs across the full input, and selected: the ID of the feasible record with highest accuracy, then lowest latency, then ASCII ID; None if no record meets accuracy>=min_accuracy and latency<=max_latency_ms. Equal metric duplicates with different IDs both remain on the frontier. Threshold equality passes. Validate every record, preserve inputs; malformed contracts raise ValueError. Empty records gives {"frontier":[],"selected":None}.

Frontier membership and feasibility are separate outputs. No FLOP-to-latency conversion, confidence interval or unseen-device prediction occurs.
