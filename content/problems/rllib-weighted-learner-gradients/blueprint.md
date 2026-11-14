---
{
  "schema_version": 1,
  "problem_id": "rllib-weighted-learner-gradients",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Aggregate Weighted Learner Gradients",
  "summary": "Aggregate Weighted Learner Gradients",
  "type": "function",
  "difficulty": "easy",
  "estimated_minutes": 20,
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
  "entrypoint": "solution.aggregate_learner_gradients",
  "physical_contract": {
    "frames": [
      "Declared robot/session/feature identities; no implicit transform"
    ],
    "units": {
      "mean_gradients/mean/norm": "normalized loss per normalized parameter coordinate",
      "sample_counts/total_samples": "valid transition counts"
    },
    "axes": "Worker mean gradients(P,D),counts(P,),combined mean(D,).",
    "timestamp_assumptions": "Supplied synchronized integer timestamps only where present; no wall clock",
    "batching": "Worker mean gradients(P,D),counts(P,),combined mean(D,)."
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
    "evaluator_sha256": "6e583aba57b6d876a0ac362a6785c52a53b14757351473e05cc8863b8de391a1"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original operational teaching policy; no full paper API reproduction. Backlog PB-009",
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

# Aggregate Weighted Learner Gradients

## Contract

`aggregate_learner_gradients(mean_gradients, sample_counts) -> dict`. mean_gradients is NumPy float32/float64(P, D),0<=P<=4096,1<=D<=256, at most 10^6 entries; all values finite with abs<=10^6, including zero-count rows. sample_counts is NumPy int64(P,),0..10^6. Each gradient is the mean over that worker's valid samples, not a gradient sum. Return mean:float64(D,), norm:Python float L2 norm of the combined mean, total_samples:Python int, has_samples:Python bool. With positive total, mean=sum(n_i*g_i)/sum(n_i); with zero total return a zero vector, norm=0, has_samples=False. Preserve inputs and support noncontiguous arrays. No optimizer step, clipping or gradient transport occurs. Work O(PD).

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

mean_gradients=[[1],[3]], counts[2,6] gives mean[2.5], norm=2.5, total_samples=8, has_samples=True.

mean_gradients=[[100,-20]], counts[0] gives mean[0,0], norm=0, total_samples=0, has_samples=False. A nonfinite ignored row is still invalid evidence.

## Source and scope

Original bounded component inspired by [2017-rllib](https://arxiv.org/abs/1712.09381). It does not reproduce the full paper or establish hardware safety or data-use authorization.
