---
{
  "schema_version": 1,
  "problem_id": "rt2-action-generalization-slices",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Monitor Invalid Actions and Semantic Generalization Slices",
  "summary": "An overall success percentage can hide a policy that emits malformed commands on unfamiliar instructions.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-rt-2",
    "policy-components"
  ],
  "paper_ids": [
    "2023-rt-2"
  ],
  "paper_sections": [
    "Original monitoring component inspired by RT-2 semantic-generalization evaluation. It computes supplied slice metrics and does not infer semantic novelty from images or claim paper-level success."
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
  "entrypoint": "solution.action_slice_metrics",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Rates are dimensionless attempt fractions; semantic slice IDs preserve external evaluation labels."
    },
    "axes": "valid/success/IDs(N) -> per-slice counts/rates(S)",
    "timestamp_assumptions": "Each row is one evaluated attempt, not a timestep; attempts may come from different episodes.",
    "batching": "valid/success/IDs(N) -> per-slice counts/rates(S)"
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
    "authoring_notes": "Original monitoring component inspired by RT-2 semantic-generalization evaluation. It computes supplied slice metrics and does not infer semantic novelty from images or claim paper-level success.",
    "primary_urls": [
      "https://arxiv.org/abs/2307.15818"
    ],
    "paper_card": "research/papers/vla-embodied/2023-rt-2.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Monitor Invalid Actions and Semantic Generalization Slices

## Contract

`action_slice_metrics(valid,success,slice_ids,num_slices)` receives bool(N,) valid and success, integer(N,) slice_ids,0<=N<=10000; integer num_slices1..128, IDs in[0,num_slices). Return dict count:int64(S,), invalid_rate:float64(S,), success_rate:float64(S,). Count all attempted actions. Invalid rate counts ~valid/count. Success counts valid & success/count, so invalid commands cannot count as successes even if a source flag says success. Unobserved slices have count0 and both rates NaN. Each attempt has one already assigned semantic slice.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original monitoring component inspired by RT-2 semantic-generalization evaluation. It computes supplied slice metrics and does not infer semantic novelty from images or claim paper-level success.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
