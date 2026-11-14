---
{
  "schema_version": 1,
  "problem_id": "scenario-coverage-confidence",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Estimate Scenario Coverage and Confidence Intervals",
  "summary": "Estimate Scenario Coverage and Confidence Intervals",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2017-domain-randomization"
  ],
  "paper_ids": [
    "2017-domain-randomization"
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
  "entrypoint": "solution.scenario_coverage",
  "physical_contract": {
    "frames": [
      "Caller-declared calibration/frame retained; no implicit spatial transform"
    ],
    "units": {
      "counts": "scenario trials",
      "rates/coverage/interval": "dimensionless fractions"
    },
    "axes": "Input vectors(N,); bucket arrays(B,), Wilson bounds(B,2) lower then upper",
    "timestamp_assumptions": "No live timestamps; episode scenarios are supplied observations or declarations.",
    "batching": "Input vectors(N,); bucket arrays(B,), Wilson bounds(B,2) lower then upper"
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
    "evaluator_sha256": "d8d9b09a6178fa50a9a5cf887c07cd644ea352dbdb8b7d9fa67d508720f9b151",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/1703.06907"
    ],
    "paper_card": "research/papers/mlops-sim2real/2017-domain-randomization.md",
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

# Estimate Scenario Coverage and Confidence Intervals

Implement scenario_coverage(bucket_ids, success, bucket_count) -> dict.

bucket_ids is NumPy int64(N,), success bool(N,), N in0..100000. bucket_count is a built-in non-bool int1..256; IDs in[0,B). Each row is one independent evaluation scenario with a Boolean task-success outcome. Return counts:int64(B,), success_rate:float64(B,), wilson:float64(B,2), coverage:Python float. Coverage is number of observed buckets divided by B. For each observed bucket use the arithmetic success fraction and the Wilson interval below with fixed z=1.96; clip its two endpoints to[0,1]. Unobserved rates and both interval endpoints are NaN. Preserve inputs and return independent storage. Noncontiguous arrays are valid. Invalid types/dtypes/shapes/ranges raise ValueError.

For n trials and k successes, p=k/n, d=1+z²/n, c=(p+z²/(2n))/d, h=z*sqrt(p*(1-p)/n+z²/(4n²))/d; interval[max(0,c-h),min(1,c+h)]. Rates and intervals are dimensionless. This nominal 95% marginal binomial interval assumes independent, comparable Bernoulli trials within each bucket. It is not a simultaneous guarantee, transfer proof, or interval for unseen buckets.
