---
{
  "schema_version": 1,
  "problem_id": "cql-discrete-conservative-penalty",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Compute a Conservative Q Penalty",
  "summary": "Conservative Q-learning compares values across the entire finite action set against values of actions that actually appear in the dataset.",
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
  "entrypoint": "solution.conservative_penalty",
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

# Compute a Conservative Q Penalty

## Contract

`q_values` is a real array of shape `(B, A)`, where `1 <= B <= 128`, `1 <= A <= 256` and every magnitude is at most `10_000`. `logged_actions` is an integer array `(B, K)`, with `1 <= K <= 128` and indices in `[0, A)`. Duplicate logged indices are allowed. `valid` is a Boolean array `(B,)`; `alpha` is a scalar in `[0, 100]`.

For each row, compute the raw penalty as log-sum-exp over **all A actions**, minus the mean Q value at its K logged indices. Return a dictionary with:

- `loss`: Python float, alpha times the mean raw penalty over valid rows; zero if none are valid.
- `per_state`: float64 `(B,)`, raw penalties, with exact zero in invalid rows.
- `gradient`: float64 `(B, A)`, alpha divided by the valid-row count, times the difference between the Q softmax and empirical logged-action frequencies. Invalid rows have zero gradient.

Use stable log-sum-exp. This is an exact finite-discrete-action CQL regularizer; arbitrary continuous proposals do not satisfy this contract. No TD loss or optimizer step runs.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
