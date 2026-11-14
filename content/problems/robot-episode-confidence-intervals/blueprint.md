---
{
  "schema_version": 1,
  "problem_id": "robot-episode-confidence-intervals",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compute Confidence Intervals Across Robot Episodes",
  "summary": "Compute Confidence Intervals Across Robot Episodes",
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
  "entrypoint": "solution.episode_mean_interval",
  "physical_contract": {
    "frames": [
      "Caller-aligned robot sensor/controller frames; no implicit transform"
    ],
    "units": {
      "mean/standard_error/interval": "caller-declared metric unit per column",
      "critical": "dimensionless multiplier"
    },
    "axes": "Input(E,M), independent episode summaries by metric; interval(M,2) lower then upper",
    "timestamp_assumptions": "Episodes and fixed sample ordering supplied; no wall clock or timing inference.",
    "batching": "Input(E,M), independent episode summaries by metric; interval(M,2) lower then upper"
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
    "evaluator_sha256": "551a40c26963ad9893376e8c9871ee8a394f9fcdbe5ba3c3e57fc4e1bfcf398f",
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

# Compute Confidence Intervals Across Robot Episodes

Implement episode_mean_interval(episodes, critical) -> dict.

episodes is NumPy float64(E,M),2<=E<=10000,1<=M<=32,total<=200000; finite abs<=1e6. Each row is one independent robot episode summary; each column a metric in its own fixed declared unit. critical is finite built-in non-bool int/float0..100, a caller-selected two-sided critical multiplier. Compute per-column sample mean, sample variance with denominator E-1, standard_error=sqrt(variance/E), interval[mean-critical*standard_error,mean+critical*standard_error]. Return mean/standard_error float64(M,), interval float64(M,2), new independent arrays; preserve inputs, noncontiguous valid. Invalid contracts raise ValueError. Do not clip bounds or infer a success-rate interpretation.

This arithmetic builds a mean interval using a supplied multiplier. For normally distributed independent episode summaries, a matching Student-t critical value can provide the selected confidence level; the function does not compute that quantile or guarantee coverage for arbitrary distributions. Correlated timesteps from one rollout are not independent episodes. Different metric columns are summarized separately, not pooled.
