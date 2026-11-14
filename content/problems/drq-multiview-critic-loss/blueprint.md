---
{
  "schema_version": 1,
  "problem_id": "drq-multiview-critic-loss",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Compute a Multi-View Critic Regression Loss",
  "summary": "Each observed state should contribute equally even when some states have fewer usable augmented views.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2020-data-regularized-q",
    "policy-components"
  ],
  "paper_ids": [
    "2020-data-regularized-q"
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
  "entrypoint": "solution.multiview_critic_loss",
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
      "https://arxiv.org/abs/2004.13649"
    ],
    "paper_card": "research/papers/robot-learning-rl/2020-data-regularized-q.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Compute a Multi-View Critic Regression Loss

## Contract

`predictions` is real `(B, M)`, with `1 <= B <= 128` and `1 <= M <= 64`; `targets` is real `(B,)`; `valid` is Boolean `(B, M)`.

For each state, compute the mean squared prediction-minus-target residual over its valid views. Then average equally over states with at least one valid view. Return a dictionary with:

- `loss`: Python float, the equal-state mean, or zero when no state has a valid view.
- `per_state`: float64 `(B,)`, each state loss, or NaN for a state without views.
- `gradient`: float64 `(B, M)`. Each valid entry is twice its residual divided by both the number of valid views in that state and the number of observed states. Invalid entries are zero.

Targets are fixed; no target gradient is returned. Equal view counts recover ordinary DrQ averaging. The unequal-mask policy is an explicit teaching extension.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
