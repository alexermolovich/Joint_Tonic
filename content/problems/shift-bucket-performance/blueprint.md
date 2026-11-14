---
{
  "schema_version": 1,
  "problem_id": "shift-bucket-performance",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Measure Performance Across Shift Buckets",
  "summary": "Measure Performance Across Shift Buckets",
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
  "entrypoint": "solution.shift_bucket_metrics",
  "physical_contract": {
    "frames": [
      "No spatial transform; preserve caller-supplied scenario/model identities"
    ],
    "units": {
      "errors": "dimensionless normalized comparable loss",
      "counts": "scenario count"
    },
    "axes": "Input vectors (N,); outputs (B,) ordered by bucket ID",
    "timestamp_assumptions": "No live timestamps; latency metrics are supplied durations only.",
    "batching": "Input vectors (N,); outputs (B,) ordered by bucket ID"
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
    "evaluator_sha256": "d2a8cf04bdeb6c4d2b279672e3389c1150fcd8dfaaabbf0bacce26e0a364de28",
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

# Measure Performance Across Shift Buckets

Implement shift_bucket_metrics(bucket_ids, errors, bucket_count) -> dict.

bucket_ids is NumPy int64(N,), errors matching float64(N,),0<=N<=100000. bucket_count is a built-in non-bool int1..256. IDs are in[0,bucket_count), errors finite in[0,1000000]. Each supplied error is a comparable dimensionless normalized per-scenario loss; lower is better. Noncontiguous inputs are valid. Return new arrays counts:int64(B,), mean_error:float64(B,), worst_error:float64(B,), B=bucket_count, in increasing bucket-ID order. Unobserved buckets have count0 and both floating metrics NaN. Observed buckets use arithmetic mean and maximum. Preserve inputs; outputs do not alias inputs or each other. Invalid contracts raise ValueError.

Bucket identity is supplied, not inferred from images. This groups equal-weight scenario measurements; it does not mix raw metres/radians, estimate confidence, or claim a pooled score proves transfer.
