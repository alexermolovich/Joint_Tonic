---
{
  "schema_version": 1,
  "problem_id": "cql-offline-policy-support",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Evaluate Offline Policy Support",
  "summary": "Offline action support is local to the state where an action was observed.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2020-conservative-q-learning",
    "policy-components"
  ],
  "paper_ids": [
    "2020-conservative-q-learning"
  ],
  "paper_sections": [
    "Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper."
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
  "entrypoint": "solution.offline_action_support",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units."
    },
    "axes": "Batch, action, view and image axes are specified explicitly below",
    "timestamp_assumptions": "All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs.",
    "batching": "Batch, action, view and image axes are specified explicitly below"
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
    "authoring_notes": "Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.",
    "primary_urls": [
      "https://arxiv.org/abs/2006.04779"
    ],
    "paper_card": "research/papers/robot-learning-rl/2020-conservative-q-learning.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Evaluate Offline Policy Support

## Contract

`logged_states` is integer `(N,)`, `logged_actions` is real `(N, D)`, `query_states` is integer `(M,)` and `query_actions` is real `(M, D)`. Bounds are `0 <= N <= 1024`, `0 <= M <= 256`, `1 <= D <= 16`. State identifiers lie in `[0, 1_000_000]`; action coordinates lie in `[-1, 1]`. `max_distance` is a scalar in `[0, 10]`.

For each query, find the logged action with the **same discrete state identifier** and minimum Euclidean action distance. Break equal-distance ties by the smallest original logged row index. Return a dictionary containing `nearest_index` (int64 `(M,)`), `distance` (float64 `(M,)`) and `unsupported` (Boolean `(M,)`). Missing state support produces index -1, NaN distance and true unsupported status. Otherwise unsupported is true only when the distance strictly exceeds `max_distance`; equality passes.

This original finite-state diagnostic is not a continuous-state density estimator or a policy performance guarantee.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
