---
{
  "schema_version": 1,
  "problem_id": "drq-augmented-bellman-targets",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Average Augmented Bellman Targets",
  "summary": "Several augmentations of one next observation estimate the same transition value.",
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
  "entrypoint": "solution.augmented_targets",
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

# Average Augmented Bellman Targets

## Contract

`rewards` is real `(B,)`; `next_values` is real `(B, K)`, with `1 <= B <= 128` and `1 <= K <= 64`. `terminated` is Boolean `(B,)`; `view_valid` is Boolean `(B, K)`; `gamma` is a scalar in `[0, 1]`.

Average the valid augmented next-state values separately for each transition. Return a dictionary with `targets` and `mean_next` (float64 `(B,)`) and `counts` (int64 `(B,)`). Nonterminal targets equal reward plus gamma times the mean next value. True-terminal targets equal reward. A nonterminal with zero valid views raises ValueError, including when gamma is zero. A terminal may have zero views: report NaN mean, zero count and the finite reward as its target.

All views represent the same physical transition. The supplied values already contain any required SAC entropy adjustment; do not subtract it again or average the reward across views.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
