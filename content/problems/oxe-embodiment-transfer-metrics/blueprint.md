---
{
  "schema_version": 1,
  "problem_id": "oxe-embodiment-transfer-metrics",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Compute Per-Embodiment and Transfer Metrics",
  "summary": "A single average hides whether a shared policy succeeds only on the embodiment it was trained for.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-open-x-embodiment",
    "policy-components"
  ],
  "paper_ids": [
    "2023-open-x-embodiment"
  ],
  "paper_sections": [
    "Original cross-embodiment evaluation aggregation inspired by OXE. A matrix cell measures supplied outcomes and cannot prove transfer causality without controlled baselines."
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
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
  "entrypoint": "solution.embodiment_transfer_metrics",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Rates dimensionless; IDs reference a versioned embodiment registry."
    },
    "axes": "train/test IDs and success(N) -> count/rate(E,E) plus two scalars",
    "timestamp_assumptions": "Each row is one episode evaluation, not an action timestep; train/test IDs label model-training and deployment embodiment.",
    "batching": "train/test IDs and success(N) -> count/rate(E,E) plus two scalars"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-inputs",
      "independent-invariants"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original cross-embodiment evaluation aggregation inspired by OXE. A matrix cell measures supplied outcomes and cannot prove transfer causality without controlled baselines.",
    "primary_urls": [
      "https://arxiv.org/abs/2310.08864"
    ],
    "paper_card": "research/papers/vla-embodied/2023-open-x-embodiment.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Compute Per-Embodiment and Transfer Metrics

## Contract

`embodiment_transfer_metrics(train_ids,test_ids,success,num_embodiments)` takes integer train_ids(N,),test_ids(N,), bool success(N,),0<=N<=10000, integer E=num_embodiments1..64, IDs0..E-1. Return dict count:int64(E,E), success_rate:float64(E,E), same_embodiment_rate:float or None, transfer_rate:float or None. Matrix rows are training embodiment IDs, columns evaluation embodiment IDs. Rates at empty cells are NaN. Same/transfer aggregate success across individual diagonal/off-diagonal attempts (micro averages), not an unweighted mean of cell rates. No observations in an aggregate gives None.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original cross-embodiment evaluation aggregation inspired by OXE. A matrix cell measures supplied outcomes and cannot prove transfer causality without controlled baselines.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
