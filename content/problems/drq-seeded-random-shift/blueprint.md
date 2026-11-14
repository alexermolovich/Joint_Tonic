---
{
  "schema_version": 1,
  "problem_id": "drq-seeded-random-shift",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Apply a Seeded Random-Shift Augmentation",
  "summary": "Small translations should not alter which physical transition a stack of camera frames represents.",
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
  "entrypoint": "solution.random_shift",
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

# Apply a Seeded Random-Shift Augmentation

## Contract

`images` is real `(B, T, H, W, C)`, with `1 <= B <= 16`, `1 <= T <= 4`, `1 <= H, W <= 64`, `1 <= C <= 3`, and values in `[0, 1]`. `padding` must be a built-in Python int in `[0, 8]`; `seed` must be a built-in Python int in `[0, 2**32 - 1]`. Booleans and NumPy integer scalars are invalid for these two arguments.

Create `rng = np.random.Generator(np.random.PCG64(seed))`. Draw `offsets = rng.integers(0, 2*padding + 1, size=(B, 2), dtype=np.int64)` exactly once, in row-offset/column-offset order. Edge-pad only height and width by `padding` on both sides. For each batch row, crop an H by W window starting at its drawn offsets. Apply that same crop to **every temporal frame and channel** in that row.

Return a dictionary with `images` (float64, original input shape) and `offsets` (int64 `(B, 2)`). With zero padding, return a fresh image copy and zero offsets. Do not interpolate, change colors, shift temporal frames independently or modify NumPy's global random state.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
