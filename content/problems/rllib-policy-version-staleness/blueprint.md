---
{
  "schema_version": 1,
  "problem_id": "rllib-policy-version-staleness",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Track Policy Version Staleness",
  "summary": "Track Policy Version Staleness",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "operational-evidence",
    "2017-rllib"
  ],
  "paper_ids": [
    "2017-rllib"
  ],
  "paper_sections": [
    "Operational component discussed in Theory; explicit original teaching policy"
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
  "entrypoint": "solution.policy_staleness_report",
  "physical_contract": {
    "frames": [
      "Declared robot/session/feature identities; no implicit transform"
    ],
    "units": {
      "lag/max_lag/mean_known_lag": "dimensionless policy-version increments",
      "sample_counts/accepted_samples/rejected_samples": "transition counts"
    },
    "axes": "Version/count vectors(N,); lags and Boolean diagnoses retain input order.",
    "timestamp_assumptions": "Supplied synchronized integer timestamps only where present; no wall clock",
    "batching": "Version/count vectors(N,); lags and Boolean diagnoses retain input order."
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
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "e1f8391a2243990af89454903e131833209ae02a744b783180266247f7196942"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original operational teaching policy; no full paper API reproduction. Backlog PB-396",
    "primary_urls": [
      "https://arxiv.org/abs/1712.09381"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2017-rllib.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "research_curator",
    "perception_completion"
  ]
}
---

# Track Policy Version Staleness

## Contract

`policy_staleness_report(current_version, sample_versions, sample_counts, max_lag) -> dict`. current_version and max_lag are built-in ints in 0..2^63-1. sample_versions and sample_counts are NumPy int64(N,),0<=N<=100000; versions in 0..2^63-1, counts in 0..10^6. Versions newer than current are valid anomaly evidence, not invalid inputs. Return lag:int64(N,)=current-version, future:bool(N,)=lag<0, stale:bool(N,)=lag>max_lag, accepted:bool(N,)=~future & ~stale. Also return Python ints accepted_samples and rejected_samples from the supplied counts, and float mean_known_lag weighted by counts over all nonfuture rows (including stale). If their total count is zero, mean_known_lag=NaN. Use exact integer differences before floating averaging. Version lag is dimensionless, not elapsed time or divergence. Work O(N).

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

current=10, versions[10,7,12], counts[2,6,4], max_lag=2 gives lag[0,3,-2], future[F, F, T], stale[F, T, F], accepted[T, F, F], accepted_samples=2, rejected_samples=10, mean_known_lag=18/8=2.25.

current=0, versions[1], counts[5], max_lag=0 gives lag[-1], future[T], stale[F], accepted[F], accepted_samples=0, rejected_samples=5, mean_known_lag=NaN.

## Source and scope

Original bounded component inspired by [2017-rllib](https://arxiv.org/abs/1712.09381). It does not reproduce the full paper or establish hardware safety or data-use authorization.
