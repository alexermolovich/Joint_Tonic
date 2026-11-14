---
{
  "schema_version": 1,
  "problem_id": "act-chunk-compounding-error",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Evaluate Chunk Length Against Compounding Error",
  "summary": "Open-loop action errors accumulate until feedback corrects them.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-aloha-act",
    "policy-components"
  ],
  "paper_ids": [
    "2023-aloha-act"
  ],
  "paper_sections": [
    "Original diagnostic inspired by ACT compounding-error motivation. It evaluates supplied residuals in a unit-gain integrator; it does not predict ACT rollout performance or claim an optimal chunk length."
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
  "entrypoint": "solution.chunk_error_scores",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Error channels are normalized dimensionless position increments; all channels are equally weighted, not mixed raw meters and radians."
    },
    "axes": "action_error(T,D), chunk_lengths(K) -> mse(K)",
    "timestamp_assumptions": "Rows are equally spaced control steps. The toy reset represents perfect feedback at each chunk boundary.",
    "batching": "action_error(T,D), chunk_lengths(K) -> mse(K)"
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
    "authoring_notes": "Original diagnostic inspired by ACT compounding-error motivation. It evaluates supplied residuals in a unit-gain integrator; it does not predict ACT rollout performance or claim an optimal chunk length.",
    "primary_urls": [
      "https://arxiv.org/abs/2304.13705"
    ],
    "paper_card": "research/papers/vla-embodied/2023-aloha-act.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Evaluate Chunk Length Against Compounding Error

## Contract

`chunk_error_scores(action_error, chunk_lengths)` receives real error(T,D), 1<=T<=4096, 1<=D<=64, abs entries<=100, and integer lengths(K,), 1<=K<=128, each1..T (duplicates permitted, preserve order). Treat error as position-increment error and restart accumulated position error at each nonoverlapping chunk boundary 0,L,2L,... . Within a chunk, position error is the inclusive cumulative sum of action_error. For each length return mean squared position error across all T*D entries, float64(K,). Include the final partial chunk with its actual length.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original diagnostic inspired by ACT compounding-error motivation. It evaluates supplied residuals in a unit-gain integrator; it does not predict ACT rollout performance or claim an optimal chunk length.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
