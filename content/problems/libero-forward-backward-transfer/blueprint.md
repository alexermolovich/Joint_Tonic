---
{
  "schema_version": 1,
  "problem_id": "libero-forward-backward-transfer",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compute a Forward and Backward Transfer Matrix",
  "summary": "Transfer compares evaluations taken at meaningful points in a learning sequence.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "dataset-evaluation",
    "2023-libero"
  ],
  "paper_ids": [
    "2023-libero"
  ],
  "paper_sections": [
    "Mechanism explicitly scoped in the contract"
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
  "entrypoint": "solution.continual_transfer_report",
  "physical_contract": {
    "frames": [
      "Caller-declared physical frames; no inferred transforms"
    ],
    "units": {
      "rates": "dimensionless success fractions",
      "transfer/forgetting": "success-rate differences"
    },
    "axes": "Rates/observed(K+1,K), task j learned at row j+1; returned vectors(K,).",
    "timestamp_assumptions": "Integer nanoseconds on source-video clock where applicable; no wall clock",
    "batching": "Rates/observed(K+1,K), task j learned at row j+1; returned vectors(K,)."
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
    "evaluator_sha256": "46d2bf4a3d854497738468b62585afd1d8c23cec93cb9cc231fb182a39f01163"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded operational teaching component. Backlog PB-115",
    "primary_urls": [
      "https://arxiv.org/abs/2306.03310"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2023-libero.md",
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

# Compute a Forward and Backward Transfer Matrix

## Contract

continual_transfer_report(rates, observed) -> dict{forward,backward,forgetting,forward_mean,backward_mean,forgetting_mean,final_mean}. rates float(K+1,K),1<=K<=256; observed bool same shape. Observed rates must finite[0,1]; unobserved entries may contain arbitrary finite/NaN/Inf placeholders and are ignored. Rows stage0(initial) throughK(final), columns task j=0..K-1 learned at stage j+1. forward[j]=rates[j,j]-rates[0,j] only j>=1 and both observed; backward[j]=rates[K,j]-rates[j+1,j] only j<K-1 and both observed; otherwise NaN. forgetting[j]=max(rates[j+1:K+1,j])-rates[K,j] only j<K-1 and ALL those post-learning stages observed; otherwise NaN. Including final stage makes forgetting nonnegative. Return three float64(K,) vectors; means average only finite entries, NaN if none. final_mean averages observed final-row tasks or NaN if none. This explicit bounded protocol distinguishes transfer from completeness; it is not asserted to match every published LIBERO metric variant.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

rates=[[.1,.2],[.8,.4],[.6,.9]], observed allTrue -> forward[NaN,.2],backward[-.2,NaN],forgetting[.2,NaN],forward_mean.2,backward_mean-.2,forgetting_mean.2,final_mean.75.

### Example 2

K1,rates[[0],[1]],observed allTrue -> allthree vectors[NaN],allthree transfer meansNaN,final_mean1.

## Source and scope

Original bounded component associated with [2023-libero](https://arxiv.org/abs/2306.03310). It does not reproduce the full dataset loader, task suite or headline results.
